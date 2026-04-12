**Roadmap Context Summary**

| Area | Key Points |
|------|------------|
| **Executive Summary** | VSM‑LLM‑Agent framework implements Stafford Beer’s Viable System Model as independent LLM agents (Management 5‑4‑3, Operations 1‑2) with a hexagonal ports‑and‑adapters architecture. |
| **Problem** | Current VSM subsystems are hand‑coded; lack reusable, interchangeable agents and generic persistence/LLM layers, slowing prototyping. |
| **Target Users** | Solo developers (e.g., Miko), small AI teams, researchers needing fast VSM scaffolding. |
| **Strategic Context** | Goal: cut time‑to‑prototype VSM‑based AI systems by 50 % (≤ 2 days per use‑case). Market size ≈ 200 k AI startups; SAM ≈ 10 k; SOM ≈ 1 k. |
| **Solution Overview** | • Each VSM subsystem is a distinct LLM agent communicating via JSON channels (resource‑bargain, policy, etc.).<br>• Agents can recursively instantiate full VSMs (System 1 → nested VSM).<br>• Ports define contracts; adapters implement them (EventBus, Persistence, LLM, Tool, Scheduler, Config, Rule, TurnManager, Memory). |
| **Core Ports & Adapters** | - **EventBusPort** → `InProcessBus` (publish/subscribe).<br>- **PersistencePort** → `YamlFileStore` (read/write YAML).<br>- **LLMPort** → `LocalLLMAdapter` (wrap LangChain model).<br>- **ToolPort** → `LocalToolRegistry` (executes Python callables).<br>- **SchedulerPort** → `SimpleTriggerEngine` (JSON/YAML rule triggers).<br>- **ConfigPort** → `YamlConfigLoader`.<br>- **RulePort** → `YamlRuleAdapter` (dynamic rule CRUD).<br>- **TurnManagerPort** → `InMemoryTurnManager` (round‑robin, O(1) ops) with optional `WeightedRootManager` for unequal slices.<br>- **MemoryPort** → per‑agent observation log (append/load/query). |
| **Three‑Clock Model** | **ClockPort** abstracts real‑time, global step, and per‑actor step counters; publishes `global_tick` events used by the rule engine and turn manager. |
| **Rule Engine** | Reactive engine registers rules (YAML) that listen to events, evaluate compiled conditions, and run actions. Supports dynamic add/remove, persistence, and deterministic priority ordering. |
| **Turn Management** | Hierarchical `InMemoryTurnManager` maintains a flat actor list with O(1) add/remove/next. Nested VSMs register their own manager with the parent, enabling interleaved scheduling across all agents. |
| **Recursion Flow** | `System3` may spawn `System1` agents; a `System1` can create its own nested VSM, inheriting shared ports. This enables arbitrary recursion depth while keeping adapters lightweight. |
| **Success Metrics** | - Setup time ≤ 1 day.<br>- ≥ 10 agents across 2 domains.<br>- Adapter swap test passes.<br>- Recursive VSM demonstrated (2‑level nesting). |
| **Open Items** | - Implement concrete adapters for the ports (currently described, not in code).<br>- Add a `SkillPort` if skill‑based extensibility is needed. |
| **Next Steps** | 1. Materialize adapters (`InProcessBus`, `YamlFileStore`, `LocalLLMAdapter`, etc.).<br>2. Implement `ClockPort` singleton (`core/time.py`).<br>3. Wire ports into agents and the rule engine.<br>4. Write integration tests covering rule registration, clock ticks, and nested VSM spawning. |

*This summary captures the current design state, identified components, and the immediate roadmap actions needed to move from the documented design (Step 1‑3) to a runnable prototype.*
