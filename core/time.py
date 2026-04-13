"""SimpleClock implementation of ``ClockPort``.

The class is deliberately minimal: it tracks a global step counter, a per‑actor
step dictionary, and a list of tick subscribers.  It can be instantiated and
injected via the ``PortFactory``.
"""

from __future__ import annotations

from datetime import datetime
from typing import Callable, Dict, List

from vsm.ports.clock_port import ClockPort


class SimpleClock:
    """Concrete ``ClockPort`` implementation.

    Attributes
    ----------
    _global_step: int
        Monotonically increasing counter incremented on each ``tick``.
    _actor_steps: dict[str, int]
        Mapping from actor identifiers to their individual step counters.
    _subscribers: list[Callable[[int], None]]
        Callbacks invoked after each ``tick`` with the new global step value.
    """

    def __init__(self) -> None:
        self._global_step: int = 0
        self._actor_steps: Dict[str, int] = {}
        self._subscribers: List[Callable[[int], None]] = []

    # ----- read‑only -------------------------------------------------
    def real_time(self) -> datetime:
        """Return the current wall‑clock time.

        ``datetime.now()`` is used so the method is cheap and side‑effect free.
        """
        return datetime.now()

    def global_step(self) -> int:
        return self._global_step

    def actor_step(self, actor_id: str) -> int:
        return self._actor_steps.get(actor_id, 0)

    # ----- mutators --------------------------------------------------
    def tick(self) -> None:
        """Advance the global step and notify subscribed handlers."""
        self._global_step += 1
        for handler in list(self._subscribers):
            handler(self._global_step)

    def inc_actor_step(self, actor_id: str, delta: int = 1) -> None:
        self._actor_steps[actor_id] = self._actor_steps.get(actor_id, 0) + delta

    # ----- listeners -------------------------------------------------
    def subscribe_tick(self, handler: Callable[[int], None]) -> None:
        if handler not in self._subscribers:
            self._subscribers.append(handler)

    def unsubscribe_tick(self, handler: Callable[[int], None]) -> None:
        if handler in self._subscribers:
            self._subscribers.remove(handler)

    # ----- optional protocol compliance -------------------------------
    # ``SimpleClock`` implements the ``ClockPort`` protocol by providing the
    # required methods.  Adding ``# type: ignore[misc]`` would silence mypy if
    # needed, but the explicit method signatures keep the implementation clear.
