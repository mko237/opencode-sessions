"""Event dataclass used across the VSM system.

Provides a lightweight container for events emitted by ports such as the
`ClockPort` or `EventBusPort`.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class Event:
    """Simple event payload.

    Attributes
    ----------
    type: str
        Identifier for the kind of event (e.g., "global_tick").
    payload: Any
        Arbitrary data associated with the event.
    timestamp: datetime
        Time the event was created; defaults to ``datetime.now()`` if not
        supplied.
    """

    type: str
    payload: Any
    timestamp: datetime = datetime.now()

    def __post_init__(self) -> None:
        # Ensure timestamp is a datetime instance; ``datetime.now()`` is used as
        # the default value but mypy treats mutable defaults specially, so we
        # normalise it here.
        if not isinstance(self.timestamp, datetime):
            self.timestamp = datetime.fromtimestamp(float(self.timestamp))
