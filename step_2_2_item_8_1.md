# MemoryPort design (pseudo‑code & interface)

---

### 1. Port (hexagonal) definition

```python
# ports/memory_port.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class MemoryPort(ABC):
    """Abstract interface for per‑agent memory persistence."""

    @abstractmethod
    def load(self, agent_id: str) -> List[Dict[str, Any]]:
        """Return the full ordered list of memory entries for *agent_id*.

        Each entry is a dict that can store any JSON‑serialisable data
        (e.g. observations, facts, timestamps)."""

    @abstractmethod
    def append(self, agent_id: str, entry: Dict[str, Any]) -> None:
        """Append a new memory entry for *agent_id* and persist it."""

    @abstractmethod
    def replace(self, agent_id: str, index: int, entry: Dict[str, Any]) -> None:
        """Replace the entry at *index* for *agent_id* with *entry*."""

    @abstractmethod
    def clear(self, agent_id: str) -> None:
        """Delete all stored entries for *agent_id*."""
```

*Why these methods?*
- **load** – needed by agents at start‑up or after a context‑window overflow.
- **append** – primary write path when a new observation is added (e.g. after a turn).
- **replace** – useful for updating a distilled entry (distillation step may replace a raw segment with a distilled one).
- **clear** – for tests or when an agent is re‑instantiated.

All methods return simple Python types to keep the port implementation‑agnostic.

---

### 2. Concrete YAML‑based adapter (pseudo‑code)

```python
# adapters/yaml_memory_adapter.py
import yaml
from pathlib import Path
from typing import List, Dict, Any
from ports.memory_port import MemoryPort

class YamlMemoryAdapter(MemoryPort):
    """Persist each agent’s memory as a YAML list in `data/memory/`."""

    def __init__(self, base_dir: Path = Path("data/memory")):
        self.base = base_dir
        self.base.mkdir(parents=True, exist_ok=True)

    def _file(self, agent_id: str) -> Path:
        return self.base / f"{agent_id}.yaml"

    def load(self, agent_id: str) -> List[Dict[str, Any]]:
        f = self._file(agent_id)
        if not f.exists():
            return []
        return yaml.safe_load(f.read_text()) or []

    def _write(self, agent_id: str, entries: List[Dict[str, Any]]) -> None:
        f = self._file(agent_id)
        f.write_text(yaml.safe_dump(entries, sort_keys=False))

    def append(self, agent_id: str, entry: Dict[str, Any]) -> None:
        entries = self.load(agent_id)
        entries.append(entry)
        self._write(agent_id, entries)

    def replace(self, agent_id: str, index: int, entry: Dict[str, Any]) -> None:
        entries = self.load(agent_id)
        entries[index] = entry
        self._write(agent_id, entries)

    def clear(self, agent_id: str) -> None:
        self._write(agent_id, [])
```

*Key points*
- **File layout** – `data/memory/<agent_id>.yaml`; each file holds a YAML list of dicts, matching the SBOM entry `YamlMemoryAdapter (per‑agent YAML log)`.
- **Atomicity** – whole list is read‑modified‑written; sufficient for the prototype and keeps the implementation simple.
- **Extensibility** – swapping to a DB or JSON store only requires a new class implementing the same four methods.

---

### 3. Observation format (what an entry looks like)

```yaml
- timestamp: "2026-04-10T18:47:12Z"
  type: "observation"
  content:
    - "🔍 observed: new file created `adapters/yaml_memory_adapter.py`"
    - "✅ memory port interface defined"
  priority: 2   # optional, higher = more important for later distillation
```

*Why a list of strings?*
- Mirrors the design note: “list of observations – bullet list of observations – each bullet can be prefixed with an emoji to indicate priority”.
- Allows agents to iterate over the list, filter by `type` (observation, fact, narrative) or by `priority`.

---

### 4. Interaction flow (high‑level)

1. **Agent startup** → `memory = memory_port.load(agent_id)` → stores in `self.memory`.
2. **During a turn** → agent creates an observation dict → `memory_port.append(agent_id, observation)`.
3. **When context window exceeds threshold** → a **Distillation** sub‑agent reads the raw entries, creates a distilled entry (narrative + facts) and calls `replace` to swap the old segment.
4. **Reflection** → an agent asks the memory port for the latest N entries or searches by `type`; the port can expose a helper `search(agent_id, predicate)` if needed (can be added later without breaking the base interface).

---

### 5. Minimal interface contract (what callers can rely on)

| Method | Params | Return | Guarantees |
|--------|--------|--------|------------|
| `load(agent_id)` | `str` | `list[dict]` (ordered as persisted) | Returns a shallow copy; modifications must go through `append/replace/clear`. |
| `append(agent_id, entry)` | `str`, `dict` | `None` | Entry is appended **atomically** and persisted. |
| `replace(agent_id, index, entry)` | `str`, `int`, `dict` | `None` | Replaces the exact index; raises `IndexError` if out of bounds. |
| `clear(agent_id)` | `str` | `None` | All entries for that agent are removed; file is overwritten with an empty list. |

---

### 6. Next steps (when ready to implement)
1. Create `ports/` and `adapters/` directories.
2. Add the abstract `MemoryPort` class (as above).
3. Add the `YamlMemoryAdapter` concrete class.
4. Write a quick unit test that:
   - Instantiates the adapter, clears a test agent’s memory, appends two entries, loads and asserts order, replaces the first entry, clears again.

That will give us a functioning memory layer aligned with the SBOM design and ready for the later distillation and reflection agents.
