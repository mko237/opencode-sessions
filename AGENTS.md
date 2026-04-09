# Skill tool usage:
  - skills often recommend using a workflow.. if a task can be accomplished via the workflow perfer following the relevant steps instead of solving a task another way
  - skills are written for you the agent/assistant and also meant to be performed by you, not the user. 
## Python Usage in skills:
  - some skills may have and recommend python script usage.. always use `uv run python` instead of just calling python directly
  - prioritizebuilt in scripts from skills over tools liek grep / glob / read (unless specified or no alternatives exist)

<!-- This section is maintained by the coding agent via lore (https://github.com/BYK/opencode-lore) -->
## Long-term Knowledge

### Architecture

<!-- lore:019d6aa2-2c8b-71d8-8348-23cd5dc35904 -->
* **Hexagonal ports‑and‑adapters**: Hexagonal ports‑and‑adapters: Core domain depends on abstract ports EventBusPort, PersistencePort, LLMPort, ToolPort, SchedulerPort, ConfigPort, \*\*RulePort\*\*, and \*\*TurnManagerPort\*\*. Concrete adapters live under adapters/ and are shared singletons across VSMs, enabling easy swapping without touching core code.

<!-- lore:019d6aa2-2c91-700c-9569-8b24c720c596 -->
* **Three‑clock time model**: System uses three independent clocks: real‑time (datetime.now()), a global step counter incremented each loop, and per‑actor step counters stored in a dict. Each clock can emit an event to the rule engine for time‑based rules.

### Gotcha

<!-- lore:019d6eb5-3fb9-774d-9450-b3564282886d -->
* **Cursor modulo zero‑division in TurnManager**: Fix TurnManager.remove\_actor: guard empty actor\_order before modulo to avoid ZeroDivisionError.

<!-- lore:019d6ee4-a4dc-77eb-a921-ca9cc65fbbe7 -->
* **Design 2 duplicate bus subscriptions**: Duplicate bus subscriptions in ReactiveEngine cause multiple identical callbacks per event type, adding O(N) overhead and double‑processing. Fix by maintaining a set of already‑subscribed event types; on add\_rule, subscribe to the bus only if the event type isn’t in the set, then add it. This ensures each event type has a single subscription and streamlines listener registration.

<!-- lore:019d6eb5-3fb8-731c-83fc-7da3ede56fef -->
* **HierarchicalTurnManager stub missing**: Add HierarchicalTurnManager class with sub\_managers list and round‑robin next\_actor delegation.

<!-- lore:019d6e3a-e517-7d01-9d7c-1893ac4b9c79 -->
* **Many listeners on frequent events**: Evaluating dozens of listeners on every high‑frequency event (e.g., global\_tick) adds O(N) overhead; mitigate by splitting the event into sub‑types (e.g., even/odd ticks) or throttling listeners.

<!-- lore:019d6aa2-2c97-761f-85d4-488b1efd24f0 -->
* **Missing actor\_order update**: If a System 1 spawns a nested VSM but does not add its agents to \`actor\_order\`, the turn manager never schedules them. Ensure spawn logic updates the list.

<!-- lore:019d6e3a-e518-761c-bf55-eb3b9e592047 -->
* **Missing SkillPort abstraction**: Skill‑based extensibility currently uses RulePort and ToolPort; without a dedicated SkillPort the skill lifecycle (load, register, invoke) mixes concerns and hampers future swapping.

<!-- lore:019d7065-1a04-7027-bf54-b785b4c38cc0 -->
* **Ports defined only in design docs, no code implementation**: Current repo lists EventBusPort, PersistencePort, LLMPort, ToolPort, SchedulerPort, ConfigPort, RulePort, TurnManagerPort, and MemoryPort in markdown (step\_1\_working.md, sbom.potential.md) but there is no ports/ package or Python class definitions. Without concrete abstract classes the interfaces aren’t type‑checked or enforceable, delaying adapter implementation. Add a ports/ directory with one abstract base class per port matching the documented method signatures, then build concrete adapters under adapters/.

<!-- lore:019d6aa2-2c99-71a2-a822-d7e1c393d4e6 -->
* **SchedulerPort coupling**: If \`SchedulerPort\` directly imports or calls \`EventBusPort\`, swapping the scheduler becomes hard. Keep \`SchedulerPort\` abstract and inject the bus only where needed.

<!-- lore:019d6eb5-3fb7-7989-b6ba-7e1dfc23f91b -->
* **Undefined THRESHOLD constant in recursion pseudo‑code**: The recursion trigger uses \`THRESHOLD\` but never defines it. Declare \`THRESHOLD = 0.7\` (or expose via ConfigPort) so the rule‑based spawning logic is executable.

### Pattern

<!-- lore:019d7079-02b6-75fc-a718-6f35c3031d00 -->
* **Append port‑interface table to step\_2\_2\_working.md**: Inserted a markdown table of all ports into task 11 of \`step\_2\_2\_working.md\`; the table lists each port, brief description, minimal method signatures, and current implementation status, making the ports‑interface visible to handoff scripts.

<!-- lore:019d6eb5-3fba-7a2f-adb7-1213848148be -->
* **Centralized port list for documentation**: Maintain a single \`Ports\` table (e.g., in sbom.potential.md) listing all abstract ports: EventBusPort, PersistencePort, LLMPort, ToolPort, SchedulerPort, ConfigPort, RulePort, TurnManagerPort, MemoryPort. Reference this table from each design section to avoid duplicate edits when ports change.

<!-- lore:019d6ae8-bc31-7803-bc5f-eecbbe60adc9 -->
* **Components that create or listen to rules**: Components that create or listen to rules (System 3, System 4, System 5, Scheduler, Turn‑manager, UI panels, tests) use \`RulePort\`. System 3 additionally injects \`RulePort\` to add/remove rules at runtime, marking core rules with \`protected: true\` so they stay immutable. All rule actions are referenced via \`action\_module\`/\`action\_func\` and can be filtered by \`origin\`.

<!-- lore:019d6aa2-2c94-7f5e-859f-feacbee08a7f -->
* **Event‑driven rule engine**: Each rule defines \`id\`, \`on\` (event types), \`when\` (string expression), \`priority\`, and an \`action\` callable. On registration the \`when\` string is compiled once to a lambda and stored as \`rule.\_cond\`. Listeners are sorted by \`(priority, id)\` for deterministic order.

<!-- lore:019d6aa2-2c96-7ce9-9639-4d8f36414cfe -->
* **Observation memory per agent**: Agents write a YAML log (\`data/agent\_{id}\_log.yaml\`) with entries \`{timestamp, event\_type, input, output}\`. \`MemoryPort\` abstracts \`append\`, \`load\_all\`, and \`query\` so agents can read/write without caring about storage format.

<!-- lore:019d6e3a-e514-7ce2-91eb-69a07e9f870c -->
* **Recursion trigger based on report complexity**: System 1 agents evaluate their latest report; if report.complexity\_score > THRESHOLD (e.g., 0.7) they instantiate a child VSM and attach it, enabling arbitrary nesting depth.

<!-- lore:019d6aa2-2c92-7e64-b0bf-985e941bcd39 -->
* **Recursive VSM spawning**: System 1 agents may instantiate a full nested VSM (Systems 5‑4‑3‑2‑1) as a child; the child re‑uses the same port instances for lightweight recursion and registers its agents with the turn manager.

<!-- lore:019d7088-2d2f-7c03-b7da-a755e892f681 -->
* **review.todo updates for ports and adapters**: Marked port‑interface verification as completed, and added tasks 24‑25 to \`review.todo.md\` to create a \`ports/\` package with abstract classes and implement concrete adapters for each port.

<!-- lore:019d6aa2-2c95-7681-a3ef-d5cfd05a25d2 -->
* **Rule persistence in YAML**: Rule definitions live in \`config/rules.yaml\`. Each rule can include optional \`protected\` (prevents deletion) and \`origin\` (creator). \`YamlRuleAdapter\` loads the file into an in‑memory dict keyed by \`id\`, writes back on every mutation, and notifies the reactive engine to refresh its listener map, ensuring dynamic updates are persisted.

<!-- lore:019d6ae8-bc30-7141-bb6c-d07bd5396a6d -->
* **RulePort abstraction for dynamic rule management**: RulePort abstraction for dynamic rule management and rule dataclass details. RulePort defines add\_rule, remove\_rule, list\_rules. Rules are represented by a dataclass that now includes a compiled condition field \`\_cond: Callable\[\[Dict], bool]\` and a \`protected: bool\` flag for immutable core rules. \`add\_rule\` compiles the \`when\` string once into \`\_cond\`. Implemented by YamlRuleAdapter persisting to config/rules.yaml and notifying ReactiveEngine. Shown in the hexagonal diagram as a core port.

<!-- lore:019d7011-5c58-78fd-8063-a4f6091e0ee3 -->
* **Session‑handoff script for incremental handoff updates**: Session‑handoff scripts live in \`.agents/skills/session-handoff/scripts\` and should be run with the project’s UV‑managed Python environment: \`uv run python \<script>.py\`. The \`create\_handoff.py\` script generates a file in \`.claude/handoffs/\` named \`YYYY-MM-DD-HHMMSS-\[slug].md\`. It pre‑fills the timestamp, project path, current git branch, recent commits, and any modified files (e.g., the port‑interface table added to \`step\_2\_2\_working.md\`).

<!-- lore:019d6aa2-2c96-7ce9-9639-4d8e3cfecaca -->
* **Skill‑based extensibility**: Each skill is a YAML file under \`skills/\`. \`SkillRegistry\` loads all \`\*.yaml\` files into a dict. \`SkillExecutor\` builds a prompt, calls \`LLMPort\`, parses JSON output, and dispatches to the appropriate \`ToolPort\` or handler.

<!-- lore:019d6f3b-f5f1-7ea4-b7fe-50a903e073b2 -->
* **Step‑N working document template**: Create a markdown file \`Step\_N\_working.md\` for each design step. Use header \`# Step N – Working Document\`, a \`## Goal\` paragraph, then a \`## Section Overview\` list of checklist items copied from the corresponding \`## N.x\` section of \`review.todo.md\`. Mirror the format of \`Step\_1\_working.md\` so each step’s tasks are tracked in a dedicated file.

<!-- lore:019d6e3a-e513-7904-b3ef-c61d3aa34c51 -->
* **TurnManagerPort abstract interface**: Defines three abstract methods: add\_actor(id), remove\_actor(id), next\_actor() -> Optional\[str]. Implementations manage an ordered actor list and cursor for round‑robin scheduling.
<!-- End lore-managed section -->
