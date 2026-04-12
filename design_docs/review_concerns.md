# Design Review – Critical Concerns

| Area | Issue | Why it matters |
|------|-------|----------------|
| **Port definitions** | The port list is extensive but several ports overlap in responsibility (e.g., `RulePort` vs `SchedulerPort`, `EventBusPort` vs `SchedulerPort` coupling). | Overlap can cause duplicated logic, harder to reason about which component should own rule evaluation or timing. |
| **Missing SkillPort** | `SkillPort` is listed as a possible addition but not defined; the skill flow currently goes `SkillRegistry → SkillExecutor → ToolPort`. | Without a dedicated port the skill‑layer mixes with tool registration, making future extensions (e.g., remote skill services) harder to plug in. |
| **MemoryPort API** | Provides only `append`, `load_all`, `query`. No `delete` or bulk‑load, and the query signature is vague (`query(**filters)`). | Agents that need to prune old observations or perform range queries will have to add ad‑hoc methods, breaking the contract. |
| **Turn‑manager scalability** | The O(1) set‑based design works for many agents, but the optional `WeightedRootManager` is only sketched and not fully specified (how weights affect ordering, how they are updated). | If weighted scheduling becomes required, the current design lacks a clear algorithm, risking inconsistent behavior when implemented later. |
| **Three‑clock interaction** | The clocks are defined as separate ports (`ClockPort`) but rule‑engine and turn‑manager both need tick events. The design does not explicitly state which component owns the tick publish/subscribe order. | Ambiguity can cause race conditions (e.g., a rule fires before the turn manager updates `actor_step`). |
| **Recursive VSM wiring** | Recursion is achieved by System 1 agents spawning a full VSM that re‑uses the same ports. The design notes “circular imports” as a risk but does not show a dependency‑injection scheme to break the cycle. | Without a clear injection pattern, Python modules may import each other at import time, leading to `ImportError` or hidden runtime bugs when nesting depth grows. |
| **Entity naming** | `Thread` is used for a VSM‑level conversation thread, which collides with `threading.Thread`. | May cause confusion in code and IDEs; a distinct name (e.g., `ConversationThread`) would be clearer. |
| **Persistence format** | YAML is chosen for all entities (events, threads, contracts). YAML is human‑readable but slower to parse and less suited for large volumes. | As the system scales, loading many events or contracts could become a bottleneck; a binary or indexed format (JSON‑Lines, SQLite) might be needed. |
| **ToolPort discovery** | `ToolPort` registers callables, but the design does not specify a discovery API (e.g., `list_tools()`) or how agents resolve a tool name to a callable. | Agents may need to validate tool existence before invoking; without a discovery method they must handle `KeyError` manually. |
| **SkillRegistry duplicate handling** | The registry loads all `*.yaml` files but no rule is defined for duplicate skill names. | Duplicate definitions could silently overwrite each other, causing nondeterministic skill availability. |
| **RulePort vs TriggerEngine** | `RulePort` manages rule objects, while `TriggerEngine` evaluates them each tick. The separation is not clearly justified. | If both ports expose similar methods (`add_rule`, `remove_rule`), developers may be unclear which to use, increasing maintenance overhead. |
| **Skipped items** | Items 20‑23 (SkillPort, SkillRegistry, SkillExecutor) and 25 (YAML persistence mapping) are still marked “skipped”. | Leaving them undone means the design is incomplete; downstream components will need those definitions before implementation can be fully validated. |

**What to address before implementation**

1. **Consolidate overlapping ports** – decide whether rule evaluation belongs to `RulePort` or `SchedulerPort` and document the ownership clearly.
2. **Add a minimal `SkillPort`** – define an interface (`register_skill`, `execute_skill`) to keep skill handling separate from generic tools.
3. **Refine `MemoryPort`** – include `delete(entry_id)` and a typed `query(filter: Callable[[Entry], bool]) -> List[Entry]`.
4. **Specify weighted turn‑manager algorithm** – define how weights are stored, updated, and applied to the round‑robin order.
5. **Clarify clock tick flow** – document that `ClockPort.tick()` publishes a `global_tick` event before/after the turn manager updates actor steps to avoid race conditions.
6. **Introduce explicit dependency injection** – e.g., a `PortContainer` passed to each VSM instance, so nested VSMs can reuse the same ports without import cycles.
7. **Rename `Thread` entity** to `ConversationThread` (or similar) to avoid confusion with Python’s threading module.
8. **Plan for persistence scaling** – keep YAML for prototyping but outline a migration path to a faster format (JSON‑Lines or SQLite).
9. **Add discovery to `ToolPort`** – a `list_tools() -> List[str]` method helps agents validate tool names.
10. **Define duplicate‑skill handling** – e.g., raise an error on duplicate names or allow explicit overriding with a priority flag.
11. **Merge `RulePort` and `TriggerEngine` concepts** if they serve the same purpose, or clearly separate rule storage (`RulePort`) from rule execution (`TriggerEngine`).

Addressing these points will tighten the design, reduce future refactoring, and give a solid contract surface for the concrete code you’ll generate next.
