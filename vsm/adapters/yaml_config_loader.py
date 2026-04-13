"""YAML‑based config loader implementing ``ConfigPort``.

The loader reads a YAML file at construction time and returns its contents via ``load``.
"""

import yaml
from pathlib import Path
from typing import Dict, Any
from ..ports.config_port import ConfigPort


class YamlConfigLoader(ConfigPort):
    def __init__(self, path: str | Path):
        self.path = Path(path)
        if not self.path.exists():
            raise FileNotFoundError(self.path)

    def load(self) -> Dict[str, Any]:
        with self.path.open() as f:
            return yaml.safe_load(f) or {}
