from agents import MainAgent


def test_detects_legal_agent():
    agent = MainAgent()
    result = agent.detect_agent("Wij hebben vragen over een ontslagprocedure")
    assert result is agent.legal


def test_detects_absence_agent():
    agent = MainAgent()
    result = agent.detect_agent("Het ziekteverzuim loopt op")
    assert result is agent.absence


def test_detects_compliance_agent():
    agent = MainAgent()
    text = "Ons privacybeleid moet voldoen aan de AVG regels"
    result = agent.detect_agent(text)
    assert result is agent.compliance
