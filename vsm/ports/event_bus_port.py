"""Abstract port definitions for the VSM system.

Each port is defined as a Python ``Protocol`` (PEP 544) so that concrete adapters can
implement the interface without needing to inherit from a base class.
"""

from typing import Protocol, Callable, Any, runtime_checkable


@runtime_checkable
class EventBusPort(Protocol):
    """Port contract for an event bus.

    Implementations must provide ``publish`` to emit an event and ``subscribe`` to
    register a handler for a specific event type.
    """

    def publish(self, ev: Any) -> None:
        """Emit an event onto the bus.

        ``ev`` can be any object representing an event; typically a dataclass with
        ``type`` and ``payload`` attributes.
        """
        ...

    def subscribe(self, ev_type: str, handler: Callable[[Any], None]) -> None:
        """Register ``handler`` to be called for events of ``ev_type``.

        ``handler`` receives the event object passed to ``publish``.
        """
        ...
