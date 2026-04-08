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
* **Design 2 duplicate bus subscriptions**: ReactiveEngine adds a bus subscription inside the per‑rule loop, causing multiple identical callbacks for the same event type. This adds O(N) overhead and can double‑process events.

<!-- lore:019d6eb5-3fb8-731c-83fc-7da3ede56fef -->
* **HierarchicalTurnManager stub missing**: Add HierarchicalTurnManager class with sub\_managers list and round‑robin next\_actor delegation.

<!-- lore:019d6e3a-e517-7d01-9d7c-1893ac4b9c79 -->
* **Many listeners on frequent events**: Evaluating dozens of listeners on every high‑frequency event (e.g., global\_tick) adds O(N) overhead; mitigate by splitting the event into sub‑types (e.g., even/odd ticks) or throttling listeners.

<!-- lore:019d6aa2-2c97-761f-85d4-488b1efd24f0 -->
* **Missing actor\_order update**: If a System 1 spawns a nested VSM but does not add its agents to \`actor\_order\`, the turn manager never schedules them. Ensure spawn logic updates the list.

<!-- lore:019d6e3a-e518-761c-bf55-eb3b9e592047 -->
* **Missing SkillPort abstraction**: Skill‑based extensibility currently uses RulePort and ToolPort; without a dedicated SkillPort the skill lifecycle (load, register, invoke) mixes concerns and hampers future swapping.

<!-- lore:019d6eb5-3fb6-7d00-8008-a828b78103c8 -->
* **Rule dataclass missing compiled condition and protected flag**: Rule dataclass currently defines only id, on, when, priority, action. Add explicit fields for the compiled condition and protected flag: \`\_cond: Callable\[\[Dict], bool] = field(init=False, repr=False)\` and \`protected: bool = False\`. Align this with the YAML rule schema used by \`YamlRuleAdapter\`: each rule entry in \`config/rules.yaml\` includes \`id\`, \`on\` (list of event types), \`when\` (condition expression), optional \`priority\` (default 0), optional \`protected\`, optional \`origin\`, and \`action\` (module/function reference or inline code). This combined definition ensures the in‑code model matches persisted YAML and makes rule handling self‑contained.

<!-- lore:019d6aa2-2c99-71a2-a822-d7e1c393d4e6 -->
* **SchedulerPort coupling**: If \`SchedulerPort\` directly imports or calls \`EventBusPort\`, swapping the scheduler becomes hard. Keep \`SchedulerPort\` abstract and inject the bus only where needed.

<!-- lore:019d6ee2-425f-76ce-884e-4d7ab31f9a04 -->
* **Step 1 design deviations from VSM**: Step 1 design deviations: missing System 2 & 5 definitions; TurnManagerPort absent; undefined THRESHOLD; cursor modulo zero‑division bug; missing HierarchicalTurnManager stub; missing imports and ListenerMap typo (ListenerMap alias should be Dict\[str, List\[Rule]]); duplicate bus subscriptions. Recommend fixing these now.

<!-- lore:019d6aa2-2c98-7316-a156-5eb6c7ef15c7 -->
* **Uncompiled rule conditions**: Leaving \`when\` strings uncompiled forces \`eval\` on every event, hurting performance. Always compile once during \`add\_rule\` and store the lambda.

<!-- lore:019d6eb5-3fb7-7989-b6ba-7e1dfc23f91b -->
* **Undefined THRESHOLD constant in recursion pseudo‑code**: The recursion trigger uses \`THRESHOLD\` but never defines it. Declare \`THRESHOLD = 0.7\` (or expose via ConfigPort) so the rule‑based spawning logic is executable.

### Pattern

<!-- lore:019d6eb5-3fba-7a2f-adb7-1213848148be -->
* **Centralized port list for documentation**: Maintain a single \`Ports\` table (e.g., in sbom.potential.md) listing all abstract ports: EventBusPort, PersistencePort, LLMPort, ToolPort, SchedulerPort, ConfigPort, RulePort, TurnManagerPort, MemoryPort. Reference this table from each design section to avoid duplicate edits when ports change.

<!-- lore:019d6ae8-bc31-7803-bc5f-eecbbe60adc9 -->
* **Components that create or listen to rules**: Components that create or listen to rules (System 3, System 4, System 5, Scheduler, Turn‑manager, UI panels, tests) use \`RulePort\`. System 3 additionally injects \`RulePort\` to add/remove rules at runtime, marking core rules with \`protected: true\` so they stay immutable. All rule actions are referenced via \`action\_module\`/\`action\_func\` and can be filtered by \`origin\`.

<!-- lore:019d6aa2-2c94-7f5e-859f-feacbee08a7f -->
* **Event‑driven rule engine**: Each rule defines \`id\`, \`on\` (event types), \`when\` (string expression), \`priority\`, and an \`action\` callable. On registration the \`when\` string is compiled once to a lambda and stored as \`rule.\_cond\`. Listeners are sorted by \`(priority, id)\` for deterministic order.

<!-- lore:019d6aa2-2c96-7ce9-9639-4d8f36414cfe -->
* **Observation memory per agent**: Agents write a YAML log (\`data/agent\_{id}\_log.yaml\`) with entries \`{timestamp, event\_type, input, output}\`. \`MemoryPort\` abstracts \`append\`, \`load\_all\`, and \`query\` so agents can read/write without caring about storage format.

<!-- lore:019d6e3a-e516-7f4b-aec2-623e89fff0ee -->
* **ReactiveEngine listener registration**: ReactiveEngine listener registration: on add\_rule the engine subscribes to the bus for each rule's event type, causing duplicate callbacks. Fix by tracking a set of already‑subscribed types and subscribe only once per type.

<!-- lore:019d6e3a-e514-7ce2-91eb-69a07e9f870c -->
* **Recursion trigger based on report complexity**: System 1 agents evaluate their latest report; if report.complexity\_score > THRESHOLD (e.g., 0.7) they instantiate a child VSM and attach it, enabling arbitrary nesting depth.

<!-- lore:019d6aa2-2c92-7e64-b0bf-985e941bcd39 -->
* **Recursive VSM spawning**: System 1 agents may instantiate a full nested VSM (Systems 5‑4‑3‑2‑1) as a child; the child re‑uses the same port instances for lightweight recursion and registers its agents with the turn manager.

<!-- lore:019d6aa2-2c93-7d04-85e6-122048f420c0 -->
* **Round‑robin turn manager**: Turn‑manager implements a hierarchical round‑robin: every VSM owns a TurnManager (actor list, add/remove, next\_actor). A root manager holds sub‑managers and on each global tick selects the next sub‑manager and calls its next\_actor, yielding an interleaved turn order (e.g., sys5 → sys4 → sys3 → sys1 → nested sys1‑0 → nested sys1‑1 …). This keeps deterministic ordering, supports dynamic nested VSM creation, isolates each VSM’s schedule, and adds only one extra call per tick. Persistence of each manager’s actor\_order is handled via PersistencePort. The public API is defined by TurnManagerPort with methods add\_actor(id), remove\_actor(id), next\_actor().

<!-- lore:019d6aa2-2c95-7681-a3ef-d5cfd05a25d2 -->
* **Rule persistence in YAML**: Rule definitions live in \`config/rules.yaml\`. Each rule can include optional \`protected\` (prevents deletion) and \`origin\` (creator). \`YamlRuleAdapter\` loads the file into an in‑memory dict keyed by \`id\`, writes back on every mutation, and notifies the reactive engine to refresh its listener map, ensuring dynamic updates are persisted.

<!-- lore:019d6ae8-bc30-7141-bb6c-d07bd5396a6d -->
* **RulePort abstraction for dynamic rule management**: RulePort abstraction for dynamic rule management: defines add\_rule, remove\_rule, list\_rules. Implemented by YamlRuleAdapter which persists to config/rules.yaml and notifies the ReactiveEngine. Now shown in the hexagonal diagram as a core port.

<!-- lore:019d6aa2-2c96-7ce9-9639-4d8e3cfecaca -->
* **Skill‑based extensibility**: Each skill is a YAML file under \`skills/\`. \`SkillRegistry\` loads all \`\*.yaml\` files into a dict. \`SkillExecutor\` builds a prompt, calls \`LLMPort\`, parses JSON output, and dispatches to the appropriate \`ToolPort\` or handler.

<!-- lore:019d6e3a-e513-7904-b3ef-c61d3aa34c51 -->
* **TurnManagerPort abstract interface**: Defines three abstract methods: add\_actor(id), remove\_actor(id), next\_actor() -> Optional\[str]. Implementations manage an ordered actor list and cursor for round‑robin scheduling.
<!-- End lore-managed section -->
