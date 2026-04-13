"""In‑process event bus implementation.

This adapter satisfies the ``EventBusPort`` protocol defined in
``src/ports/event_bus_port.py``.  It stores a list of handlers per event type
and calls them synchronously when ``publish`` is invoked.
"""

from typing import Callable, Dict, List, Any
from ..ports.event_bus_port import EventBusPort


class InProcessBus(EventBusPort):
    def __init__(self) -> None:
        self._handlers: Dict[str, List[Callable[[Any], None]]] = {}

    def publish(self, ev: Any) -> None:
        ev_type = getattr(ev, "type", None)
        if ev_type is None:
            raise ValueError("Event object must have a 'type' attribute")
        for h in self._handlers.get(ev_type, []):
            h(ev)

    def subscribe(self, ev_type: str, handler: Callable[[Any], None]) -> None:
        self._handlers.setdefault(ev_type, []).append(handler)
