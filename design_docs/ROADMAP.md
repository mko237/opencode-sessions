# Epic‑Hypothesis Statements

## Epic 1 – Core Architecture
**If we** implement a hexagonal ports‑and‑adapters architecture with abstract ports (`EventBusPort`, `PersistencePort`, `LLMPort`, `ToolPort`, `SchedulerPort`, `ConfigPort`, `RulePort`, `TurnManagerPort`, `MemoryPort`, `ClockPort`) for each VSM subsystem, **then we will** achieve a reusable, interchangeable foundation that reduces integration effort and enables rapid swapping of implementations, **because** agents will depend only on contracts and adapters can be replaced without touching core logic.

## Epic 2 – Agents & VSM Skeleton
**If we** build MGMT‑5/4/3 and OPS‑1/2 agents plus a `VSM` class that wires these agents together and registers them with the turn manager, **then we will** have a functional scaffold that demonstrates the VSM hierarchy and recursion capability, **because** the skeleton provides the essential plumbing and agent interfaces needed for higher‑level features.

## Epic 3 – Rule Engine
**If we** create a `ReactiveEngine` that loads YAML rule definitions, compiles conditions once, and executes actions on matching events, **then we will** enable dynamic, data‑driven behavior across the system, **because** rules can be added/removed at runtime and the engine guarantees deterministic ordering via priority.

## Epic 4 – Recursion Support
**If we** extend `System3` with `spawn_system1()` logic that instantiates a child `VSM`, shares the existing ports, and registers the child with the turn manager, **then we will** allow System 1 agents to create nested VSMs of arbitrary depth, **because** shared ports keep resource usage low and the turn manager treats child agents as regular actors.

## Epic 5 – Persistence & Logging
**If we** implement `YamlFileStore` for `PersistencePort` and a `YamlMemoryAdapter` for `MemoryPort` that write per‑agent state and observation logs to YAML files, **then we will** have durable, human‑readable storage for events, agent state, and memory, **because** YAML is easy to version‑control and inspect during debugging.

## Epic 6 – Testing & CI
**If we** write unit tests for each port adapter, agent creation, turn‑manager ordering, rule registration, and recursion flow, and add a GitHub Actions workflow to run them on each push, **then we will** ensure reliability and quick feedback on changes, **because** automated tests catch regressions early and CI enforces a passing baseline.

## Epic 7 – Demo & Documentation
**If we** create a `demo.py` script that builds a top‑level VSM, forces a System 1 to spawn a nested VSM, runs the scheduler for several steps, and prints events and turn order, and update the README with usage steps and architecture diagram, **then we will** provide a concrete example and clear onboarding material for developers, **because** a runnable demo showcases the design and documentation reduces ramp‑up time.
# Prioritization Framework Recommendation

**Based on your context:**
- **Product Stage:** Early PMF, scaling – you have found initial product‑market fit and are growing fast.
- **Team Context:** Small team (solo developer / few collaborators) – need a simple yet data‑driven method.
- **Decision‑Making Need:** Too many ideas, unclear which to pursue – you need a systematic way to filter backlog.
- **Data Availability:** Some data – basic analytics and customer feedback exist, but not extensive usage metrics.

---

## Recommended Framework: **RICE** (Reach, Impact, Confidence, Effort)

**Why this framework fits:**
1. **Matches stage:** Early‑PMF teams benefit from a balanced view of reach and impact to prioritize features that drive adoption.
2. **Fits team size:** RICE scoring can be done quickly in a spreadsheet; it doesn’t require heavy tooling.
3. **Addresses need:** Provides a clear filter for many ideas, turning a long backlog into a ranked list.
4. **Leverages available data:** You have enough analytics to estimate Reach and Impact, and confidence can be expressed as a percentage.

**When to use it:**
- Quarterly or sprint‑planning sessions when the backlog exceeds 20‑30 items.
- When you want a transparent, quantifiable ranking to share with stakeholders.

