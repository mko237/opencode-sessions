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
