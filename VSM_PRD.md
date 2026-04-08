# VSM LLM‑Agent Framework – PRD (Updated)

## 1. Executive Summary
The VSM framework will provide a reusable, LLM‑agent‑driven implementation of Stafford Beer’s Viable System Model (VSM). Each VSM subsystem (Systems 5, 4, 3) **within Management** and **within Operations** will be instantiated as independent LLM agents. This modularity enables recursive nesting, rapid swapping of persistence or LLM providers, and clear separation of concerns.

## 2. Problem Statement
**Who** – Miko, a solo developer building AI‑driven systems.
**What** – Currently each VSM subsystem is hand‑coded; there is no generic agent structure.
**Why** – Repeated ad‑hoc wiring slows development and creates inconsistent interfaces.
**Evidence** – Request.md (lines 3‑4) describes the need for a generic, customizable VSM system.

## 3. Target Users & Personas
| Persona | Role | Goal | Pain |
|---|---|---|---|
| Solo Dev – Miko | Solo developer | Quickly spin up a VSM‑based architecture | Re‑implementing VSM plumbing for each project |
| Team Lead | Leads a small AI team | Reuse VSM components across projects | Inconsistent interfaces and integration effort |
| Researcher | Experiments with recursive VSM models | Swap LLM, persistence, or event‑bus layers | Tight coupling makes swapping hard |

## 4. Strategic Context
- **Business goal** – Reduce time‑to‑prototype VSM‑based AI systems by 50 % (target < 2 days per new use‑case).
- **Why now** – LLM API cost reductions make multi‑agent architectures affordable; solo‑dev schedule demands rapid iteration.
- **Market** – TAM: 200 k AI‑enabled startups; SAM: 10 k needing custom orchestration; SOM: 1 k early‑stage teams needing VSM scaffolding.

## 5. Solution Overview
We will implement each VSM subsystem as an independent LLM agent exposing JSON channels: the **resource‑bargain channel** implements the contract defined in request2.md (budget ↔ expected output).

System 1 agents are concrete functional units (e.g., Read‑email, Web‑research, Journal‑summary). The VSM can add or replace System 1 agents at runtime, enabling adaptability to new input types.

1. **Management Agents** – System 5, 4, 3 each run as separate agents under the Management umbrella.
2. **Operations Agents** – System 1 and System 2 each run as separate agents under the Operations umbrella.
3. **Ports & Adapters** – interchangeable persistence, event‑bus, and LLM provider layers.
4. **Recursive VSM** – Each System 1 agent instantiates a full, nested VSM (Systems 5‑4‑3‑2‑1) as a self‑contained component. This encapsulated VSM can itself spawn further System 1 agents, enabling true recursion. Because recursion is a defining property of VSM, each System 1’s nested VSM can be further instantiated, allowing arbitrary recursion depth.

5. **Channel‑based communication** – agents exchange JSON channels (resource‑bargain, policy, etc.) stored on disk for progressive context disclosure.

### Key Components

Algedonic alerts – lightweight events (pain/pleasure signals) emitted by System 1 agents and propagated up through the channel hierarchy to trigger corrective actions in System 3.

**Thread objects** – a Thread tracks the lifecycle of a System 3 ↔ System 1 interaction.  
• Created when System 3 issues a contract to a System 1.  
• Holds contract ID, participants, message history, and status (open/closed).  
• Persisted as a YAML file via the PersistencePort; closed threads are archived.  
• Enables both sides to query prior exchanges, supporting retries or audits.

| Agent | Responsibility |
|---|---|
| **MGMT‑5** | Policy decisions, balance MGMT‑4/3, expose policy channel |
| **MGMT‑4** | Strategic foresight, monitor environment, expose strategy data |
| **MGMT‑3** | Coordinates MGMT‑1/2 and MGMT‑4, manages operations, **creates/instantiates System 1 agents as needed (based on reports from existing agents)**, expose coordination channel |
| **OPS‑1** | Primary activities execution, expose ops‑1 channel |
| **OPS‑2** | Information channel coordination, expose ops‑2 channel |
| **Common Services** | Event bus, persistence adapters, LLM provider adapters |

| Entity | Core fields | Remarks |
|---|---|---|
| Event | id, timestamp, type, payload | Base class for all bus messages |
| Thread | id, participants, messages[], status | Archived as YAML when closed |
| Contract | id, sys1_id, budget, expected_output, deadline, status | Represents the resource‑bargain contract |
| Report | sys1_id, metrics (dict), timestamp | Produced by System 1, consumed by System 3 |
| Strategy | id, focus_areas[], priority, timestamp | Emitted by System 4 |
| Policy | id, name, value | Defined by System 5 (placeholder) |

