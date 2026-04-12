# Epic‑Hypothesis Statements

## Epic 1 – Core Architecture
**If we** implement a hexagonal ports‑and‑adapters architecture with abstract ports (`EventBusPort`, `PersistencePort`, `LLMPort`, `ToolPort`, `SchedulerPort`, `ConfigPort`, `RulePort`, `TurnManagerPort`, `MemoryPort`) for each VSM subsystem, **then we will** achieve a reusable, interchangeable foundation that reduces integration effort and enables rapid swapping of implementations, **because** agents will depend only on contracts and adapters can be replaced without touching core logic.

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
