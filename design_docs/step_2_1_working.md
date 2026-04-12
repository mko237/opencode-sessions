# Step 2‑1 – Working Document

## Goal
Capture the items from the **2.1 Tasks** section of the design review (items 5‑7) for focused work.

## Tasks (2.1 – Agents)
- [x] 5) Ensure responsibilities of MGMT‑5, MGMT‑4, MGMT‑3, OPS‑1, OPS‑2 are distinct and non‑overlapping.
- [x] 6) Validate MGMT‑3’s logic for spawning System 1 agents matches the recursion requirement.
- [x] 7) Identify any missing agent types (e.g., System 2 (OPS‑2), System 5 (MGMT‑5)) and decide if they need explicit definitions.

---

##  Item 5

**Responsibilities (section‑based reference)**

| Component | Responsibility | Source section(s) |
|---|---|---|
| MGMT‑5 (Policy / Config) | Sets top‑level policy (system scope, recursion‑trigger threshold, child‑VSM config) that the lower‑level components read at startup. | VSM Wiki – “System 5 (MGMT‑5)” |
| MGMT‑4 (Strategic Orchestrator) | Performs strategic and future‑looking activities; does not directly spawn child VSMs. | VSM Wiki – “System 4” |
| MGMT‑3 (Rule Engine) | Holds the rule set that drives the recursion trigger and child‑VSM lifecycle; integrates the compiled conditions from Design for Item 2 – Event‑Driven Rule Engine and the dynamic rule handling described in Design for Item 3 – TriggerEngine / Dynamic Rule Management. | Design for Item 2 & Design for Item 3 |
| OPS‑1 (Recursion Worker) | Executes the recursion logic for a given agent: evaluates the latest report, calls the rule engine to check the trigger condition, and invokes the orchestrator to create a child VSM when needed. | VSM Wiki – “System 1” |
| OPS‑2 (Child VSM Monitor) | Tracks the health and performance of any spawned child VSMs, aggregates their metrics, and reports them back to OPS‑3 for policy updates. | VSM Wiki – “System 2 (OPS‑2)” |

**How the pieces fit together**

1. MGMT‑5 defines the recursion‑trigger threshold (`THRESHOLD`) and child‑VSM configuration.
2. MGMT‑4 watches each agent’s report (via OPS‑1) and, when `report.complexity_score > THRESHOLD`, creates a child VSM.
3. MGMT‑3 supplies the rule that encodes the trigger (`when: "report.complexity_score > THRESHOLD"`) and the rule that cleans up the child VSM once it finishes.
4. OPS‑1 runs per‑agent and calls the rule engine (MGMT‑3) to evaluate the trigger condition.
5. OPS‑2 monitors any active child VSMs, feeds their status back to MGMT‑5, and updates the turn‑manager’s actor list (see Design for Item 4 – Turn‑manager (Hybrid Hierarchical)).

These responsibilities are anchored to the concrete sections you’ll see in the source files, so they remain stable even if line numbers shift.

##  Item 6
### Design – MGMT‑3 creates System 1 (spawn logic)

**Goal** – capture the refined design where System 3 both decides **and** creates a child System 1.

**High‑level flow**
```
System 5 MGMT‑5) (Policy) ──► System 3 (Rule Engine) ──► System 1 (User I/O) (default)
      │                         │
      │   creates default       │   emits CapabilityRequest when it needs a new capability
      ▼   System 1 (User I/O)  ▼
System 1 (User I/O) ──► CapabilityRequest ──► System 3 (Rule Engine)
                                                    │
                                                    │   creates child System 1 (worker)
                                                    ▼
                                                Turn‑Manager
```

**Component responsibilities**
| Component | Responsibility |
|---|---|
| System 5 (MGMT‑5) – Policy/Config | Holds global purpose and default System 1 type |
| System 3 – Rule Engine | Stores the rule that matches `CapabilityRequest`; when it fires, creates a new System 1 via `ToolPort.create_system1` and registers it with `TurnManagerPort`. |
| System 1 – User I/O (default) | Communicates with the user; emits `CapabilityRequest` when a new capability is needed. |
| System 1 – Worker (spawned) | Executes the concrete capability (e.g., email monitoring). |
| Turn‑Manager | Schedules all System 1 actors in a round‑robin list. |

**Rule definition (config/rules.yaml)**
```yaml
- id: spawn-system1
  on: CapabilityRequest
  when: "payload.capability_desc != ''"
  priority: 10
  action: spawn_system1
```

