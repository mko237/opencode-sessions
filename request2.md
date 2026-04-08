📦 VSM‑LLM System – “Request for Design”
(a concise, structured spec that will become the basis of the PRD)

1. Purpose & Vision
Item	Description
Goal	Build a single‑process prototype that uses LLM agents to implement Stafford Beer’s Viable System Model (VSM). The prototype must be able to read daily inputs (email, journal, URLs, video links), run the VSM recursion, and produce a report + suggestions. All components must be plug‑and‑play (ports & adapters) so they can later be swapped for micro‑services, DBs, event buses, etc.
Success criteria	1. The system can ingest at least three distinct input types (e‑mail, journal entry, URL) and trigger the appropriate System 1 agents.
2. System 3 can negotiate a contract with each System 1 and later measure compliance.
3. System 4 and System 3 exchange at least one coordination message per VSM cycle.
4. The whole prototype runs as a single Python process and can be split into separate services with minimal code change.
Future‑proofing	All I/O, persistence, and event‑bus layers are defined as abstract interfaces (ports). Concrete adapters (YAML files, Redis streams, SQLite, etc.) will be added later without touching the core logic.
2. Core Actors & Boundaries
text

+-------------------+          +-------------------+
|   USER (Miko)    |  CLI/UI  |   ENVIRONMENT     |
|  (real person)    | <------> | (emails, journal, |
|                   |          |  URLs, videos)    |
+-------------------+          +-------------------+

    ^                               ^
    |                               |
    |  internal event bus (in‑process)  |
    v                               v

+---------------------------------------------------+
|                VSM PROCESS (single process)     |
|                                                   |
|  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐ |
|  │ System 5    │   │ System 4    │   │ System 3    │ |
|  │ (Policy)   │   │ (Strategy) │   │ (Ops‑Ctrl) │ |
|  └─────▲───────┘   └─────▲───────┘   └─────▲───────┘ |
|        │                 │                 │       |
|        │   coordination  │   contracts     │       |
|        │   messages      │   & reports     │       |
|  ┌─────▼───────┐   ┌─────▼───────┐   ┌─────▼───────┐ |
|  │ System 2    │   │ System 1‑n │   │ System 1   │ |
|  │ (Channel)   │   │ (Recursive)│   │ (Agent)    │ |
|  └─────────────┘   └─────────────┘   └─────────────┘ |
+---------------------------------------------------+
Real actors – the user (you) and the environment (email, journal, URLs).
Simulated actors – System 1‑5 agents (LLM‑driven). Each System 1 instance is a single functional agent (e.g., “Read‑email”, “Web‑research”, “Journal‑summary”).
3. Functional Requirements
3.1 System 1 – Functional Agents
Requirement	Detail
Creation	System 3 decides how many System 1 agents to spin up (based on workload & reports).
Recursion	Each System 1 can contain its own VSM (5‑subsystems) if the activity is complex (e.g., “Web‑research” may need its own System 2 coordination).
Contract	System 3 ↔ System 1 negotiate a contract (resource budget ↔ expected output). Contract is stored as a YAML file and referenced by both sides.
Reporting	System 1 emits periodic status events (ReportEvent) that System 3 consumes to evaluate compliance.
Thread lifecycle	Each System 1 ↔ System 3 conversation lives in a Thread object; when the contract is fulfilled or cancelled the thread is archived (YAML dump).
3.2 System 3 – Operations & Control
Requirement	Detail
Negotiation	Initiates contract creation, sends ContractProposal → System 1, receives ContractAck.
Monitoring	Subscribes to ReportEvents from all System 1 agents; aggregates into a System 3 Dashboard (JSON for now).
Feedback loop	If a System 1 misses its target, System 3 can re‑allocate resources (adjust contract) or spawn new System 1 agents.
Coordination with System 4	Sends StrategyUpdate events (e.g., “focus on web‑research next day”) and receives StrategyAck.
Persistence	Stores contracts, reports, and thread logs in a generic PersistencePort (YAML now).
3.3 System 4 – Strategy
Requirement	Detail
Environment scan	Consumes external events (new email arrived, new URL posted) via ExternalBusPort.
Strategic output	Emits StrategyProposal (what to prioritize) to System 3.
Bidirectional sync	Periodically sends a heartbeat to System 3 to confirm alignment.
3.4 System 2 – Information Channels
Requirement	Detail
Channel registry	Provides a publish/subscribe API for any system to create a new “topic”.
Dynamic topics	System 1 can create its own topic (e.g., sys1-<id>-events).
Routing	Guarantees FIFO per‑topic (simple Python queue.Queue).
3.5 System 5 – Policy (future)
Requirement	Detail
Policy definition	Holds high‑level policies (e.g., “max 5 System 1 agents”).
Policy broadcast	Emits PolicyUpdate events that System 3 and System 2 listen to.
Extensible	Not used in the MVP but defined as a port‑ready component.
4. Data Model (abstract – concrete adapters later)
Entity	Core fields (YAML/JSON)	Remarks
Event	id, timestamp, type, payload	Base class for all bus messages
Thread	id, participants, messages[], status (open/closed)	Archived as a YAML file when closed
Contract	id, sys1_id, budget (resource units), expected_output, deadline, status	Versioning optional – added later
Report	sys1_id, metrics (dict), timestamp	Produced by System 1, consumed by System 3
Strategy	id, focus_areas[], priority, timestamp	Emitted by System 4
Policy	id, name, value	Emitted by System 5
All entities are serializable to JSON/YAML; the PersistencePort defines save(entity) and load(entity_type, id).

