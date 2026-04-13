"""YAML‑backed rule storage implementing ``RulePort``.

Rules are stored as a list of dicts in a YAML file.  The file is read on
initialisation and written on every mutation.
"""

import yaml
from pathlib import Path
from typing import List, Any, Dict
from ..ports.rule_port import RulePort


class YamlRuleAdapter(RulePort):
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if self.path.exists():
            with self.path.open() as f:
                self._rules: List[Dict[str, Any]] = yaml.safe_load(f) or []
        else:
            self._rules = []
        self._write()

    def _write(self) -> None:
        with self.path.open("w") as f:
            yaml.safe_dump(self._rules, f)

    def add(self, rule: Any) -> None:
        self._rules.append(rule)
        self._write()

    def remove(self, rule_id: str) -> None:
        self._rules = [r for r in self._rules if r.get("id") != rule_id]
        self._write()

    def get_all(self) -> List[Any]:
        return list(self._rules)
