"""YAML‑backed memory adapter implementing ``MemoryPort``.

It stores a list of arbitrary entries in a YAML file.  Each entry is expected to be a
serialisable mapping; the adapter assigns a unique ``id`` if the entry lacks one.
"""

import yaml
from pathlib import Path
from typing import List, Any, Dict
import uuid
from ..ports.memory_port import MemoryPort


class YamlMemoryAdapter(MemoryPort):
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if self.path.exists():
            with self.path.open() as f:
                self._entries: List[Dict[str, Any]] = yaml.safe_load(f) or []
        else:
            self._entries = []
        self._write()

    def _write(self) -> None:
        with self.path.open("w") as f:
            yaml.safe_dump(self._entries, f)

    def append(self, entry: Any) -> None:
        if isinstance(entry, dict) and "id" not in entry:
            entry = {"id": str(uuid.uuid4()), **entry}
        self._entries.append(entry)
        self._write()

    def load_all(self) -> List[Any]:
        return list(self._entries)

    def query(self, **filters: Any) -> List[Any]:
        result = []
        for e in self._entries:
            if all(e.get(k) == v for k, v in filters.items()):
                result.append(e)
        return result

    def delete(self, entry_id: str) -> None:
        self._entries = [e for e in self._entries if e.get("id") != entry_id]
        self._write()