5. Event Bus & Messaging
Aspect	Design decision (MVP)	Future‑swap
Message format	Python dict → JSON/YAML when persisted	Replace with protobuf, Avro, etc.
Transport	In‑process queue.Queue per topic	Plug‑in to Redis Streams, Kafka, etc.
Topic registration	bus.register_topic(name) returns a Topic object	Same API for external buses
Publish / Subscribe	topic.publish(event) / topic.subscribe(callback)	Same signature for other adapters
Ordering	FIFO per topic (simple queue)	Can be upgraded to at‑least‑once semantics
External bus	ExternalBusPort – currently a stub that can be called by a test harness to inject “environment events” (new email, new URL).	Later implement a webhook listener or file‑watcher.
6. Runtime Scheduling & Simulation
Need	Implementation (MVP)	Extensibility
Three clocks	1️⃣ Real‑time clock (datetime.now()) for “tomorrow” triggers.
2️⃣ Global step counter (global_step) incremented after each event loop iteration.
3️⃣ Actor step counter (actor_step[sys_id]) stored per System.	Scheduler can be swapped for asyncio or a discrete‑event simulator later.
Trigger engine	TriggerEngine evaluates rules (e.g., “every 100 global steps → System 5 heartbeat”) and posts corresponding events.	Rules can be expressed as JSON/YAML and loaded at runtime.
Turn management	Each System processes its incoming queue in a round‑robin order; no asyncio needed for MVP.	Later replace with thread‑pool or async tasks.
7. LLM Agents & Memory
Component	MVP design	Swap‑out plan
LLM Provider	Local model accessed via LangChain’s LLM interface (e.g., gpt4all, llama.cpp).	Provide an LLMPort with generate(prompt); later implement OpenAI, Anthropic, etc.
Prompt construction	Simple f‑strings (f"System 1: {context}\nMessages:{msg_log}").	Later add Jinja2 or custom DSL.
Observation memory	Flat‑file log (YAML) per agent; each action appends a record (timestamp, event, result).	Replace with vector DB or SQLite if needed.
Tool invocation	Agents call Tool objects (e.g., WebSearchTool, SummarizerTool) via LangChain’s function calling.	Provide a ToolRegistryPort that can expose HTTP services or separate micro‑services.
Determinism	No explicit seed; results may vary – acceptable for prototype.	Add temperature param in LLMPort.
8. Ports & Adapters (Hexagonal Architecture)
Port name	Responsibility	MVP concrete class	Future candidates
EventBusPort	Publish/subscribe events	InProcessBus (queues)	Redis Streams, Kafka
PersistencePort	Save/load entities	YamlFileStore (writes to data/)	SQLite, Parquet, TinyDB
LLMPort	Generate text	LocalLLMAdapter (LangChain)	OpenAI, Anthropic SDKs
ToolPort	Invoke a tool	LocalToolRegistry (Python functions)	Remote gRPC / HTTP services
SchedulerPort	Trigger rules	SimpleTriggerEngine (Python loops)	APScheduler, Celery beat
ConfigPort	Load system config	YamlConfigLoader	Env‑vars, Consul
All ports expose Python abstract base classes so the core VSM code never imports concrete libraries.

