# Skill tool usage:
  - skills often recommend using a workflow.. if a task can be accomplished via the workflow perfer following the relevant steps instead of solving a task another way
  - skills are written for you the agent/assistant and also meant to be performed by you, not the user. 
## Python Usage in skills:
  - some skills may have and recommend python script usage.. always use `uv run python` instead of just calling python directly
  - prioritizebuilt in scripts from skills over tools liek grep / glob / read (unless specified or no alternatives exist)

<!-- This section is maintained by the coding agent via lore (https://github.com/BYK/opencode-lore) -->
## Long-term Knowledge

### Architecture

<!-- lore:019d6aa2-2c8b-71d8-8348-23cd5dc35904 -->
* **Hexagonal ports‑and‑adapters**: Hexagonal ports-and-adapters: Core domain depends on abstract ports EventBusPort, PersistencePort, LLMPort, ToolPort, SchedulerPort, ConfigPort, RulePort, TurnManagerPort, and MemoryPort. Concrete adapters live under adapters/ and are shared singletons across VSMs, enabling easy swapping without touching core code.

<!-- lore:019d6aa2-2c91-700c-9569-8b24c720c596 -->
* **Three‑clock time model**: Three-clock time model: System uses three independent clocks: real-time (datetime.now()), a global step counter incremented each loop, and per-actor step counters stored in a dict. Each clock can emit an event to the rule engine for time-based rules.

### Decision

<!-- lore:019d7acb-f11c-740a-a103-0d02433c821d -->
* **Step 2‑2 handoff updated with progress**: The handoff file .claude/handoffs/2026-04-10-161051-continue-ports-table.md now records completion of MVP adapters (item 9), coupling analysis (item 10), and marks the SkillPort decision (item 11) as skipped. It also adds a next step to continue with the review.todo file, giving future agents a clear snapshot of what’s done and what’s next.

### Gotcha

<!-- lore:019d6eb5-3fb9-774d-9450-b3564282886d -->
* **Cursor modulo zero‑division in TurnManager**: Cursor modulo zero-division in TurnManager: Fix TurnManager.remove\_actor: guard empty actor\_order before modulo to avoid ZeroDivisionError.

<!-- lore:019d6ee4-a4dc-77eb-a921-ca9cc65fbbe7 -->
* **Design 2 duplicate bus subscriptions**: Duplicate bus subscriptions in ReactiveEngine cause multiple identical callbacks per event type, adding O(N) overhead and double‑processing. Fix by maintaining a set of already‑subscribed event types; on add\_rule, subscribe to the bus only if the event type isn’t in the set, then add it. This ensures each event type has a single subscription and streamlines listener registration.

<!-- lore:019d6e3a-e517-7d01-9d7c-1893ac4b9c79 -->
* **Many listeners on frequent events**: Many listeners on frequent events: Mitigate by splitting events into sub-types (e.g., even/odd ticks) or throttling listeners to reduce O(N) overhead.

<!-- lore:019d6aa2-2c97-761f-85d4-488b1efd24f0 -->
* **Missing actor\_order update**: Missing actor\_order update: If a System 1 spawns a nested VSM but does not add its agents to actor\_order, the turn manager never schedules them. Ensure spawn logic updates the list.

<!-- lore:019d6e3a-e518-761c-bf55-eb3b9e592047 -->
* **Missing SkillPort abstraction**: Missing SkillPort abstraction: Skill-based extensibility mixes concerns using RulePort and ToolPort. Add a dedicated SkillPort for the skill lifecycle.

<!-- lore:019d6aa2-2c99-71a2-a822-d7e1c393d4e6 -->
* **SchedulerPort coupling**: SchedulerPort coupling: Keep SchedulerPort abstract and inject the bus only where needed to enable easy swapping.

<!-- lore:019d7a5f-356b-79bb-9603-083a578f50cc -->
* **TurnManagerPort event‑bus coupling**: TurnManagerPort consumes \`global\_tick\` events from EventBusPort to drive its turn cycle, creating a hard dependency on the bus and on the event name. Decouple by letting TurnManagerPort receive a generic tick callback (or a TickSource interface) that can be wired to the bus or to any other scheduler, making the manager portable across transports.

### Pattern

<!-- lore:019d6eb5-3fba-7a2f-adb7-1213848148be -->
* **Centralized port list for documentation**: Centralized port list for documentation: Maintain a single Ports table listing all abstract ports. Reference this table from each design section to avoid duplicate edits when ports change.

<!-- lore:019d6ae8-bc31-7803-bc5f-eecbbe60adc9 -->
* **Components that create or listen to rules**: Components using RulePort: System 3, System 4, System 5, Scheduler, Turn-manager, UI panels, tests use RulePort for rule management.

<!-- lore:019d6aa2-2c94-7f5e-859f-feacbee08a7f -->
* **Event‑driven rule engine**: SchedulerPort coupling: The current SimpleTriggerEngine implementation directly publishes \`global\_tick\` events on an EventBusPort, binding the scheduler to a specific bus. To enable swapping, make SchedulerPort accept an optional EventBusPort in its constructor and expose a pure \`tick()\` method. This isolates timing logic from event publishing and lets alternative schedulers use callbacks instead of a bus.

<!-- lore:019d7acb-f11a-7847-a4e3-d290827e72ac -->
* **Ports table as interim spec**: Maintain an interim ports specification as a markdown table in step\_2\_2\_working.md; treat this table as the authoritative source before generating Python abstract port classes. It simplifies validation against the SBOM and keeps documentation lightweight.

<!-- lore:019d6e3a-e514-7ce2-91eb-69a07e9f870c -->
* **Recursion trigger based on report complexity**: Recursion trigger based on report complexity: System 1 agents spawn a child VSM if report.complexity\_score > THRESHOLD (e.g., 0.7).

<!-- lore:019d6aa2-2c92-7e64-b0bf-985e941bcd39 -->
* **Recursive VSM spawning**: Recursive VSM spawning: System 1 agents instantiate a nested VSM as a child, re-use port instances, and register agents with the turn manager.

<!-- lore:019d6aa2-2c95-7681-a3ef-d5cfd05a25d2 -->
* **Rule persistence in YAML**: Rule persistence in YAML: Rule definitions live in config/rules.yaml. YamlRuleAdapter loads and writes rules dynamically.

<!-- lore:019d6ae8-bc30-7141-bb6c-d07bd5396a6d -->
* **RulePort abstraction for dynamic rule management**: RulePort abstraction: Defines add\_rule, remove\_rule, list\_rules. Rules include a compiled condition field \_cond and protected flag.

<!-- lore:019d6e3a-e513-7904-b3ef-c61d3aa34c51 -->
* **TurnManagerPort abstract interface**: TurnManagerPort abstract interface: Defines add\_actor(id), remove\_actor(id), next\_actor() -> Optional\[str].
<!-- End lore-managed section -->