**When NOT to use it:**
- If you had **minimal data** (pre‑product) – ICE or Value/Effort would be lighter.
- For **strategic, multi‑quarter bets** where reach isn’t the primary concern – consider Opportunity Scoring or Kano.

---

## How to Implement RICE

### Step 1: Define Scoring Criteria
- **Reach:** Estimate the number of users the feature will affect per month/quarter.
- **Impact:** Rate the expected benefit (1 = minimal, 2 = high, 3 = massive).
- **Confidence:** Express confidence in your Reach/Impact estimates as a % (50 % = low data, 80 % = good data).
- **Effort:** Estimate person‑months (include design, engineering, QA).

### Step 2: Score Each Feature
- Create a shared spreadsheet (Google Sheets, Airtable, or CSV).
- Involve the small team (you and any collaborators) to assign each metric.

### Step 3: Calculate RICE Score
```
RICE = (Reach × Impact × Confidence) / Effort
```
- Higher scores = higher priority.

### Step 4: Review & Adjust
- Sort by score, discuss the top 5‑10 items with any stakeholders (e.g., a mentor or a future teammate).
- Adjust for strategic considerations that RICE doesn’t capture (e.g., “this feature is a required dependency”).

---

## Example Scoring Template

| Feature | Reach (users/quarter) | Impact (1‑3) | Confidence (%) | Effort (person‑months) | RICE Score |
|---------|----------------------|--------------|----------------|------------------------|------------|
| Core ports & adapters | 8,000 | 3 | 80% | 2 | 96,000 |
| System 1 agent skeleton | 5,000 | 2 | 70% | 1.5 | 46,667 |
| Rule engine prototype | 4,000 | 2 | 60% | 1 | 48,000 |
| Recursion support | 3,000 | 3 | 50% | 2 | 22,500 |
| Demo script & docs | 2,000 | 1 | 90% | 0.5 | 36,000 |

**Priority order (high → low):** Core ports & adapters → Rule engine → Demo script → System 1 skeleton → Recursion support.

---

## Alternative Framework (if RICE feels too heavy)

**ICE** (Impact, Confidence, Ease) – removes Reach, making scoring faster when you lack usage numbers.

**Why it might work:**
- Simpler 3‑column scoring, quicker to complete.
- Still gives a relative ranking.

**Trade‑offs:**
- No visibility into how many users benefit.
- May over‑prioritize high‑impact but low‑reach items.

---

## Common Pitfalls & How to Avoid Them

1. **Over‑weighting Effort** – Don’t drop high‑impact items just because they need more work; consider strategic importance.
2. **Inflating Confidence** – Be honest; a 90 % confidence score when you have no data misleads the ranking.
3. **Ignoring Strategy** – RICE is a tool, not a decision; adjust the list for product vision or roadmap themes.

---

## Reassess When

- Your product moves from **early‑PMF** to **mature** – you may shift to **Opportunity Scoring** or **Kano**.
- Your team grows beyond a handful of people – you might adopt a more formal scoring workshop.
- Data collection improves – you can add a more precise Reach metric.

---

**Next step:** Run the RICE scoring session with the items listed in `epic_hypotheses.md` and record the scores in a spreadsheet. Use the resulting order to prioritize the implementation phases in the roadmap.
# Delivery Slices – User Story Mapping

## Overview
Using the **user‑story‑mapping** framework, each epic from `epic_hypotheses.md` is broken into a backbone of activities, then into steps and tasks. The vertical ordering (Release 1, Release 2) creates delivery slices that guide implementation order.

---

## Epic 1 – Core Architecture
**If we** implement a hexagonal ports‑and‑adapters architecture … **then we will** achieve a reusable foundation.

### Backbone Activities (User‑level view)
| Release | Activity |
|--------|----------|
| **R1** | Define abstract port contracts (EventBus, Persistence, LLM, Tool, Scheduler, Config, Rule, TurnManager, Memory)
| **R1** | Implement concrete adapters (`InProcessBus`, `YamlFileStore`, `LocalLLMAdapter`, `LocalToolRegistry`, `SimpleTriggerEngine`)
| **R2** | Wire ports into a `PortFactory` for easy injection
| **R2** | Add unit tests for each adapter
| **R3** | Document port contracts in `README-ports.md`

