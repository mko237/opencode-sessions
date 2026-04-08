<!-- This section is maintained by the coding agent via lore (https://github.com/BYK/opencode-lore) -->
## Long-term Knowledge

### Architecture

<!-- lore:019d6aa2-2c8b-71d8-8348-23cd5dc35904 -->
* **Hexagonal ports‑and‑adapters**: Core domain modules depend only on abstract ports (EventBusPort, PersistencePort, LLMPort, ToolPort, SchedulerPort, ConfigPort). Concrete adapters live under adapters/ and implement those ports, enabling swap‑in without touching core code.

<!-- lore:019d6aa2-2c91-700c-9569-8b24c720c596 -->
* **Three‑clock time model**: System uses three independent clocks: real‑time (datetime.now()), a global step counter incremented each loop, and per‑actor step counters stored in a dict. Each clock can emit an event to the rule engine for time‑based rules.

### Gotcha

<!-- lore:019d6aa2-2c97-761f-85d4-488b1efd24f0 -->
* **Missing actor\_order update**: If a System 1 spawns a nested VSM but does not add its agents to \`actor\_order\`, the turn manager never schedules them. Ensure spawn logic updates the list.

<!-- lore:019d6aa2-2c99-71a2-a822-d7e1c393d4e6 -->
* **SchedulerPort coupling**: If \`SchedulerPort\` directly imports or calls \`EventBusPort\`, swapping the scheduler becomes hard. Keep \`SchedulerPort\` abstract and inject the bus only where needed.

<!-- lore:019d6aa2-2c98-7316-a156-5eb6c7ef15c7 -->
* **Uncompiled rule conditions**: Leaving \`when\` strings uncompiled forces \`eval\` on every event, hurting performance. Always compile once during \`add\_rule\` and store the lambda.

### Pattern

<!-- lore:019d6ae8-bc31-7803-bc5f-eecbbe60adc9 -->
* **Components that create or listen to rules**: System 3 (ops‑ctrl), System 4 (strategy), System 5 (policy), the Scheduler, the Turn‑manager, UI panels, and test harnesses may add, remove, or listen to rules. Each should use \`RulePort\` and can tag rules with \`origin\` to filter their own rules. Protected rules (e.g., heartbeat) stay immutable across components.

<!-- lore:019d6aa2-2c94-7f5e-859f-feacbee08a7f -->
* **Event‑driven rule engine**: Each rule defines \`id\`, \`on\` (event types), \`when\` (string expression), \`priority\`, and an \`action\` callable. On registration the \`when\` string is compiled once to a lambda and stored as \`rule.\_cond\`. Listeners are sorted by \`(priority, id)\` for deterministic order.

<!-- lore:019d6aa2-2c96-7ce9-9639-4d8f36414cfe -->
* **Observation memory per agent**: Agents write a YAML log (\`data/agent\_{id}\_log.yaml\`) with entries \`{timestamp, event\_type, input, output}\`. \`MemoryPort\` abstracts \`append\`, \`load\_all\`, and \`query\` so agents can read/write without caring about storage format.

<!-- lore:019d6aa2-2c92-7e64-b0bf-985e941bcd39 -->
* **Recursive VSM spawning**: System 1 agents may instantiate a full nested VSM (Systems 5‑4‑3‑2‑1) as a child; the child re‑uses the same port instances for lightweight recursion and registers its agents with the turn manager.

<!-- lore:019d6aa2-2c93-7d04-85e6-122048f420c0 -->
* **Round‑robin turn manager**: Turn manager maintains a flat \`actor\_order\` list of all agents (including nested System 1). When a new agent is spawned it must be appended to this list; the manager pulls the next ID, processes its turn, then moves it to the end.

<!-- lore:019d6aa2-2c95-7681-a3ef-d5cfd05a25d2 -->
* **Rule persistence in YAML**: Rule definitions are stored in \`config/rules.yaml\`. At startup a \`RulePort\` implementation (\`YamlRuleAdapter\`) loads the file into an in‑memory dict, registers each rule with the engine, and writes back any runtime additions/removals. Each rule can include optional \`protected\` (immutable for designers) and \`origin\` (creator component) fields to aid dynamic management.

<!-- lore:019d6ae8-bc30-7141-bb6c-d07bd5396a6d -->
* **RulePort abstraction for dynamic rule management**: A \`RulePort\` interface defines \`add\_rule(rule)\`, \`remove\_rule(rule\_id)\`, and \`list\_rules()\`. Concrete adapters (e.g., \`YamlRuleAdapter\`) implement the interface, keep the rule list in memory, persist changes to the YAML file, and update the engine’s listener map. All components inject this port to manage rules at runtime.

<!-- lore:019d6aa2-2c96-7ce9-9639-4d8e3cfecaca -->
* **Skill‑based extensibility**: Each skill is a YAML file under \`skills/\`. \`SkillRegistry\` loads all \`\*.yaml\` files into a dict. \`SkillExecutor\` builds a prompt, calls \`LLMPort\`, parses JSON output, and dispatches to the appropriate \`ToolPort\` or handler.
<!-- End lore-managed section -->
