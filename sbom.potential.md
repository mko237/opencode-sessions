# SBOM‑like Bill of Materials

**Purpose** – List the architectural components identified in the design documents (`request2.md`, `VSM_PRD.md`, `review.todo.md`, `Step_1_working.md`). This serves as a lightweight SBOM for the VSM‑LLM prototype.

---

## 1. Core Domain Agents

- **MGMT‑5** – Policy decision agent
- **MGMT‑4** – Strategic foresight agent
- **MGMT‑3** – Operations & control agent (spawns System 1 agents)
- **OPS‑1** – Primary functional agent (e.g., read‑email, web‑research)
- **OPS‑2** – Information‑channel coordination agent
- **System 1** – Functional agent instance (can host a nested VSM)

## 2. Ports (hexagonal interfaces)

- `EventBusPort`
- `PersistencePort`
- `LLMPort`
- `ToolPort`
- `SchedulerPort`
- `ConfigPort`
- `RulePort`
- `TurnManagerPort`
- `MemoryPort`
- `ClockPort`

## 3. Concrete Adapters (implementations of the ports)

| Port | Adapter |
|------|---------|
| `EventBusPort` | `InProcessBus` (singleton in‑process `queue.Queue` implementation) |
| `PersistencePort` | `YamlFileStore` (writes YAML files under `data/`) |
| `LLMPort` | `LocalLLMAdapter` (LangChain wrapper around a local LLM) |
| `ToolPort` | `LocalToolRegistry` (registry of Python callables) |
| `SchedulerPort` | `SimpleTriggerEngine` (loop‑based rule scheduler) |
| `ConfigPort` | `YamlConfigLoader` |
| `RulePort` | `YamlRuleAdapter` (persists rules in `config/rules.yaml`) |
| `TurnManagerPort` | `InMemoryTurnManager` (basic round‑robin) |
| `TurnManagerPort` (hierarchical) | `HierarchicalTurnManager` (manages sub‑managers for nested VSMs) |
| `MemoryPort` | `YamlMemoryAdapter` (per‑agent YAML log) |
| `ClockPort` | `SimpleClock` (singleton, see step_2_3_working.md, Item 12 section ) |

## 4. Runtime Engines / Services

- **ReactiveEngine** – event‑driven rule engine that registers `Rule` objects and dispatches them on events.
- **TriggerEngine** – evaluates time‑based rules (e.g., every N global steps) and emits `global_tick` events.
- **Turn‑manager** – round‑robin scheduler for agents; hierarchical version interleaves sub‑managers.

## 5. Data Model Entities (persisted via `PersistencePort`)

- `Event` (type, payload, timestamp)
- `Thread` (id, participants, messages, status)
- `Contract` (id, sys1_id, budget, expected_output, deadline, status)
- `Report` (sys1_id, metrics, timestamp)
- `Strategy` (id, focus_areas, priority, timestamp)
- `Policy` (id, name, value)

## 6. Supporting Utilities

- `Rule` dataclass (id, on, when, priority, action)
- `RuleValidator` – validates rule schema and compiles conditions.
- `RuleManager` – façade that updates both the `RulePort` and the reactive engine.
- `Skill` registry (YAML files under `skills/`) – not a core component yet but part of the extensibility plan.

---

*Generated from the design documents as of 2026‑04‑08.*
