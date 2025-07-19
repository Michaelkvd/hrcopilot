from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_auto_route_multiple_agents(tmp_path):
    response = client.post(
        "/auto/",
        data={"text": "Het ziekteverzuim neemt toe en mogelijk ontslag"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "absence" in data
    assert "legal" in data


def test_auto_route_no_match():
    response = client.post("/auto/", data={"text": "geen relevantie"})
    assert response.status_code == 200
    assert response.json()["status"] == "geen match"
