# VSM‑LLM Architecture – Layer Overview

---

## 1️⃣ Presentation / UI (future)
- CLI / React UI that talks to the VSM core.

## 2️⃣ Application / orchestration layer
- **VSM bootstrap** (run.py) – wires ports & adapters.
- **Turn‑manager** – round‑robin / hierarchical scheduling.
- **TriggerEngine** – time‑/step‑based rule emission.
- **ReactiveEngine** – rule registration & event dispatch.

## 3️⃣ Core domain (agents & data objects)
- Agent classes: `MGMT‑5/4/3`, `OPS‑1/2`, `System‑1`.
- Dataclasses: `Event`, `Message`, `Contract`, `Report`, `Strategy`, `Policy`, `Thread`.
- `MemoryPort` interface – per‑agent log.

## 4️⃣ Ports (hexagonal interfaces)
- `EventBusPort` – internal events.
- `ExternalEventBusPort` – external events.
- `PersistencePort`
- `LLMPort`
- `ToolPort`
- `SchedulerPort`
- `ConfigPort`
- `RulePort`
- `TurnManagerPort`
- `MemoryPort`
- `ClockPort`

## 5️⃣ Adapters (concrete implementations)
- `InProcessBus` → implements **EventBusPort**.
- `InProcessExternalBus` → implements **ExternalEventBusPort**.
- `YamlFileStore` → implements **PersistencePort**.
- `LocalLLMAdapter` → implements **LLMPort**.
- `LocalToolRegistry` → implements **ToolPort**.
- `SimpleTriggerEngine` → implements **SchedulerPort**.
- `YamlConfigLoader` → implements **ConfigPort**.
- `YamlRuleAdapter` → implements **RulePort**.
- `InMemoryTurnManager` → implements **TurnManagerPort**.
- `YamlMemoryAdapter` → implements **MemoryPort**.
- `SimpleClock` → implements **ClockPort**.

## 6️⃣ External environment (outside world)
- Email inbox, web URLs, video links, etc.
- Injected via **ExternalEventBusPort**.

---

### Interaction flow
1. **Presentation** sends commands to the **Application** layer.
2. **Application** creates agents, schedules turns, and registers rules.
3. Agents use **Ports** to interact with the outside world or persistence.
4. **Adapters** fulfil those ports with concrete tech (queues, YAML files, LLM wrappers, etc.).
5. **ExternalEventBusPort** receives external stimuli and forwards them to internal agents.

---

*This markdown captures the layered grouping of components as discussed and aligns with the SBOM entries.*
