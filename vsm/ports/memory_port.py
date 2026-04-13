"""Port contract for per‑agent observation memory."""

from typing import Protocol, Any, List, runtime_checkable


@runtime_checkable
class MemoryPort(Protocol):
    def append(self, entry: Any) -> None: ...

    def load_all(self) -> List[Any]: ...

    def query(self, **filters: Any) -> List[Any]: ...

    def delete(self, entry_id: str) -> None: ...
