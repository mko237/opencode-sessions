# Epic 1 – Core Architecture PRD

## 1. Executive Summary
We need a reusable, interchangeable foundation for the VSM system. By implementing a hexagonal **ports‑and‑adapters** architecture with nine abstract ports (EventBus, Persistence, LLM, Tool, Scheduler, Config, Rule, TurnManager, Memory), we can reduce integration effort and enable rapid swapping of implementations. This will accelerate future feature work and lower the cognitive load for agents that depend on these contracts.

## 2. Problem Statement
**Who:** Platform engineers and VSM agent developers.

**Problem:** Current VSM code tightly couples agents to concrete implementations (e.g., hard‑coded event bus, in‑memory persistence). This makes swapping components painful, forces duplicated code across agents, and slows onboarding of new adapters.

**Why it matters:** Integration effort for each new agent or adapter takes days, leading to missed delivery dates and higher maintenance cost. Engineers spend time refactoring rather than delivering value.

**Evidence:** 
- Multiple PRs (e.g., `demo.py`, `VSM` wiring) show duplicated adapter code.
- Team retrospectives cite “hard to replace the event bus” as a blocker.
- No documented port contracts exist; new contributors must read source to infer interfaces.

## 3. Target Users & Personas
**Primary Persona – Platform Engineer Priya**
- **Role:** Engineer building and maintaining the VSM core library.
- **Goals:** Add new adapters quickly, keep agent code clean, ensure testability.
- **Pain points:** Unclear contracts, duplicated boilerplate, difficulty swapping implementations.
- **Quote:** “I spend half a day just figuring out how to hook my new agent into the existing event system.”

**Secondary Persona – Agent Developer Alex**
- **Role:** Developer writing a new agent (e.g., `LLMAgent`).
- **Goals:** Focus on business logic, not on wiring ports.
- **Pain points:** Need to stub multiple ports manually, unclear naming conventions.

## 4. Strategic Context
- **Business goal:** Reduce time‑to‑integrate new VSM subsystems from 5 days to <1 day (Q2 OKR).
- **Why now:** Upcoming epics (Agents & VSM Skeleton, Rule Engine) depend on stable contracts; delays are already impacting the roadmap.
- **Market signal:** Hexagonal architecture is a proven pattern for modular systems, improving scalability and testability.

## 5. Solution Overview
We will define **abstract port interfaces** for each subsystem and implement **concrete adapters** that satisfy those contracts. The ports are:
- `EventBusPort`
- `PersistencePort`
- `LLMPort`
- `ToolPort`
- `SchedulerPort`
- `ConfigPort`
- `RulePort`
- `TurnManagerPort`
- `MemoryPort`

Each port will be a Python `Protocol` (or abstract base class) exposing minimal methods. Concrete adapters (e.g., `InProcessBus`, `YamlFileStore`) will implement these protocols. A `PortFactory` will provide a single injection point for VSM initialization.

## 6. Success Metrics
| Metric | Current | Target | Measurement |
|--------|---------|--------|-------------|
| **Port contract coverage** | 0 % (no contracts) | 100 % (all 9 ports defined) | Count of `Protocol` definitions vs. target list |
| **Adapter test coverage** | 0 % | ≥ 80 % unit‑test coverage per adapter | `pytest --cov` report |
| **Integration time** | ~5 days per new adapter | ≤ 1 day | Time logged in issue workflow |
| **Documentation completeness** | None | README‑ports.md with diagram | Presence of file & link in PRD |

## 7. User Stories & Requirements
### Epic Hypothesis
> **If we** implement a hexagonal ports‑and‑adapters architecture with abstract ports (`EventBusPort`, `PersistencePort`, `LLMPort`, `ToolPort`, `SchedulerPort`, `ConfigPort`, `RulePort`, `TurnManagerPort`, `MemoryPort`) for each VSM subsystem, **then we will** achieve a reusable, interchangeable foundation that reduces integration effort and enables rapid swapping of implementations, **because** agents will depend only on contracts and adapters can be replaced without touching core logic.

