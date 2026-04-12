# Implementation Roadmap – VSM LLM‑Agent Framework

## Goal
Create a reusable, hexagonal‑architecture based LLM‑agent system that implements the Viable System Model (VSM) with recursion, event‑driven rule engine, and turn‑manager scheduling.

## High‑Level Phases
| Phase | Duration (approx.) | Focus |
|------|-------------------|-------|
| **0 Prep** | 1 day | Align on PRD, set up repo, install dependencies. |
| **1 Core Architecture** | 3 days | Implement ports & adapters (EventBus, Persistence, LLM, Tool, Scheduler). |
| **2 Agents & VSM Skeleton** | 4 days | Build MGMT‑5/4/3, OPS‑1/2 agents, `VSM` class wiring, round‑robin turn manager. |
| **3 Rule Engine** | 3 days | Implement `ReactiveEngine`, rule DSL, YAML persistence, integrate with three‑clock model. |
| **4 Recursion Support** | 3 days | Add `System3.spawn_system1()` logic, nested VSM instantiation, shared ports handling. |
| **5 Persistence & Logging** | 2 days | YAML file stores for agents, events, turn order, and memory logs. |
| **6 Testing & CI** | 2 days | Unit tests for ports, agents, rule engine, turn manager; add CI step to run them. |
| **7 Demo & Documentation** | 2 days | `demo.py` showing two‑level recursion, sample contracts, and rule‑driven scheduling; update README. |
| **8 Polish & Refactor** | 1 day | Code cleanup, type hints, lint fixes. |

## Detailed Task Breakdown
### Phase 0 – Prep
- Verify Python 3.11 environment.
- Install required packages (`uv`, `langchain`, `ruamel.yaml`).
- Pull latest PRD (`VSM_PRD.md`).

### Phase 1 – Core Architecture
- **Ports**: create abstract base classes in `ports/` for EventBus, Persistence, LLM, Tool, Scheduler, Config.
- **Adapters**: implement concrete classes in `adapters/` (e.g., `InProcessBus`, `YamlFileStore`, `LocalLLMAdapter`).
- Add simple factory (`PortFactory`) to instantiate default adapters.

### Phase 2 – Agents & VSM Skeleton
- Define `AgentBase` with `id`, `ports` reference, `run()` stub.
- Implement MGMT‑5, MGMT‑4, MGMT‑3, OPS‑1, OPS‑2 classes inheriting `AgentBase`.
- Build `VSM` class that:
  - Instantiates agents.
  - Registers them with the turn manager.
  - Holds shared ports.
- Implement round‑robin `InMemoryTurnManager` (from step_2_1_working.md).

### Phase 3 – Rule Engine
- Add `Event` and `Rule` dataclasses (from step_1_working.md).
- Implement `ReactiveEngine` that registers rules, compiles conditions, and handles events.
- YAML rule loader (`config/rules.yaml`).
- Provide example rules for global tick heartbeat and report handling.

### Phase 4 – Recursion Support
- Extend `System3` (MGMT‑3) with `spawn_system1()` that:
  - Instantiates a new `VSM` object.
  - Passes shared ports.
  - Calls `start()` on the child VSM.
- Update turn manager to include newly spawned agents (flat `actor_order`).
- Add heuristic `maybe_spawn_nested_vsm` (complexity score > threshold) as shown in step_1_working.md.

### Phase 5 – Persistence & Logging
- Use `YamlFileStore` to persist:
  - Agent state (`agents/{id}.yaml`).
  - Event log (`events.yaml`).
  - Turn order (`turn_order.yaml`).
- Implement `MemoryPort` with YAML logs for each agent.

### Phase 6 – Testing & CI
- Write unit tests for:
  - Port adapters (bus publish/subscribe, file store read/write).
  - Agent creation and turn manager ordering.
  - Rule registration, condition evaluation, and action execution.
  - Recursion flow – ensure nested VSM agents appear in turn order.
- Add a GitHub Actions workflow (`.github/workflows/ci.yml`) to run `uv run pytest`.

### Phase 7 – Demo & Docs
- `demo.py` script:
  1. Build a top‑level VSM.
  2. Create a contract that forces a System 1 to spawn a nested VSM.
  3. Run the scheduler for 10 global steps, printing events and turn order.
- Update `README.md` with architecture diagram and usage steps.

### Phase 8 – Polish & Refactor
- Add type hints throughout.
- Run `ruff`/`black` for formatting.
- Ensure all imports are absolute and ports are only referenced via interfaces.

## Milestones
- **M1 (Day 2)** – Core ports & adapters compiled.
- **M2 (Day 5)** – Agents and turn manager functional.
- **M3 (Day 8)** – Rule engine integrated with clocks.
- **M4 (Day 11)** – Recursion demo works.
- **M5 (Day 13)** – CI passes, demo script ready.
- **M6 (Day 15)** – Documentation and final polish.

## Risks & Mitigations
- **Port leakage** – Ensure core modules import only abstract ports; run a grep for concrete adapter names.
- **Rule performance** – Compile condition once; limit number of listeners per event type.
- **Recursion depth** – Use shared ports to avoid duplicate resources; monitor memory usage in tests.

## Next Steps
1. Add the roadmap file to the repo.
2. Open a PR and assign reviewers.
3. Begin Phase 0 by installing dependencies.
