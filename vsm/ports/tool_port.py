"""Port contract for callable tools available to agents.

Tools are identified by name and invoked with arbitrary arguments.
"""

from typing import Protocol, List, Any, runtime_checkable


@runtime_checkable
class ToolPort(Protocol):
    def list_tools(self) -> List[str]:
        """Return the names of registered tools."""
        ...

    def run(self, name: str, *args: Any, **kwargs: Any) -> Any:
        """Execute the tool ``name`` with provided arguments."""
        ...
