"""Abstract port definitions for the VSM system.

Each port is defined as a Python ``Protocol`` (PEP 544) to specify the required
methods without imposing inheritance constraints on concrete adapters.
"""

from typing import Protocol, Callable, Any, List, Dict


class PersistencePort(Protocol):
    """Port contract for key‑value persistence.

    Implementations must store arbitrary Python objects and retrieve them by a
    string key.
    """

    def save(self, key: str, obj: Any) -> None:
        """Persist ``obj`` under ``key``."""
        ...

    def load(self, key: str) -> Any:
        """Retrieve the object stored under ``key``."""
        ...

    def delete(self, key: str) -> None:
        """Remove the entry for ``key``."""
        ...


class LLMPort(Protocol):
    """Port contract for language‑model interaction.

    A minimal interface exposing a ``generate`` method that returns a string.
    """

    def generate(self, prompt: str) -> str:
        """Return a completion for ``prompt``."""
        ...

    def chat(self, messages: List[Dict[str, Any]]) -> str:
        """Chat interface accepting a list of message dicts."""
        ...


class ToolPort(Protocol):
    """Port contract for callable tools available to agents.

    Tools are identified by name and invoked with arbitrary arguments.
    """

    def list_tools(self) -> List[str]:
        """Return the names of registered tools."""
        ...

    def run(self, name: str, *args: Any, **kwargs: Any) -> Any:
        """Execute the tool ``name`` with provided arguments."""
        ...


class SchedulerPort(Protocol):
    """Port contract for scheduling rules or tasks.

    The scheduler receives rule objects (or similar) and triggers them at the
    appropriate time.
    """

    def add_rule(self, rule: Any) -> None:
        """Register a rule with the scheduler."""
        ...

    def remove_rule(self, rule_id: str) -> None:
        """Unregister a rule identified by ``rule_id``."""
        ...

    def list_rules(self) -> List[Any]:
        """Return all registered rules."""
        ...


class ConfigPort(Protocol):
    """Port contract for configuration loading.

    Implementations typically read a file (e.g., YAML) and expose the data as a
    dictionary.
    """

    def load(self) -> Dict[str, Any]:
        """Load configuration data."""
        ...


class RulePort(Protocol):
    """Port contract for rule storage and CRUD operations."""

    def add(self, rule: Any) -> None: ...

    def remove(self, rule_id: str) -> None: ...

    def get_all(self) -> List[Any]: ...


class TurnManagerPort(Protocol):
    """Port contract for round‑robin turn management."""

    def add_actor(self, actor_id: str) -> None: ...

    def remove_actor(self, actor_id: str) -> None: ...

    def next_actor(self) -> str: ...

    def size(self) -> int: ...


class MemoryPort(Protocol):
    """Port contract for per‑agent observation memory."""

    def append(self, entry: Any) -> None: ...

    def load_all(self) -> List[Any]: ...

    def query(self, **filters: Any) -> List[Any]: ...

    def delete(self, entry_id: str) -> None: ...
