"""Port contract for rule storage and CRUD operations."""

from typing import Protocol, Any, List, runtime_checkable


@runtime_checkable
class RulePort(Protocol):
    def add(self, rule: Any) -> None: ...

    def remove(self, rule_id: str) -> None: ...

    def get_all(self) -> List[Any]: ...
