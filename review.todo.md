# Design Review TODO – VSM LLM‑Agent System

*Goal*: Validate the core functional design choices (Solution Overview, Key Components, Data Model) and capture any needed refactors.

## 1. Solution Overview (foundation)
- [ ] Verify the high‑level hexagonal architecture and LLM‑driven agents support the intended recursion flow.
- [ ] Confirm the three‑clock model (real‑time, global step, actor step) is well defined and documented.
- [ ] Review the TriggerEngine rule format (JSON/YAML) for expressiveness.
- [ ] Evaluate the round‑robin turn‑management algorithm for scalability and determinism.

## 2. Key Components (ordered by dependency)
### 2.1 Agents (most fundamental)
- [ ] Ensure responsibilities of MGMT‑5, MGMT‑4, MGMT‑3, OPS‑1, OPS‑2 are distinct and non‑overlapping.
- [ ] Validate MGMT‑3’s logic for spawning System 1 agents matches the recursion requirement.
- [ ] Identify any missing agent types (e.g., System 2, System 5) and decide if they need explicit definitions.

### 2.2 Ports & Adapters (next layer)
- [ ] Confirm each port interface (EventBusPort, PersistencePort, LLMPort, ToolPort, SchedulerPort, ConfigPort) is minimal yet complete.
- [ ] Verify MVP concrete adapters (InProcessBus, YamlFileStore, LocalLLMAdapter, LocalToolRegistry, SimpleTriggerEngine, YamlConfigLoader) fully implement their contracts.
- [ ] Spot any coupling between ports that could hinder future swapping (e.g., SchedulerPort depending on EventBusPort).
- [ ] Determine whether an additional SkillPort is needed for the skill‑based extensibility layer.

### 2.3 Runtime Scheduling & Simulation (built on ports)
- [ ] Review the three‑clock definitions and their interactions; ensure no ambiguity about which clock drives which events.
- [ ] Validate the TriggerEngine rule example (global_step heartbeat) and test edge cases (conflicts, ordering).
- [ ] Assess whether the simple round‑robin turn management will scale with many System 1 agents.

### 2.4 LLM Agents & Memory (uses ports)
- [ ] Examine LLMPort prompt construction (f‑string) for readability and future templating needs.
- [ ] Verify the Determinism note (seed handling) is captured in the LLMPort API.
- [ ] Review MemoryPort API (`append`, `load_all`, `query`) for completeness; consider bulk‑load or delete ops.
- [ ] Check observation‑memory log format (YAML entries) for consistency and easy parsing.
- [ ] Ensure ToolPort registration/discovery does not create circular imports with agents.

### 2.5 Skill‑Based Extensibility (top of key components)
- [ ] Validate the skill YAML schema (name, description, parameters) for function‑calling style.
- [ ] Confirm SkillRegistry correctly loads all `*.yaml` files and handles duplicates.
- [ ] Review SkillExecutor flow (LLMPort → parse JSON → dispatch to ToolPort/handler) and define error handling.
- [ ] Decide if a dedicated `SkillPort` abstraction would clarify responsibilities.

## 3. Data Model (depends on all above)
- [ ] Verify each entity (Event, Thread, Contract, Report, Strategy, Policy) includes all required fields.
- [ ] Ensure the YAML persistence mapping (PersistencePort → YamlFileStore) correctly serialises each entity.
- [ ] Check naming consistency (`Thread.id` vs `thread_id` in code) to avoid mismatches.
- [ ] Evaluate whether extra entities (e.g., SchedulerState) are needed for future extensions.
- [ ] Confirm versioning fields (e.g., contract version) are present for audit trails.

---
*Mark items as done when the design is accepted or note the needed refactor.*