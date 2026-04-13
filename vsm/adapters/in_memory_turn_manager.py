"""In‑memory round‑robin turn manager.

Implements the ``TurnManagerPort`` protocol and provides O(1) add/remove/next.
"""

from typing import List
from ..ports.turn_manager_port import TurnManagerPort


class InMemoryTurnManager(TurnManagerPort):
    def __init__(self) -> None:
        self._actors: List[str] = []
        self._index = 0

    def add_actor(self, actor_id: str) -> None:
        if actor_id not in self._actors:
            self._actors.append(actor_id)

    def remove_actor(self, actor_id: str) -> None:
        if actor_id in self._actors:
            self._actors.remove(actor_id)
            # adjust index if needed
            if self._index >= len(self._actors):
                self._index = 0

    def next_actor(self) -> str:
        if not self._actors:
            raise IndexError("No actors registered")
        actor = self._actors[self._index]
        self._index = (self._index + 1) % len(self._actors)
        return actor

    def size(self) -> int:
        return len(self._actors)
