from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_upload_route_returns_empty_dict(tmp_path):
    file_content = b"dummy content for upload"
    response = client.post("/upload/", files={"file": ("dummy.txt", file_content, "text/plain")})
    assert response.status_code == 200
    assert response.json() == {}


def test_batch_upload_returns_empty_list(tmp_path):
    files = [
        ("files", ("dummy1.txt", b"data1", "text/plain")),
        ("files", ("dummy2.txt", b"data2", "text/plain")),
    ]
    response = client.post("/batch_upload/", files=files)
    assert response.status_code == 200
    assert response.json() == []


def test_legalcheck_route_with_keywords(tmp_path):
    text = "Dit document gaat over ontslag en verzuim en heeft voldoende lengte."
    response = client.post("/legalcheck/", files={"file": ("dummy.txt", text.encode(), "text/plain")})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "ontslag" in data["herkenning_kernwoorden"]
    assert "verzuim" in data["herkenning_kernwoorden"]
    assert data["legal_markdown"].startswith("## Juridische Analyse")

