from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_analyse_route_returns_json():
    response = client.post(
        "/analyse/",
        files={"file": ("data.csv", b"a,b,c", "text/csv")},
        data={"vraag": "test"},
    )
    assert response.status_code == 200
    assert response.json()["bestand"] == "data.csv"


def test_spp_route_excel_output():
    response = client.post(
        "/spp/?formaat=excel",
        files={"file": ("data.csv", b"a,b,c", "text/csv")},
    )
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/vnd.openxml")


def test_feedback_route():
    response = client.post(
        "/feedback/",
        data={"gebruiker": "tester", "bericht": "goed"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "opgeslagen"
