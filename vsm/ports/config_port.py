"""Port contract for configuration loading.

Implementations typically read a configuration file (e.g., YAML) and expose the data as a dict.
"""

from typing import Protocol, Dict, Any, runtime_checkable


@runtime_checkable
class ConfigPort(Protocol):
    def load(self) -> Dict[str, Any]:
        """Load configuration data and return it as a dict."""
        ...
