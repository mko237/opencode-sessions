# Step 2‑2 – Working Document

## Tasks (2.2 – Ports & Adapters)
- [ ] 8) Confirm each port interface (EventBusPort, PersistencePort, LLMPort, ToolPort, SchedulerPort, ConfigPort,RulePort,TurnManagerPort,MemoryPort) is minimal yet complete.
- [ ] 9) Verify MVP concrete adapters (InProcessBus, YamlFileStore, LocalLLMAdapter, LocalToolRegistry, SimpleTriggerEngine, YamlConfigLoader) fully implement their contracts.
- [ ] 10) Spot any coupling between ports that could hinder future swapping (e.g., SchedulerPort depending on EventBusPort).
- [ ] 11) Determine whether an additional SkillPort is needed for the skill‑based extensibility layer.

| Port | Description | Methods / Properties (minimal API) | Notes |
|------|-------------|--------------------------------------|-------|
| **EventBusPort** | Central publish/subscribe bus used by all components to emit and listen for events. | `publish(event)` – send an event object
`subscribe(event_type, handler)` – register a callable for a given type | Defined only in *step_1_working.md*; no concrete `InProcessBus` class yet. |
| **PersistencePort** | Abstract storage layer for reading/writing files or other durable data. | `read(path) → str`
`write(path, content)`
`list_dir(path) → List[str]` | Mentioned in the design; implementation (e.g., `YamlFileStore`) not present in the repo. |
| **LLMPort** | Wrapper around an LLM backend (local model, API client, etc.). | `generate(prompt, **kwargs) → str` | Interface only; concrete adapters such as `LocalLLMAdapter` are planned. |
| **ToolPort** | Registry/execution interface for external tools (shell commands, python scripts, etc.). | `execute(tool_name, **kwargs) → Any` | No concrete `LocalToolRegistry` exists yet. |
| **SchedulerPort** | Simple timer/trigger service for delayed callbacks. | `schedule(callback, delay)` – schedule a call after *delay* steps/ticks
`cancel(job_id)` – cancel a scheduled job | Planned concrete `SimpleTriggerEngine` is not in the codebase. |
| **ConfigPort** | Access to configuration values (YAML, env vars, etc.). | `get(key) → Any`
`set(key, value)` | Concrete `YamlConfigLoader` is referenced but not implemented. |
| **RulePort** | Manages dynamic rule objects for the reactive engine. | `add_rule(rule)`
`remove_rule(rule_id)`
`list_rules() → List[Rule]` | Used by System 3; no concrete `YamlRuleAdapter` file yet. |
| **TurnManagerPort** | Schedules actors (systems) each step in a round‑robin fashion. | `add_actor(actor_id)`
`remove_actor(actor_id)`
`next_actor() → Optional[str]` | Abstract class defined in the markdown; a concrete `InMemoryTurnManager` implementation is present in the design snippet, but not in a Python module. |
| **MemoryPort** | Simple per‑agent observation log abstraction. | `append(entry)` – add a log entry
`load_all() → List[Entry]` – retrieve all entries
`query(**filters) → List[Entry]` | Only described; no storage implementation yet. |

