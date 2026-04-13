"""Very simple trigger engine implementing ``SchedulerPort``.

It stores rule objects (any) in a list and provides basic CRUD operations.
"""

from typing import Any, List
from ..ports.scheduler_port import SchedulerPort


class SimpleTriggerEngine(SchedulerPort):
    def __init__(self) -> None:
        self._rules: List[Any] = []

    def add_rule(self, rule: Any) -> None:
        self._rules.append(rule)

    def remove_rule(self, rule_id: str) -> None:
        # Assume each rule has an ``id`` attribute.
        self._rules = [r for r in self._rules if getattr(r, "id", None) != rule_id]

    def list_rules(self) -> List[Any]:
        return list(self._rules)