#### User Story 1 – Define abstract port contracts
- **As a** platform engineer
- **I want to** have a `Protocol` for each subsystem (e.g., `EventBusPort` with `publish(event)` / `subscribe(event_type, handler)`)
- **so that** all agents can type‑check against a stable interface.

**Acceptance Criteria**
- **Scenario:** Port contracts exist
  - **Given** the repository root
  - **When** I list files in `src/ports`
  - **Then** I see nine `Protocol` definitions matching the list above

#### User Story 2 – Implement concrete adapters for R1
- **As a** platform engineer
- **I want to** provide concrete implementations (`InProcessBus`, `YamlFileStore`, `LocalLLMAdapter`, etc.) that satisfy the ports
- **so that** developers can plug them in without writing boilerplate.

**Acceptance Criteria**
- **Scenario:** In‑process event bus works
  - **Given** `InProcessBus` is instantiated
  - **When** a listener subscribes to `TestEvent`
  - **And** `publish(TestEvent())` is called
  - **Then** the listener receives the event

#### User Story 3 – Add unit tests for each adapter
- **As a** platform engineer
- **I want to** have pytest tests that verify each adapter implements its port methods correctly
- **so that** regressions are caught early.

**Acceptance Criteria**
- **Scenario:** `YamlFileStore` round‑trip
  - **Given** a temporary directory
  - **When** I `save('key', {'a': 1})` and then `load('key')`
  - **Then** the loaded object equals the original

#### User Story 4 – Document port contracts
- **As a** platform engineer
- **I want to** create `README-ports.md` with a diagram and usage examples
- **so that** new contributors can understand the architecture quickly.

**Acceptance Criteria**
- **Scenario:** Documentation is complete
  - **Given** the PRD is merged
  - **When** I open `README-ports.md`
  - **Then** I see a table of ports, method signatures, and a Mermaid diagram of dependencies

#### User Story 5 – Provide `PortFactory` for injection
- **As a** developer building a VSM instance
- **I want to** call `PortFactory.create()` to get all adapters pre‑wired
- **so that** I can instantiate `VSM` with a single line of code.

**Acceptance Criteria**
- **Scenario:** Factory returns ready‑to‑use adapters
  - **Given** I call `PortFactory()`
  - **When** I request `event_bus`
  - **Then** I receive an instance of `InProcessBus`

### Splitting notes (applied user‑story‑splitting)
- Story 1 covers contract definition (single focus).
- Story 2 covers adapter implementation (multiple adapters but grouped as a single logical effort for R1).
- If needed, Story 2 can be split by adapter type using the "Data variations" pattern (e.g., separate stories for `EventBusPort` adapter, `PersistencePort` adapter, etc.). For now we keep it as one story because each adapter is small and can be delivered together.

## 7. Delivery Slices (Release Plan & Tasks)

### Backbone Activities (User‑level view)

| Release | Activity |
|--------|----------|
| **R1** | Define abstract port contracts (EventBus, Persistence, LLM, Tool, Scheduler, Config, Rule, TurnManager, Memory) |
| **R1** | Implement concrete adapters (`InProcessBus`, `YamlFileStore`, `LocalLLMAdapter`, `LocalToolRegistry`, `SimpleTriggerEngine`) |
| **R2** | Wire ports into a `PortFactory` for easy injection |
| **R2** | Add unit tests for each adapter |
| **R3** | Document port contracts in `README-ports.md` (table + Mermaid diagram) |

### Steps & Tasks (example for Activity 1)

- **Step 1.1 – List required methods for each port**  
  - Task 1.1.1 – Write `EventBusPort` interface with `publish(event)` / `subscribe(event_type, handler)`  
  - Task 1.1.2 – Write `PersistencePort` with `save(key, obj)` / `load(key)`  
  - Task 1.1.3 – Add type hints and docstrings for all ports  