**Ports & adapters**

| Port | Responsibility | MVP implementation | Future candidates |
|---|---|---|---|
| EventBusPort | Publish/subscribe events | InProcessBus (queue.Queue) | Redis Streams, Kafka |
| PersistencePort | Save/load entities | YamlFileStore (`data/` folder) | SQLite, Parquet |
| LLMPort | Generate text | LocalLLMAdapter (LangChain) | OpenAI, Anthropic SDKs |
| ToolPort | Invoke tooling functions | LocalToolRegistry (Python callables) | gRPC/HTTP services |
| SchedulerPort | Trigger rules | SimpleTriggerEngine (loop + timers) | APScheduler, Celery beat |
| ConfigPort | Load configuration | YamlConfigLoader | Env‑vars, Consul |

### 5. Runtime Scheduling & Simulation

| Aspect | Design (MVP) | Future swap |
|-------|----------------|------------|
| **Clocks** | • **Real‑time clock** – `datetime.now()` used for “tomorrow” triggers.<br>• **Global step counter** – integer `global_step` incremented after each event‑loop iteration.<br>• **Actor step counters** – dict `actor_step[sys_id]` storing steps per system. | Replace with async clock or discrete‑event simulator. |
| **Trigger Engine** | `TriggerEngine` reads JSON/YAML rule objects (e.g., `{when: "global_step % 100 == 0", do: "emit", type: "StrategyHeartbeat", target: "MGMT‑4"}`) and posts events onto the bus. Rules loaded at startup, hot‑reloaded possible. | Swap to a rule engine such as APScheduler or Drools. |
| **Turn Management** | Simple **round‑robin**: <br>1. Pull next system ID from `actor_order` list.<br>2. Dequeue one event (if any) and handle it.<br>3. Increment its `actor_step` and move to end of list.<br>4. Loop until all queues empty → increment `global_step`. | Replace with priority queue or thread‑pool/async scheduler. |
| **Scheduler Port** | `SchedulerPort` abstract base defines `schedule(rule: dict) -> None` and `tick() -> List[Event]`. MVP implementation is `SimpleTriggerEngine` (loops, evaluates all rules each tick). | Future implementations could expose a cron‑like API or integrate with Celery beat for distributed timing. |

### 7. LLM Agents & Memory (expanded)

| Component | MVP implementation | Why it matters | Future alternatives |
|----------|-------------------|----------------|-------------------|
| **LLMPort** | `LocalLLMAdapter` wraps a LangChain LLM (e.g., gpt4all or llama.cpp). Prompt built with f‑strings: `prompt = f"System 1 context: {ctx}\nMessages:{msg_log}"`. | Keeps prompt generation simple for the prototype. | Switch to a templating engine (Jinja2) for richer composition; add `temperature` field for randomness control. |
| **Observation Memory** | Each agent owns a YAML log file (`data/agent_{id}_log.yaml`). On every action the agent appends `{timestamp, event_type, input, output}`. File read on startup to reconstruct in‑memory list. | Human‑readable, no external deps, easy version‑control. | Replace with SQLite table for faster queries or a vector store (FAISS) for similarity search. |
| **Memory API** | `MemoryPort` defines `append(entry: dict)`, `load_all() -> List[dict]`, `query(filter: Callable) -> List[dict]`. MVP `YamlMemoryAdapter` implements using `ruamel.yaml`. | Provides clean contract for agents to read/write logs without caring about storage format. | Future adapters could expose semantic search or time‑windowed retrieval. |
| **Determinism** | No explicit random seed; LLM may vary. Port records `seed` (if any) in log entry for reproducibility. | Makes debugging easier when re‑running same prompt. | Add `seed` param to `LLMPort.generate(prompt, seed=None)` and store it. |
| **Tool Registry** | `ToolPort` registers Python callables (e.g., `web_search`, `summarize`). Agents discover tools via `ToolRegistry.list()` and invoke by name. | Enables agents to call utilities without hard‑coding imports. | Later expose tools as gRPC services or HTTP endpoints for remote micro‑services.

## 6. Success Metrics
| Metric | Current | Target | Measurement |
|---|---|---|---|
| Setup time | 3 days (manual) | ≤ 1 day (auto‑generated) | Time from repo clone to runnable VSM demo |
| Agent count | 5 agents + manual glue | 5 agents × 2 domains = 10 agents | Code size (lines) |
| Toggle‑ability | Hard‑coded LLM calls | Plug‑and‑play adapters | Unit tests swapping adapters |
| Demonstrated recursion levels | 1 level only | ≥ 2 recursive VSM levels (achieved by each System 1 instantiating its own VSM) | Integration test spawning nested agents |

