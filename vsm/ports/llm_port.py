"""Port contract for language‑model interaction.

Implementations expose a ``generate`` method for simple completions and a
``chat`` method for multi‑turn interactions.
"""

from typing import Protocol, List, Dict, Any, runtime_checkable


@runtime_checkable
class LLMPort(Protocol):
    def generate(self, prompt: str) -> str:
        """Return a completion for ``prompt``."""
        ...

    def chat(self, messages: List[Dict[str, Any]]) -> str:
        """Chat interface accepting a list of message dicts.

        ``messages`` follows the typical ``{"role": ..., "content": ...}`` schema.
        """
        ...
