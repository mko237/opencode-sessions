**Code‑vs‑design review**

| Area | Design reference | Code artifact | Alignment / gap |
|------|------------------|---------------|-----------------|
| **Ports (hexagonal contracts)** | `step_2_2_working.md` – lists 9 ports | `vsm/ports/*.py` – all 9 contracts exist as `Protocol`s (EventBusPort, PersistencePort, LLMPort, ToolPort, SchedulerPort, ConfigPort, RulePort, TurnManagerPort, MemoryPort) | ✅ 100 % match |
| **ClockPort** | `step_2_3_working.md` – draft protocol; `sbom.potential.md` – listed under ports; `design_docs/architecture_layers.md` – mentions `ClockPort` | No `ClockPort` file in `vsm/ports/` and no concrete implementation in `core/` | ❌ missing – needs a `clock_port.py` (or add to `vsm/ports/`) and a concrete `SimpleClock` (e.g. `core/time.py`) |
| **Adapters** | `step_2_2_working.md` – concrete adapters for each port | `vsm/adapters/` contains `InProcessBus`, `YamlFileStore`, `LocalLLMAdapter`, `LocalToolRegistry`, `SimpleTriggerEngine`, `YamlConfigLoader`, `YamlRuleAdapter`, `InMemoryTurnManager`, `YamlMemoryAdapter` | ✅ all adapters present and wired in `PortFactory` |
| **PortFactory** | `step_2_2_working.md` – “wire adapters together” | `vsm/ports/port_factory.py` – creates a `PortFactory` that instantiates every adapter and exposes a `create()` dict | ✅ matches design |
| **Turn‑manager implementation** | `step_2_2_working.md` – O(1) add/remove/next; `step_2_3_working.md` – scalability assessment | `vsm/adapters/in_memory_turn_manager.py` – O(1 `add_actor`/`next_actor`; `remove_actor` uses list.remove (O(n)) but acceptable for modest actor counts | ✅ largely aligns; removal could be O(1) if a dict+list were used, but not a blocker |
| **RulePort & adapter** | `step_2_2_working.md` – CRUD for rules | `vsm/ports/rule_port.py` (Protocol) + `vsm/adapters/yaml_rule_adapter.py` (YAML storage) | ✅ matches |
| **MemoryPort & adapter** | `step_2_2_working.md` – per‑agent log | `vsm/ports/memory_port.py` + `vsm/adapters/yaml_memory_adapter.py` | ✅ matches |
| **SBOM** | `design_docs/sbom.potential.md` – lists ports, includes `ClockPort` | No code for `ClockPort` yet, but the SBOM entry is already present | ✅ SBOM reflects intended design; implementation still pending |
| **Roadmap diagram** | `design_docs/ROADMAP.md` – table of ports | Diagram lists the 9 ports, not `ClockPort` | ❌ update roadmap to include `ClockPort` for consistency |
| **Event class** | `step_2_3_working.md` ClockPort draft imports `core.event.Event` | No `core/event.py` or similar module in the repo | ❌ missing concrete `Event` type; currently only the protocol `EventBusPort` is defined. Adding a minimal `Event` dataclass would close the gap. |

### Summary of findings
1. **Port definitions** are fully implemented and match the design list.
2. **Adapters** exist for every defined port; `PortFactory` wires them correctly.
3. **ClockPort** is the only port defined in the design but absent from the codebase; a new protocol file (e.g. `vsm/ports/clock_port.py`) and a simple implementation (`core/time.py` → `SimpleClock`) should be added.
4. **Event dataclass** referenced by the ClockPort draft is not present; creating `core/event.py` with a lightweight `Event` class (type, payload, timestamp) would satisfy the import.
5. **Roadmap & step‑1 diagram** should be updated to list `ClockPort` alongside the other ports for visual consistency.
6. **Turn‑manager removal** is O(n) due to list.remove; acceptable for now, but could be made O(1) by storing a dict of indices (as done in the SBOM description). Not a functional issue yet.
7. Overall, the codebase implements the hexagonal architecture as described, with the only missing pieces being the three‑clock abstraction and its supporting `Event` type.

### Next steps (if you want to close the gaps)
- Add `vsm/ports/clock_port.py` containing the `ClockPort` protocol from the draft.
- Add `core/time.py` with a `SimpleClock` class that implements the protocol and publishes `global_tick` events via the existing `EventBusPort`.
- Add `core/event.py` defining a simple `Event` dataclass (type, payload, timestamp) used by the clock and other components.
- Update `design_docs/ROADMAP.md` and `design_docs/step_1_working.md` diagrams to include `ClockPort`.
- Optionally, refine `InMemoryTurnManager.remove_actor` to use a dict for O(1) removal if actor counts grow large.