### Steps & Tasks (example for Activity 1)
- **Step 1.1** – List required methods for each port
  - Task 1.1.1 – Write `EventBusPort` interface with `publish(event)` / `subscribe(event_type, handler)`
  - Task 1.1.2 – Write `PersistencePort` with `save(key, obj)` / `load(key)`
  - Task 1.1.3 – Add type hints and docstrings
- **Step 1.2** – Create concrete `InProcessBus`
  - Task 1.2.1 – Implement internal dict of listeners
  - Task 1.2.2 – Add thread‑safe lock
  - Task 1.2.3 – Write simple unit test for publish/subscribe flow

---

## Epic 2 – Agents & VSM Skeleton
**If we** build MGMT‑5/4/3 and OPS‑1/2 agents plus a `VSM` class … **then we will** have a functional scaffold.

### Backbone Activities
| Release | Activity |
|--------|----------|
| **R1** | Define `AgentBase` with `id`, `ports`, and abstract `run()` method
| **R1** | Implement MGMT‑5, MGMT‑4, MGMT‑3, OPS‑1, OPS‑2 classes inheriting `AgentBase`
| **R2** | Build `VSM` class that instantiates agents and registers them with the turn manager
| **R2** | Add a simple `run()` loop that steps through agents in round‑robin order
| **R3** | Write integration test that verifies each agent receives a tick event

### Steps & Tasks (excerpt for Activity 2)
- **Step 2.1** – Create `AgentBase`
  - Task 2.1.1 – Add `self.id = uuid4()`
  - Task 2.1.2 – Store reference to `self.ports`
  - Task 2.1.3 – Declare abstract `run(self, context)` method
- **Step 2.2** – Implement `MGMT5Agent`
  - Task 2.2.1 – Define `run` to evaluate strategic goals
  - Task 2.2.2 – Subscribe to `global_tick` via `EventBusPort`
- **Step 2.3** – Wire agents in `VSM.__init__`
  - Task 2.3.1 – Instantiate each agent with shared ports
  - Task 2.3.2 – Register agents with `TurnManagerPort`

---

## Epic 3 – Rule Engine
**If we** create a `ReactiveEngine` … **then we will** enable dynamic, data‑driven behavior.

### Backbone Activities
| Release | Activity |
|--------|----------|
| **R1** | Design `Rule` and `Event` dataclasses
| **R1** | Implement `ReactiveEngine.register_rule(rule_yaml_path)`
| **R2** | Build YAML loader that validates rule schema
| **R2** | Add priority ordering for rule execution
| **R3** | Create example rule set (`rules.yaml`) for global tick and contract handling
| **R3** | Write unit tests for condition evaluation and action dispatch

### Steps & Tasks (excerpt)
- **Step 3.1** – Define `Rule` fields (`name`, `condition`, `action`, `priority`)
  - Task 3.1.1 – Use `ruamel.yaml` for safe loading
  - Task 3.1.2 – Implement `Rule.matches(event)` method
- **Step 3.2** – Implement `ReactiveEngine.evaluate(event)`
  - Task 3.2.1 – Iterate rules sorted by priority
  - Task 3.2.2 – Call `action(event)` when condition true

---

## Epic 4 – Recursion Support
**If we** extend `System3` with `spawn_system1()` … **then we will** allow nested VSMs.

### Backbone Activities
| Release | Activity |
|--------|----------|
| **R1** | Add `System3.spawn_system1(self, config)` method
| **R1** | Ensure shared ports are passed to child `VSM`
| **R2** | Update `TurnManagerPort` to accept dynamic agent registration at runtime
| **R2** | Write integration test that spawns a child VSM and verifies its agents appear in the turn order
| **R3** | Document recursion flow in `README-recursion.md`

