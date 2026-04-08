## Step 1 Omissions – First Pass Review

**Overall** – The document captures the four design items (hexagonal view, rule engine, TriggerEngine/rule‑port, turn‑manager) but a few internal inconsistencies and omissions show up when the sections are read together.

---

### 1️⃣ Hexagonal architecture & recursion flow
| Issue | Where | Why it matters |
|------|-------|----------------|
| **Missing System 2 & System 5 definitions** | Section 1.2 (Agent hierarchy) only lists System 3 and System 1; later “Systems 5‑4‑3‑2‑1” is referenced in the pseudo‑code but never described. | The recursion model assumes a full stack of agents (5‑4‑3‑2‑1). Without a brief description of System 2 and System 5 the reader can’t see what ports they use or what responsibilities they have. |
| **Port list mismatch** | In the hex‑graph (lines 31‑37) the core lists `EventBusPort`, `PersistencePort`, `LLMPort`, `ToolPort`, `SchedulerPort`, `ConfigPort`. In the later Turn‑manager implementation (Item 4) the `TurnManagerPort` is added but not shown in the graph. | The ports diagram should include `TurnManagerPort` (and optionally `RulePort`) so the core‑domain view stays consistent. |
| **Recursion heuristic variable** | Pseudo‑code (lines 57‑60) uses `THRESHOLD` but the constant is never defined in the doc. | The algorithm can’t be implemented without a defined threshold value (e.g., `THRESHOLD = 0.7`). |
| **Port‑reuse note** | “Each nested VSM re‑uses the same **Port** instances (event bus, persistence, etc.)” – good, but the diagram shows adapters under each concrete adapter; it might suggest separate instances per VSM. | Clarify that adapters are **singletons** shared by all VSMs, otherwise readers may think each VSM creates its own adapters. |

---

### 2️⃣ Reactive rule‑engine design
| Issue | Where | Why it matters |
|------|-------|----------------|
| **ListenerMap type syntax error** | Line 126: `ListenerMap = Dict[str, List[Rule]]` – extra `]`. | Causes a syntax error if copied verbatim; should be `ListenerMap = Dict[str, List[Rule]]`. |
| **Missing imports** | The code snippets use `time`, `Dict`, `List`, `Optional`, `defaultdict` but the imports are not shown together. | A reader copying the snippet will get `NameError`s. Add `from typing import Dict, List, Optional` and `import time`. |
| **Duplicate subscriptions** | In `ReactiveEngine.add_rule` (lines 259‑262) the engine subscribes to the bus **inside the loop** for each rule added. If multiple rules listen to the same event type the bus will get multiple identical callbacks. | Inefficient and can cause the same event to be handled multiple times per rule list. The engine should subscribe once per event type (e.g., keep a set of already‑subscribed types). |
| **`compile_condition` location** | The helper is defined at lines 131‑134 but not imported where the engine uses it. | Either move the function into the same module or import it explicitly. |
| **Rule `action` signature** | The `Rule` dataclass defines `action: Callable[[Event], None] = lambda e: None` but the YAML loader (lines 272‑280) builds a `Rule` with `action=action` where `action` expects `(ev)` – fine, but the type hint should be `Callable[[Event], None]`. | Minor but keeping type consistency helps static analysis. |
| **`Rule._cond` attribute not declared** | The dataclass doesn’t define `_cond`; it’s added dynamically in `add_rule`. | Consider adding `field(init=False, repr=False)` to make the attribute explicit. |

---

### 3️⃣ TriggerEngine / Dynamic rule management (System 3)
| Issue | Where | Why it matters |
|------|-------|----------------|
| **Port name mismatch** | The text refers to a `RulePort` abstraction (Item 3) but the earlier hexagonal diagram does not list it. | Add `RulePort` to the ports list so the diagram matches the narrative. |
| **`YamlRuleAdapter` description vs implementation** | The adapter is described to “write the full rule list back to `config/rules.yaml` on each mutation”, but the code snippet in the rule engine (`load_rules_from_yaml`) only **reads** the file; there’s no write logic shown. | Include a brief write example (`yaml.safe_dump`) to keep the description and code aligned. |
| **Protected‑rule handling** | The schema example shows `protected: true` but the `Rule` dataclass has no such field. | Add `protected: bool = False` to the dataclass or explain that it lives only in the YAML layer. |
| **Rule‑change events** | The design mentions a `RuleChangeEvent` (line 357) but no concrete definition or usage is shown elsewhere. | Either provide a small definition or remove the placeholder to avoid dangling references. |

