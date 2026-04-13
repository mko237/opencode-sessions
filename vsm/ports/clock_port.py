"""ClockPort protocol definition.

The three‑clock model provides:
- ``real_time`` – wall‑clock datetime.
- ``global_step`` – a monotonically increasing integer incremented each tick.
- ``actor_step`` – per‑actor step counters.

Additional helper methods are included to mutate the step counters and to
subscribe to tick notifications.  Concrete implementations (e.g. ``SimpleClock``)
should provide these methods.
"""

from __future__ import annotations

from datetime import datetime
from typing import Callable, Protocol


class ClockPort(Protocol):
    """Abstract interface for the three‑clock model.

    Implementations are expected to be lightweight and injectable via the
    ``PortFactory``.  The protocol includes read‑only getters, mutators, and a
    simple publish/subscribe mechanism for tick events.
    """

    # ----- read‑only -------------------------------------------------
    def real_time(self) -> datetime:
        """Return the current wall‑clock time (e.g. ``datetime.now()``)."""

    def global_step(self) -> int:
        """Return the current global step counter."""

    def actor_step(self, actor_id: str) -> int:
        """Return the step count for a specific actor or system."""

    # ----- mutators --------------------------------------------------
    def tick(self) -> None:
        """Advance the global step and notify tick subscribers.

        Implementations should increment ``global_step`` and then invoke any
        registered callbacks via ``subscribe_tick``.
        """

    def inc_actor_step(self, actor_id: str, delta: int = 1) -> None:
        """Increment the step count for *actor_id* by *delta*.

        ``delta`` defaults to ``1``; callers can use a larger value for batch
        updates.
        """

    # ----- optional listeners -----------------------------------------
    def subscribe_tick(self, handler: Callable[[int], None]) -> None:
        """Register *handler* to receive the new global step after each tick."""

    def unsubscribe_tick(self, handler: Callable[[int], None]) -> None:
        """Remove a previously registered tick *handler*."""