### Steps & Tasks (excerpt)
- **Step 4.1** – Implement `spawn_system1`
  - Task 4.1.1 – Create new `VSM` instance with `self.ports`
  - Task 4.1.2 – Call `child_vsm.start()` to initialize agents
- **Step 4.2** – Extend `InMemoryTurnManager.add_agent(agent)` to handle runtime additions
  - Task 4.2.1 – Append to `self.actor_order`
  - Task 4.2.2 – Ensure `next_actor` accounts for new agents

---

## Epic 5 – Persistence & Logging
**If we** implement `YamlFileStore` and `YamlMemoryAdapter` … **then we will** have durable, human‑readable storage.

### Backbone Activities
| Release | Activity |
|--------|----------|
| **R1** – Implement `YamlFileStore.save(key, obj)` and `load(key)`
| **R1** – Implement `YamlMemoryAdapter.append(entry)` and `load_all()`
| **R2** – Add file‑locking to avoid concurrent writes
| **R2** – Write unit tests for read/write integrity
| **R3** – Add logging of every event to `events.yaml`

### Steps & Tasks (excerpt)
- **Step 5.1** – Create `YamlFileStore`
  - Task 5.1.1 – Use `Path` for base directory
  - Task 5.1.2 – Serialize objects with `yaml.safe_dump`
- **Step 5.2** – Implement `YamlMemoryAdapter`
  - Task 5.2.1 – Append JSON‑serializable dict per observation
  - Task 5.2.2 – Provide `query(filter_fn)` method for later retrieval

---

## Epic 6 – Testing & CI
**If we** write unit tests … **then we will** ensure reliability.

### Backbone Activities
| Release | Activity |
|--------|----------|
| **R1** – Add `tests/` folder with modules for ports, agents, rule engine, recursion
| **R1** – Write pytest fixtures for shared ports
| **R2** – Create GitHub Actions workflow (`.github/workflows/ci.yml`) that runs `uv run pytest`
| **R2** – Add coverage report step
| **R3** – Add linting (`ruff`) and formatting (`black`) steps

### Steps & Tasks (excerpt)
- **Step 6.1** – Write `test_ports.py`
  - Task 6.1.1 – Verify `InProcessBus.publish` triggers subscribed handler
  - Task 6.1.2 – Ensure `YamlFileStore.save/load` round‑trip works
- **Step 6.2** – Write `test_recursion.py`
  - Task 6.2.1 – Spawn child VSM and assert child agents receive ticks

---

## Epic 7 – Demo & Documentation
**If we** create a `demo.py` script … **then we will** provide a concrete example.

### Backbone Activities
| Release | Activity |
|--------|----------|
| **R1** – Write `demo.py` that builds top‑level VSM, spawns a child, runs scheduler for 10 steps, prints events & turn order
| **R1** – Update `README.md` with architecture diagram (SVG) and usage instructions
| **R2** – Add a short video GIF of the demo output
| **R2** – Publish `demo.py` in the repo root and tag a release

### Steps & Tasks (excerpt)
- **Step 7.1** – Implement demo script
  - Task 7.1.1 – Instantiate `PortFactory` and create `VSM`
  - Task 7.1.2 – Call `vsm.start()` then loop `for i in range(10): vsm.tick()`
  - Task 7.1.3 – Print `vsm.turn_manager.order` after each tick
- **Step 7.2** – Add diagram to `README.md`
  - Task 7.2.1 – Generate PNG/SVG from `architecture.drawio`
  - Task 7.2.2 – Write a quick start section with `python demo.py`

---

## Summary of Delivery Slices
- **Slice 1 (R1)** – Core ports, basic agents, rule engine skeleton, persistence adapters, first tests.
- **Slice 2 (R2)** – Full VSM wiring, recursion support, expanded test suite, CI pipeline.
- **Slice 3 (R3)** – Documentation, demo script, final polishing.

Use this map to plan sprint goals or quarterly milestones.
