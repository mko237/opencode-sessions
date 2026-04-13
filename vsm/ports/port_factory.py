"""Factory that creates concrete adapter instances for each abstract port.

The factory wires default implementations together so that callers can obtain a
single object with ready‑to‑use ports.
"""

from pathlib import Path

from ..ports.event_bus_port import EventBusPort
from ..ports.persistence_port import PersistencePort
from ..ports.llm_port import LLMPort
from ..ports.tool_port import ToolPort
from ..ports.scheduler_port import SchedulerPort
from ..ports.config_port import ConfigPort
from ..ports.rule_port import RulePort
from ..ports.turn_manager_port import TurnManagerPort
from ..ports.memory_port import MemoryPort

# Concrete adapters
from ..adapters.in_process_bus import InProcessBus
from ..adapters.yaml_file_store import YamlFileStore
from ..adapters.local_llm_adapter import LocalLLMAdapter
from ..adapters.local_tool_registry import LocalToolRegistry
from ..adapters.simple_trigger_engine import SimpleTriggerEngine
from ..adapters.yaml_config_loader import YamlConfigLoader
from ..adapters.yaml_rule_adapter import YamlRuleAdapter
from ..adapters.yaml_memory_adapter import YamlMemoryAdapter
from ..adapters.in_memory_turn_manager import InMemoryTurnManager


class PortFactory:
    """Create and expose default adapter instances for all ports."""

    def __init__(self, base_path: str | Path = "./data") -> None:
        self.base = Path(base_path)
        self.base.mkdir(parents=True, exist_ok=True)

        # Event bus – shared instance
        self.event_bus: EventBusPort = InProcessBus()

        # Persistence – YAML file per key namespace
        self.persistence: PersistencePort = YamlFileStore(
            self.base / "persistence.yaml"
        )

        # LLM – simple stub
        self.llm: LLMPort = LocalLLMAdapter()

        # Tools – registry
        self.tools: ToolPort = LocalToolRegistry()

        # Scheduler – rule engine
        self.scheduler: SchedulerPort = SimpleTriggerEngine()

        # Config – ensure file exists then load
        cfg_path = self.base / "config.yaml"
        if not cfg_path.exists():
            cfg_path.write_text("{}")
        self.config: ConfigPort = YamlConfigLoader(cfg_path)
        # Ensure the config file exists – create an empty yaml if missing
        cfg_path = self.base / "config.yaml"
        if not cfg_path.exists():
            cfg_path.write_text("{}")

        # Rule storage
        self.rule: RulePort = YamlRuleAdapter(self.base / "rules.yaml")

        # Turn manager – simple round robin
        self.turn_manager: TurnManagerPort = InMemoryTurnManager()

        # Memory – per‑agent yaml log
        self.memory: MemoryPort = YamlMemoryAdapter(self.base / "memory.yaml")

    def create(self) -> dict:
        """Return a dict of port name → instance for easy injection."""
        return {
            "event_bus": self.event_bus,
            "persistence": self.persistence,
            "llm": self.llm,
            "tools": self.tools,
            "scheduler": self.scheduler,
            "config": self.config,
            "rule": self.rule,
            "turn_manager": self.turn_manager,
            "memory": self.memory,
        }