9. Contracts & Coordination Messages
9.1 Contract lifecycle (System 3 ↔ System 1)
Proposal – ContractProposal (budget, deadline, expected output).
Ack – System 1 replies with ContractAck (accept/reject + rationale).
Persist – System 3 stores the contract via PersistencePort.
Report – System 1 sends ReportEvents (actual output, resource usage).
Compliance check – System 3 evaluates contract vs. report, may emit ContractUpdate.
9.2 Coordination (System 3 ↔ System 4)
Message	Direction	Payload
StrategyProposal	4 → 3	list of focus areas, priority
StrategyAck	3 → 4	approved focus list + any constraints
StrategyHeartbeat	4 ↔ 3	simple “I’m alive” ping (used for sync)
10. Reporting & Observability
Item	Current format	Future UI
System 3 dashboard	JSON printed to CLI (python run.py --dashboard)	Text UI (curses) → Web UI (React)
Thread logs	Archived YAML files (threads/<id>.yaml)	searchable view in UI
Event trace	print statements in the event loop	Structured logging (JSON) → Loki/Prometheus
11. Extensibility & Skills
Skill definition – follows Anthropic/OpenAI function‑calling schema (name, description, parameters).
Tool Registry – ToolRegistry.register(name, callable); agents discover via ToolRegistry.list().
Future skill plug‑ins – can be added as separate Python packages or containerised services; no code change needed in core VSM.
12. Open Questions / Next Steps
Area	Open question (from the answers)	Suggested next action
Recursion depth decision	System 3 will decide at runtime based on reports, but we need a concrete algorithm (e.g., “if avg compliance < 80 % → split System 1 into two sub‑systems”).	Define a RecursionPolicy class with a pluggable strategy.
External‑bus trigger model	Not yet decided whether environment pushes or pulls events.	Implement a stub poller that reads a folder of “incoming” YAML files; later replace with webhook listener.
Contract schema versioning	Not needed now, but later we may want audit trails.	Add an optional version field in the contract model; keep it optional for now.
Thread archiving	When a thread is closed we archive to a file; need a naming convention.	Use <sys3_id>_<sys1_id>_<timestamp>.yaml.
Policy component	System 5 is placeholder – define a PolicyPort now so later we can plug in a DB‑backed policy engine.	Create an empty PolicyPort interface with get_policy(name) and a NoOpPolicyAdapter.
13. Deliverables for the PRD (next phase)
Architecture diagram (hexagonal view with ports).
Component interface specs (Python ABCs).
Sequence diagram for a full VSM cycle (environment → System 4 → System 3 → System 1 → contract/report → back to System 3).
Data‑model definitions (YAML schema).
Prototype skeleton (repo layout, entry point, CI stub).
Once these are approved, we can flesh them out into a formal Product Requirements Document (features, UI mock‑ups, test cases, rollout plan).

Prepared by: ChatGPT (2024‑06)
Date: 2026‑04‑01


