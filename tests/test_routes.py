from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_upload_route_returns_analysis(tmp_path):
    file_content = b"dummy content for upload"
    response = client.post(
        "/upload/",
        files={"file": ("dummy.txt", file_content, "text/plain")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "verkorte_analyse" in data


def test_legalcheck_route_with_keywords(tmp_path):
    text = "Dit document gaat over ontslag en verzuim en heeft voldoende lengte."
    response = client.post("/legalcheck/", files={"file": ("dummy.txt", text.encode(), "text/plain")})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "ontslag" in data["herkenning_kernwoorden"]
    assert "verzuim" in data["herkenning_kernwoorden"]
    assert data["legal_markdown"].startswith("## Juridische Analyse")


def test_batch_upload_route_returns_list(tmp_path):
    file1 = b"first file"
    file2 = b"second file"
    response = client.post(
        "/batch_upload/",
        files=[
            ("files", ("a.txt", file1, "text/plain")),
            ("files", ("b.txt", file2, "text/plain")),
        ],
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert all(item.get("status") == "ok" for item in data)


def test_analyse_text_endpoint():
    response = client.post("/analyse_text/", data={"text": "een korte analyse"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
