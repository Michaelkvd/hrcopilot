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


def test_spp_route_json_grid_keys():
    response = client.post(
        "/spp/?formaat=json",
        files={"file": ("data.csv", b"a,b,c", "text/csv")},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["grid"]) == 9


def test_spp_auto_category_mapping():
    csv = "laag_potentieel_lage_prestatie,hoog_potentieel_hoge_prestatie\n1,2\n"
    response = client.post(
        "/spp/?formaat=json",
        files={"file": ("spp.csv", csv.encode(), "text/csv")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["grid"]["onderpresteerder"] == 1
    assert data["grid"]["ster"] == 2


def test_spp_text_input():
    csv = "laag_potentieel_lage_prestatie,hoog_potentieel_hoge_prestatie\n1,1\n"
    response = client.post(
        "/spp/?formaat=json",
        data={"text": csv},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["grid"]["onderpresteerder"] == 1
    assert data["grid"]["ster"] == 1


def test_feedback_route_requires_admin():
    response = client.post(
        "/feedback/",
        data={"gebruiker": "tester", "bericht": "goed"},
    )
    assert response.status_code == 403


def test_feedback_route_with_admin():
    response = client.post(
        "/feedback/",
        data={"gebruiker": "admin", "bericht": "goed"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "opgeslagen"


def test_legalcheck_risk_and_sources():
    text = "Dit document bespreekt langdurig verzuim en mogelijke ontslagprocedures." * 5
    response = client.post(
        "/legalcheck/",
        files={"file": ("doc.txt", text.encode(), "text/plain")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["risico"] in {"laag", "matig", "hoog"}
    assert data["bronnen"]
    for hits in data["bronnen"].values():
        for url, _ in hits:
            assert url.startswith("http")
