# Item 10 – Coupling analysis

**Critical coupling review – Item 10**

Below is a concise analysis of the ports defined in the design (step 1 & 2) and the concrete adapters listed in the SBOM.  The goal is to spot any *hard* dependencies that would make swapping a port or its adapter painful later on.

---

### 1. Current port definitions (from *step 1 & 2*)

| Port | Minimal API (step 2 2) | Primary responsibilities |
|------|------------------------|--------------------------|
| **EventBusPort** | `publish(event)`<br>`subscribe(event_type, handler)` | Pub/sub backbone for all components |
| **PersistencePort** | `read(path) → str`<br>`write(path, content)`<br>`list_dir(path) → List[str]` | Simple file‑based storage |
| **LLMPort** | `generate(prompt, **kwargs) → str` | LLM access |
| **ToolPort** | `execute(tool_name, **kwargs) → Any` | External‑tool registry |
| **SchedulerPort** | `schedule(callback, delay)`<br>`cancel(job_id)` | Timer / trigger service |
| **ConfigPort** | `get(key) → Any`<br>`set(key, value)` | Config lookup |
| **RulePort** | `add_rule(rule)`<br>`remove_rule(rule_id)`<br>`list_rules() → List[Rule]` | Dynamic rule management |
| **TurnManagerPort** | `add_actor(actor_id)`<br>`remove_actor(actor_id)`<br>`next_actor() → Optional[str]` | Round‑robin (or hierarchical) scheduling |
| **MemoryPort** | `append(entry)`<br>`load_all() → List[Entry]`<br>`query(**filters) → List[Entry]` | Per‑agent observation log |

---

### 2. Concrete adapters (SBOM)

| Port | Adapter(s) |
|------|------------|
| EventBusPort | `InProcessBus` (queue‑based) |
| PersistencePort | `YamlFileStore` (writes YAML under `data/`) |
| LLMPort | `LocalLLMAdapter` (LangChain wrapper) |
| ToolPort | `LocalToolRegistry` (Python callables) |
| SchedulerPort | `SimpleTriggerEngine` (loop‑based rule scheduler) |
| ConfigPort | `YamlConfigLoader` |
| RulePort | `YamlRuleAdapter` |
| TurnManagerPort | `InMemoryTurnManager` (simple) <br>`HierarchicalTurnManager` (nested) |
| MemoryPort | `YamlMemoryAdapter` |

---

### 3. Observed coupling patterns

| Coupling | Where it appears | Why it can be problematic |
|----------|------------------|---------------------------|
| **SchedulerPort → EventBusPort** | `SimpleTriggerEngine` emits a `global_tick` event (`ev.bus.publish(...)`) inside its rule definitions (see step 1 lines 340‑349). | The scheduler is *hard‑wired* to an event‑bus implementation. If we later want a scheduler that pushes ticks via a callback rather than publishing to the bus, we must modify the adapter (or the port) and all code that expects the bus‑publish side‑effect. |
| **TurnManagerPort ↔ EventBusPort** | The root turn‑manager *consumes* `global_tick` events (step 1 line 432) to generate its own `turn_tick`. | The turn‑manager relies on the existence of a bus and on a specific event type. Swapping the bus for another transport (e.g., Redis Streams) will require the turn‑manager to know the exact event payload format. |
| **TurnManagerPort ↔ PersistencePort** | Turn‑manager saves `actor_order` on shutdown (step 1 line 433). | This is a *runtime* dependency; if we replace the persistence mechanism (e.g., move from YAML files to a DB) the turn‑manager must be updated to use the new port’s API. |
| **MemoryPort ↔ PersistencePort** (implicit) | `YamlMemoryAdapter` writes per‑agent logs to YAML files – it internally uses the same file‑IO primitives as `YamlFileStore`. | Sharing the same underlying file store can cause contention or make it harder to replace one without affecting the other. |
| **RulePort ↔ EventBusPort** | `YamlRuleAdapter` may publish rule‑change events (`rule_added`, `rule_removed`) on the bus (see step 1 lines 357‑360). | Ties rule management to a specific bus implementation; a future rule store that pushes changes via callbacks would need a different adapter. |

---

### 4. Recommendations to reduce coupling

1. **Make SchedulerPort explicitly own its event‑bus dependency**  
   *Add an optional constructor argument* `event_bus: EventBusPort | None`.  
   - If supplied, `schedule` can publish `tick` events.  
   - If not, the scheduler can expose a `tick()` method that returns the scheduled callbacks directly.  
   This isolates the *publish* behavior from the *timing* behavior.

2. **TurnManagerPort should accept a *tick source* rather than hard‑coding the event name**  
   - Define `set_tick_source(source: Callable[[], Any])` or simply `on_tick(callback)`.  
   - The current implementation can still subscribe to `global_tick` on the bus, but a future implementation could use a direct callback from a different scheduler.

3. **Persisted state handling**  
   - Extract the *save/load* responsibility into a small `StatefulPort` interface (e.g., `save_state(state: dict)` / `load_state() -> dict`).  
   - TurnManagerPort and MemoryPort would implement this interface, allowing any persistence backend (YAML, SQLite, etc.) to be swapped without touching the ports.

4. **Separate “event publishing” from “state mutation” in adapters**  
   - For `YamlRuleAdapter` and `YamlFileStore`, keep the file‑IO logic pure and add a thin wrapper that injects an `EventBusPort` only if the caller wants notifications.  
   - This makes the adapters reusable in non‑event‑bus contexts (e.g., unit tests that only need file IO).

5. **Document the dependency direction in the SBOM**  
   - Add a column “Depends on” so future reviewers can see that `SimpleTriggerEngine → EventBusPort` and `InMemoryTurnManager → PersistencePort`.  
   - This will surface coupling early when new ports/adapters are added.

---

### 5. Quick impact check

| Port | Current coupling | Change needed for a swap |
|------|------------------|--------------------------|
| **SchedulerPort** | Hard‑coded `event_bus.publish` | Add optional `event_bus` injection; expose a pure callback API |
| **TurnManagerPort** | Listens to `global_tick` on bus, saves via PersistencePort | Refactor to accept a tick *callback* and a generic `state_port` interface |
| **MemoryPort** | Uses `YamlMemoryAdapter` that writes files | Replace with `JsonMemoryAdapter` that implements same `MemoryPort` methods – no change to callers |
| **RulePort** | Emits rule‑change events on bus | Wrap rule‑change notification in a separate `RuleNotifierPort` if needed |

These refactors are **small** (add a constructor argument and a couple of methods) and keep the public API unchanged for existing code, satisfying the “minimal change” principle.

---

### 6. Summary

* The main coupling to watch is **SchedulerPort → EventBusPort** (via `SimpleTriggerEngine`).
* Turn‑manager also couples to the bus and to persistence.
* By making the dependencies *explicit* (constructor‑injection) and by separating “state persistence” from “event publishing”, future swaps of adapters or underlying technologies will require only the adapter implementation, not the port interfaces themselves.

When you are ready, the next step can be to implement the small constructor changes in `adapters/simple_trigger_engine.py` and `adapters/turn_manager.py`, or simply note them for a later iteration.