## 7. User Stories
### Story 2 – OPS‑2 Coordination
**As an** OPS‑2 agent, **I want to** coordinate child agents’ execution order **without a contract**, **so that** system‑wide tasks run deterministically.
*Acceptance Criteria*
- Given three child agents (OPS‑1, OPS‑2, MGMT‑3), when OPS‑2 receives a “run” command, it triggers each child sequentially, aggregates their responses, and reports the overall status.

### Story 3 – MGMT‑4 Strategy
**As a** MGMT‑4 agent, **I want to** expose strategic foresight data, **so that** OPS‑2 can align scheduling.
*Acceptance Criteria*
- When MGMT‑4 updates its environment scan, OPS‑2 receives updated strategy JSON.

### Story 4 – Persistent Event Bus
**As an** EVENT‑BUS, **I want to** persist events to disk, **so that** agents can replay missed messages after restart.
*Acceptance Criteria*
- Given an event emitted, when the bus writes it, then a later consumer reads the event in order.

## 8. Story Splitting (User‑Story‑Splitting)
| Original Story | Split Pattern | Resulting Stories |
|---|---|---|
| Story 2 (OPS‑2 Coordination) | Acceptance criteria complexity | 1. OPS‑2 triggers child agents sequentially <br>2. OPS‑2 aggregates child responses <br>3. OPS‑2 reports overall status |
| Story 3 (MGMT‑4 Strategy) | Business rule variations | 1. MGMT‑4 validates strategy data |
| Story 4 (Event Bus) | Data variations | 1. EVENT‑BUS writes event to JSON file <br>2. EVENT‑BUS reads events on startup <br>3. EVENT‑BUS supports in‑memory queue fallback |

## 12. Extensibility via Skill‑Based Design

| Layer | Purpose | MVP concrete class | Extension path |
|---|---|---|---|
| **Skill definition** | Formal description of an agent’s capability (name, description, JSON schema of parameters). | `Skill` dataclass stored in `skills/` as YAML files (e.g., `read_email.yaml`). | Add new skills by dropping a YAML file – the system auto‑loads them at startup. |
| **Skill registry** | Central lookup for agents to discover which skills are available and their parameter contracts. | `SkillRegistry` reads all `*.yaml` under `skills/` into a dict `name → Skill`. | Plugins can register at runtime (`registry.register(skill)`) for dynamically generated skills. |
| **Skill execution** | Turn a skill into an LLM‑driven function call (function‑calling style). | `SkillExecutor` builds a prompt that includes the skill schema, calls the LLM via `LLMPort`, parses the JSON response, and dispatches to the appropriate `ToolPort` or internal method. | Replace the executor with a function‑calling SDK (OpenAI/Anthropic) that validates JSON automatically. |
| **Skill‑based extensibility flow** | 1. Add a skill YAML.<br>2. (Optional) implement a Python handler class if the skill needs custom logic.<br>3. Register the handler with `SkillRegistry`.<br>4. Agents can now request the skill via `ToolPort` or directly via the LLM. | `SkillHandlerBase` abstract class with `run(params: dict) -> dict`. The MVP includes a `ReadEmailHandler` that reads a local mbox file. | New handlers can be packaged as separate modules or pip‑installable plugins; the registry discovers them via entry‑points. |
| **Benefits** | • Keeps the **LLM‑agent core** thin – most new behavior is added as a declarative skill.<br>• Allows **plug‑and‑play** addition of capabilities without modifying core agent code.<br>• Skills can be versioned, tested, and documented independently. | – | Future UI could expose a **skill marketplace** where users upload a skill YAML + optional handler code. |

---

Each split yields an independent story that can be implemented, tested, and shipped in a single sprint.

## 9. Out of Scope
- UI‑level dashboards for agents – focus on core API first.
- Multi‑cloud deployment – only local Docker compose supported now.
- Advanced analytics on contract negotiations – future iteration.

## 10. Dependencies & Risks
- **Dependencies** – Python 3.11, `openai` SDK, `redis` for in‑process bus.
- **Risks** – Recursive agent spawning may cause circular imports; mitigated by explicit adapter interfaces.
- **Open Questions** – Contract versioning: JSON‑Schema vs protobuf? Decision pending after first prototype.

## 11. Acceptance Criteria for PRD
- All five user stories are implemented as unit‑tested Python modules.
- Two recursive VSM levels are demonstrated in `demo.py`.
- Success metrics are instrumented in CI (setup time < 1 day, adapter swap test passes).

---
*Prepared by the PRD workflow (problem‑statement → proto‑persona → PRD → user‑stories → story‑splitting). Updated to reflect per‑system agents within Management and Operations.*