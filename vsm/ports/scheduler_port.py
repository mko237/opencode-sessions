"""Port contract for scheduling rules or tasks.

A scheduler receives rule objects (or similar) and triggers them at the appropriate
time.
"""

from typing import Protocol, Any, List, runtime_checkable


@runtime_checkable
class SchedulerPort(Protocol):
    def add_rule(self, rule: Any) -> None:
        """Register a rule with the scheduler."""
        ...

    def remove_rule(self, rule_id: str) -> None:
        """Unregister a rule identified by ``rule_id``."""
        ...

    def list_rules(self) -> List[Any]:
        """Return all registered rules."""
        ...
