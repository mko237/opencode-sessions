# Design Review TODO – VSM LLM‑Agent System

*Goal*: Validate the core functional design choices (Solution Overview, Key Components, Data Model) and capture any needed refactors.

## 1. Solution Overview (foundation)
- [x] 1) Verify the high‑level hexagonal architecture and LLM‑driven agents support the intended recursion flow.
- [x] 2) Confirm the three‑clock model (real‑time, global step, actor step) is well defined and documented.
- [x] 3) Review the TriggerEngine rule format (JSON/YAML) for expressiveness.
- [x] 4) Evaluate the round‑robin turn‑management algorithm for scalability and determinism.
- work for the above have been documented in step_1_working.md use the full file contents as a more detailed reference

## 2. Key Components (ordered by dependency)
### 2.1 Agents (most fundamental)
- [x] 5) Ensure responsibilities of MGMT‑5, MGMT‑4, MGMT‑3, OPS‑1, OPS‑2 are distinct and non‑overlapping.
- [x] 6) Validate MGMT‑3’s logic for spawning System 1 agents matches the recursion requirement.
- [x] 7) Identify any missing agent types (e.g., System 2, System 5) and decide if they need explicit definitions.
- work for the above have been documented in step_2_1_working.md use the full file contents as a more detailed reference

### 2.2 Ports & Adapters (next layer)
- [x] 8) Confirm each port interface (EventBusPort, PersistencePort, LLMPort, ToolPort, SchedulerPort, ConfigPort) is minimal yet complete.
- [ ] 9) Verify MVP concrete adapters (InProcessBus, YamlFileStore, LocalLLMAdapter, LocalToolRegistry, SimpleTriggerEngine, YamlConfigLoader) fully implement their contracts.
- [ ] 10) Spot any coupling between ports that could hinder future swapping (e.g., SchedulerPort depending on EventBusPort).
- [x] 11) Determine whether an additional SkillPort is needed for the skill‑based extensibility layer.
- [ ] 24) Add ports/ package with abstract base classes for each defined port.
- [ ] 25) Implement concrete adapters (InProcessBus, YamlFileStore, LocalLLMAdapter, etc.) under adapters/.

### 2.3 Runtime Scheduling & Simulation (built on ports)
- [ ] 12) Review the three‑clock definitions and their interactions; ensure no ambiguity about which clock drives which events.
- [ ] 13) Validate the TriggerEngine rule example (global_step heartbeat) and test edge cases (conflicts, ordering).
- [ ] 14) Assess whether the simple round‑robin turn management will scale with many System 1 agents.

### 2.4 LLM Agents & Memory (uses ports)
- [ ] 15) Examine LLMPort prompt construction (f‑string) for readability and future templating needs.
- [ ] 16) Verify the Determinism note (seed handling) is captured in the LLMPort API.
- [ ] 17) Review MemoryPort API (`append`, `load_all`, `query`) for completeness; consider bulk‑load or delete ops.
- [ ] 18) Check observation‑memory log format (YAML entries) for consistency and easy parsing.
- [ ] 19) Ensure ToolPort registration/discovery does not create circular imports with agents.

### 2.5 Skill‑Based Extensibility (top of key components)
- [ ] 20) Validate the skill YAML schema (name, description, parameters) for function‑calling style.
- [ ] 21) Confirm SkillRegistry correctly loads all `*.yaml` files and handles duplicates.
- [ ] 22) Review SkillExecutor flow (LLMPort → parse JSON → dispatch to ToolPort/handler) and define error handling.
- [ ] 23) Decide if a dedicated `SkillPort` abstraction would clarify responsibilities.

## 3. Data Model (depends on all above)
- [ ] 24) Verify each entity (Event, Thread, Contract, Report, Strategy, Policy) includes all required fields.
- [ ] 25) Ensure the YAML persistence mapping (PersistencePort → YamlFileStore) correctly serialises each entity.
- [ ] 26) Check naming consistency (`Thread.id` vs `thread_id` in code) to avoid mismatches.
- [ ] 27) Evaluate whether extra entities (e.g., SchedulerState) are needed for future extensions.
- [ ] 28) Confirm versioning fields (e.g., contract version) are present for audit trails.

---
*Mark items as done when the design is accepted or note the needed refactor.*
