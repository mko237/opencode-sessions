"""Simple YAML‑based persistence adapter.

Stores arbitrary Python objects (serializable by ``yaml.safe_dump``) under a string
key in a single YAML file.  The file path is supplied at construction time.
"""

import yaml
from pathlib import Path
from typing import Any
from ..ports.persistence_port import PersistencePort


class YamlFileStore(PersistencePort):
    def __init__(self, file_path: str | Path):
        self.file = Path(file_path)
        self.file.parent.mkdir(parents=True, exist_ok=True)
        # Load existing data or start with empty dict
        if self.file.exists():
            with self.file.open() as f:
                self._data = yaml.safe_load(f) or {}
        else:
            self._data = {}

    def _write(self) -> None:
        with self.file.open("w") as f:
            yaml.safe_dump(self._data, f)

    def save(self, key: str, obj: Any) -> None:
        self._data[key] = obj
        self._write()

    def load(self, key: str) -> Any:
        return self._data.get(key)

    def delete(self, key: str) -> None:
        if key in self._data:
            del self._data[key]
            self._write()
