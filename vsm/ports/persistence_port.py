"""Port contract for key‑value persistence.

Adapters implement a simple ``save``/``load`` API keyed by a string.
"""

from typing import Protocol, Any, runtime_checkable


@runtime_checkable
class PersistencePort(Protocol):
    def save(self, key: str, obj: Any) -> None:
        """Persist ``obj`` under ``key``."""
        ...

    def load(self, key: str) -> Any:
        """Retrieve the object stored under ``key``."""
        ...

    def delete(self, key: str) -> None:
        """Remove the entry for ``key``."""
        ...