- **Step 1.2 – Create concrete `InProcessBus`**  
  - Task 1.2.1 – Implement internal dict of listeners  
  - Task 1.2.2 – Add thread‑safe lock for publish/subscribe  
  - Task 1.2.3 – Write simple unit test for publish/subscribe flow  

- **Step 1.3 – Implement other adapters**  
  - Task 1.3.1 – Build `YamlFileStore` with `save`/`load` using `yaml.safe_dump`/`safe_load`  
  - Task 1.3.2 – Implement `LocalLLMAdapter` with `generate(prompt)` stub  
  - Task 1.3.3 – Create `LocalToolRegistry` exposing `list_tools()` and `run(tool_name, args)`  

- **Step 2 – Wire ports in `PortFactory`**  
  - Task 2.1 – `PortFactory.create()` instantiates each concrete adapter and returns a dict or object with ready‑to‑use ports.  

- **Step 3 – Add unit tests**  
  - Task 3.1 – Verify `InProcessBus.publish` triggers subscribed handler.  
  - Task 3.2 – Ensure `YamlFileStore.save/load` round‑trip works.  
  - Task 3.3 – Test `LocalLLMAdapter.generate` returns expected mock output.  

- **Step 4 – Documentation**  
   - Task 4.1 – Create `README-ports.md` with a table of ports, method signatures, and a Mermaid diagram of dependencies.

## 8. Reference Material Mapping

| Document | Path | Purpose |
|----------|------|---------|
| Step 1 working | `step_1_working.md` | Initial port‑contract draft and early design notes (helps define port interfaces and see early design decisions) |
| Step 2 working (various) | `step_2_1_working.md`, `step_2_2_working.md`, `step_2_3_working.md`, `step_2_4_working.md` | Detailed implementation steps for adapters and factory (guides concrete adapter creation and factory wiring) |
| Step 2 items | `step_2_2_item_8_1.md`, `step_2_2_item_10.md` | Specific sub‑tasks and decisions for individual ports (reference for port‑specific choices) |
| Step 3 working | `step_3_working.md` | Wiring of ports into `PortFactory` and integration tests (useful for final integration and test setup) |
| SBOM potential | `sbom.potential.md` | Bill‑of‑materials outline for dependencies (helps track external packages) |
| Epic hypotheses | `epic_hypotheses.md` | High‑level hypothesis statements for all epics (provides overall vision and alignment) |
| Roadmap | `ROADMAP.md` | Timeline and milestone view across releases (aids sprint and release planning) |
| VSM PRD | `VSM_PRD.md` | Complementary product requirement doc for the VSM core (gives broader VSM context) |

## 8. Out of Scope
- **Advanced adapters** (e.g., async event bus, cloud persistence) – slated for later releases.
- **Port versioning** – current design assumes a single version; future versioning strategy will be defined after R1.
- **Performance benchmarking** – not part of this epic; will be addressed in a separate performance story.

## 9. Dependencies & Risks
### Dependencies
- None external; all adapters use standard library or existing dependencies (`yaml`, `uuid`).
- Requires `src/ports/` directory to exist (will be created).

### Risks & Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| Mis‑aligned method signatures across ports | Medium | Review each port with the team before implementation; use a shared template.
| Over‑engineering (too many methods) | Low | Start with minimal required methods; iterate later.
| Incomplete test coverage | Medium | Enforce ≥ 80 % coverage threshold in CI.
| Adoption lag by agents | High | Provide a migration guide in `README-ports.md` and hold a walkthrough session.

## 10. Open Questions
- Should `EventBusPort` support async handlers now or later?
- Will `MemoryPort` be in‑memory only, or need persistence for large state?
- Do we need a versioning scheme for ports to support future breaking changes?

---
*Prepared using the `problem-statement`, `proto-persona`, `prd-development`, `user-story`, and `user-story-splitting` skills.*