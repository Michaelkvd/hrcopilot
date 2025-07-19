from agents import MainAgent
from utils.memory import Memory


def test_memory_persistence(tmp_path):
    path = tmp_path / "mem.json"
    mem = Memory(path)
    mem.add("user", {"data": 1})
    mem2 = Memory(path)
    assert mem2.get("user")[0]["data"] == 1


def test_main_agent_stores_in_memory(tmp_path):
    path = tmp_path / "mem.json"
    agent = MainAgent(memory_path=path)
    agent.auto_route("Het ziekteverzuim neemt toe", user="tester")
    assert agent.memory.get("tester")
