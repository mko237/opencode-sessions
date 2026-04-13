"""Simple tool registry used by agents.

It implements the ``ToolPort`` protocol by storing callables in a dict.
"""

from typing import Callable, Dict, List, Any
from ..ports.tool_port import ToolPort


class LocalToolRegistry(ToolPort):
    def __init__(self) -> None:
        self._tools: Dict[str, Callable[..., Any]] = {}

    def register(self, name: str, fn: Callable[..., Any]) -> None:
        self._tools[name] = fn

    def list_tools(self) -> List[str]:
        return list(self._tools.keys())

    def run(self, name: str, *args: Any, **kwargs: Any) -> Any:
        if name not in self._tools:
            raise KeyError(f"Tool {name!r} not registered")
        return self._tools[name](*args, **kwargs)
