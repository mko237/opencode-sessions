"""Port contract for round‑robin turn management."""

from typing import Protocol, runtime_checkable


@runtime_checkable
class TurnManagerPort(Protocol):
    def add_actor(self, actor_id: str) -> None: ...

    def remove_actor(self, actor_id: str) -> None: ...

    def next_actor(self) -> str: ...

    def size(self) -> int: ...