---

### 4️⃣ Turn‑manager (Hybrid hierarchical)
| Issue | Where | Why it matters |
|------|-------|----------------|
| **Missing `TurnManagerPort` import** | The abstract class is defined (lines 374‑381) but the file does not import `ABC`, `abstractmethod`. | Add `from abc import ABC, abstractmethod`. |
| **`InMemoryTurnManager` missing type imports** | Uses `List` and `Optional` without import. | Add `from typing import List, Optional`. |
| **Cursor adjustment logic** | In `remove_actor` the cursor is decremented if the removed index is less than the cursor, then `% len(self.actor_order)`. If the list becomes empty, `len(self.actor_order)` is `0` → division‑by‑zero on the modulo. | Guard with `if self.actor_order:` before the modulo or set cursor to `0` when the list empties. |
| **Hierarchical manager not implemented** | Item 4 lists a “HierarchicalTurnManager” that holds sub‑managers, but only the simple `InMemoryTurnManager` is shown. | Provide at least a stub class (`HierarchicalTurnManager`) with `add_sub_manager`, `next_actor` delegating to sub‑managers, to keep the design concrete. |
| **Turn‑manager port added to diagram** | As noted in Item 1, the hexagonal diagram should be updated to include `TurnManagerPort` (and maybe `RulePort`). | Keeps the architecture view consistent across sections. |
| **Root‑manager interaction description** | The root manager “selects the next sub‑manager and asks it for its `next_actor()`” – but the pseudo‑code for the root manager is missing. | Add a small snippet showing how the root loops through sub‑managers (e.g., round‑robin over a list of sub‑managers). |

---

### 5️⃣ Minor formatting / consistency points
| Issue | Detail |
|------|--------|
| **Bullet‑checkmarks** – The checklist items use `[x]` and `[ ]` but later sections still have unchecked items (`[ ] Review the TriggerEngine rule format`). Keep the status synchronized if the doc is updated. |
| **Line‑number references** – Some cross‑references (e.g., “see `RulePort` in the hex‑graph”) rely on line numbers that may shift as the doc evolves. Consider using section headings instead of absolute line numbers. |
| **Code block language tags** – Most code blocks lack a language tag (`python`, `yaml`). Adding them improves readability. |
| **Consistent naming** – `System 3` is sometimes called “Ops‑Ctrl” and sometimes “System 3 (Ops‑Ctrl)”. Pick one form and use it throughout. |
| **Timestamp** – The autogenerated timestamp at the bottom (`2026‑04‑07`) is static; if the doc is edited later, consider updating it automatically or removing it. |

---

### **Summary of actions needed to resolve inconsistencies**
1. **Add missing System 2 and System 5 descriptions** (brief responsibilities, ports used).  
2. **Update the hexagonal diagram** to include `TurnManagerPort` and `RulePort`.  
3. **Define `THRESHOLD`** (e.g., `THRESHOLD = 0.7`) in the recursion pseudo‑code.  
4. **Fix syntax errors** (`ListenerMap` line, missing imports, duplicate subscriptions).  
5. **Add `protected` field** to `Rule` dataclass or note it’s YAML‑only.  
6. **Provide a write‑back example** for `YamlRuleAdapter`.  
7. **Implement a minimal `HierarchicalTurnManager` stub** and show root‑manager interaction.  
8. **Adjust cursor logic** in `remove_actor` to handle empty lists safely.  
9. **Synchronize check‑list status** and add language tags to code blocks.  

These updates will make the Step 1 working document internally consistent and ready for the next implementation phase.
