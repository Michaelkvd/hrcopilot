from agents import MainAgent


def test_workflow_handles_multiple_steps():
    agent = MainAgent()
    result = agent.workflow.handle(text="Ontslag traject\nVerzuim stijgt")
    steps = result["stappen"]
    assert len(steps) == 2
    assert steps[0]["agent"] == "legal"
    assert steps[1]["agent"] == "absence"
