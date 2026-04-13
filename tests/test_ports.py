import os
import yaml
import tempfile
from pathlib import Path

from vsm.ports.event_bus_port import EventBusPort
from vsm.ports.persistence_port import PersistencePort
from vsm.ports.llm_port import LLMPort
from vsm.ports.tool_port import ToolPort
from vsm.ports.scheduler_port import SchedulerPort
from vsm.ports.config_port import ConfigPort
from vsm.ports.rule_port import RulePort
from vsm.ports.turn_manager_port import TurnManagerPort
from vsm.ports.memory_port import MemoryPort

from vsm.adapters.in_process_bus import InProcessBus
from vsm.adapters.yaml_file_store import YamlFileStore
from vsm.adapters.local_llm_adapter import LocalLLMAdapter
from vsm.adapters.local_tool_registry import LocalToolRegistry
from vsm.adapters.simple_trigger_engine import SimpleTriggerEngine
from vsm.adapters.yaml_config_loader import YamlConfigLoader
from vsm.adapters.yaml_rule_adapter import YamlRuleAdapter
from vsm.adapters.yaml_memory_adapter import YamlMemoryAdapter
from vsm.adapters.in_memory_turn_manager import InMemoryTurnManager


def test_in_process_bus():
    bus = InProcessBus()
    events = []
    bus.subscribe("test", lambda e: events.append(e))

    class E:
        type = "test"

    bus.publish(E())
    assert len(events) == 1
    assert events[0].type == "test"


def test_yaml_file_store(tmp_path: Path):
    store = YamlFileStore(tmp_path / "store.yaml")
    store.save("k", {"v": 1})
    assert store.load("k") == {"v": 1}
    store.delete("k")
    assert store.load("k") is None


def test_local_llm_adapter():
    llm = LocalLLMAdapter()
    assert llm.generate("hi") == "generated: hi"
    msgs = [
        {"role": "user", "content": "hello"},
        {"role": "assistant", "content": "world"},
    ]
    assert llm.chat(msgs) == "chat: hello world"


def test_local_tool_registry():
    registry = LocalToolRegistry()
    registry.register("echo", lambda x: x)
    assert registry.list_tools() == ["echo"]
    assert registry.run("echo", 5) == 5
    try:
        registry.run("missing")
    except KeyError:
        pass
    else:
        assert False, "expected KeyError"


def test_simple_trigger_engine():
    engine = SimpleTriggerEngine()
    rule = type("R", (), {"id": "r1"})()
    engine.add_rule(rule)
    assert engine.list_rules() == [rule]
    engine.remove_rule("r1")
    assert engine.list_rules() == []


def test_yaml_config_loader(tmp_path: Path):
    cfg_path = tmp_path / "cfg.yaml"
    cfg_path.write_text(yaml.safe_dump({"a": 1, "b": 2}))
    loader = YamlConfigLoader(cfg_path)
    assert loader.load() == {"a": 1, "b": 2}


def test_yaml_rule_adapter(tmp_path: Path):
    adapter = YamlRuleAdapter(tmp_path / "rules.yaml")
    rule = {"id": "r1", "desc": "test"}
    adapter.add(rule)
    assert adapter.get_all() == [rule]
    adapter.remove("r1")
    assert adapter.get_all() == []


def test_yaml_memory_adapter(tmp_path: Path):
    mem = YamlMemoryAdapter(tmp_path / "mem.yaml")
    entry = {"type": "obs", "value": 5}
    mem.append(entry)
    all_entries = mem.load_all()
    assert len(all_entries) == 1
    e = all_entries[0]
    assert e["type"] == "obs"
    # query by field
    result = mem.query(type="obs")
    assert result == [e]
    # delete
    mem.delete(e["id"])
    assert mem.load_all() == []


def test_in_memory_turn_manager():
    tm = InMemoryTurnManager()
    tm.add_actor("a")
    tm.add_actor("b")
    assert tm.size() == 2
    assert tm.next_actor() == "a"
    assert tm.next_actor() == "b"
    tm.remove_actor("a")
    assert tm.size() == 1
    assert tm.next_actor() == "b"


def test_port_factory(tmp_path: Path):
    from vsm.ports.port_factory import PortFactory

    factory = PortFactory(base_path=tmp_path)
    ports = factory.create()
    # ensure each key exists and matches protocol types
    assert isinstance(ports["event_bus"], EventBusPort)
    assert isinstance(ports["persistence"], PersistencePort)
    assert isinstance(ports["llm"], LLMPort)
    assert isinstance(ports["tools"], ToolPort)
    assert isinstance(ports["scheduler"], SchedulerPort)
    assert isinstance(ports["config"], ConfigPort)
    assert isinstance(ports["rule"], RulePort)
    assert isinstance(ports["turn_manager"], TurnManagerPort)
    assert isinstance(ports["memory"], MemoryPort)