**Callback in System 3**
```python
class RuleEngine:
    def __init__(self, event_bus, tool_port, turn_manager, config):
        self.event_bus   = event_bus
        self.tool_port   = tool_port
        self.turn_manager = turn_manager
        self.config      = config
        self.event_bus.subscribe("CapabilityRequest", self.on_capability)

    def on_capability(self, payload):
        rule = self.rule_port.get_rule("spawn-system1")
        if rule._cond(payload):
            self.spawn_system1(payload)

    def spawn_system1(self, payload):
        cfg = self.config.get("default_system1")
        cfg = {**cfg, "type": payload.capability_desc}
        child_id = self.tool_port.create_system1(parent_id=self.vsm_id, config=cfg)
        self.turn_manager.add_actor(child_id)
        self.event_bus.publish(
            "SpawnedChildSystem1",
            {"parent_id": self.vsm_id, "child_id": child_id}
        )
```

**End‑to‑end example**
1. System 5 (MGMT‑5) defines `default_system1 = {"type":"user_io"}`.
2. System 3 loads the rule and subscribes to `CapabilityRequest`.
3. Default System 1 receives a user request “monitor my Gmail” and publishes `CapabilityRequest` with `capability_desc="email_monitor"`.
4. System 3 matches the rule, calls `spawn_system1`, creates a child System 1 of type `email_monitor`, and adds it to the Turn‑Manager.
5. Turn‑Manager schedules the child; it starts fetching mail.

**Test ideas**
- Rule‑condition unit: `rule._cond({"capability_desc":"x"}) == True`.
- Rule‑match integration: mock `ToolPort.create_system1` and assert it is called when a `CapabilityRequest` is published.
- Turn‑manager registration: after spawn, verify the child id appears in `actor_order`.
- Full flow: simulate the whole sequence and assert two actors (default + child) are scheduled.
- No‑spawn case: empty `capability_desc` → rule does not fire.

**Risks & mitigations**
- Rule typo – validate on load.
- Duplicate CapabilityRequests – debounce with a timestamp per `agent_id`.
- Missing `default_system1` config – fail fast on startup.
- Turn‑manager race – `add_actor` appends; `next_actor` reads the current length.

##  Item 7
**System 2 (OPS‑2) – Information Channels & Resource Scheduler**

- Core function: provides a publish/subscribe API that any component (System 1, System 3, System 4, System 5 (MGMT‑5)) can use to emit and listen for events.
- Scheduling role: maintains a simple resource‑allocation table (e.g., CPU slots, I/O channels, external service handles) and grants a shared‑resource token to each System 1 instance when it schedules a task. This prevents contention and lets System 3 query resource availability when coordinating the agents.
- Typical usage pattern:
  1. System 1 registers its topic (e.g., `sys1‑<id>`).
  2. System 1 calls `request_resource(resource_id)` → System 2 (OPS‑2) checks the allocation table, reserves the slot, and returns a token.
  3. System 1 publishes its event; System 3 subscribes to the topic and, when needed, asks System 2 (OPS‑2) for the next free slot.
- Why it matters: without a central scheduler, each System 1 would need its own queue and conflict‑resolution logic; System 2 (OPS‑2) centralises both messaging and resource arbitration, keeping the design lightweight and extensible.

**System 5 (MGMT‑5) – Policy / Configuration Source**

- Responsibility: owns the global policy configuration for the VSM (recursion‑threshold, default System 1 type, max concurrent child VSMs, etc.).
- Event emission: when a policy value changes (e.g., a new threshold is set or a limit is reached), System 5 (MGMT‑5) publishes a `PolicyUpdate` event on System 2 (OPS‑2)’s bus.
- Consumers:
  - System 3 (Ops‑Ctrl) subscribes to `PolicyUpdate` to adjust rule‑engine thresholds and to decide whether to spawn additional System 1 agents.
  - System 4 (Strategic Orchestrator) listens for policy changes to recalibrate its strategic planning (e.g., altering the cadence of global coordination).
- Interaction flow:
  1. System 5 (MGMT‑5) updates its internal policy dict (`self.policy[key] = value`).
  2. System 5 (MGMT‑5) calls `event_bus.publish("PolicyUpdate", {"key": key, "value": value})`.
  3. System 3 and System 4 receive the payload, extract the updated field, and apply it to their local state.
- Benefit: centralising policy in System 5 (MGMT‑5) ensures a single source‑of‑truth; any component that needs the current policy can either read it directly from System 5 (MGMT‑5) (synchronous) or react to the asynchronous `PolicyUpdate` events.
