from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_upload_route_returns_analysis_dict(tmp_path):
    file_content = b"dummy content for upload"
    response = client.post(
        "/upload/",
        files={"file": ("dummy.txt", file_content, "text/plain")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "dummy.txt"
    assert data["sbi_code"] == "6420"
    assert "KW" in data["periode"]
    assert "risico" in data
    assert "advies" in data
    assert data["resultaat"] == "Analyse nog niet geïmplementeerd"


def test_batch_upload_returns_list_of_dicts(tmp_path):
    files = [
        ("files", ("dummy1.txt", b"data1", "text/plain")),
        ("files", ("dummy2.txt", b"data2", "text/plain")),
    ]
    response = client.post("/batch_upload/", files=files)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    for item in data:
        assert {
            "filename",
            "sbi_code",
            "periode",
            "resultaat",
            "risico",
            "advies",
            "verzuimpercentage",
            "cbs_benchmark",
        }.issubset(item.keys())


def test_legalcheck_route_with_keywords(tmp_path):
    text = "Dit document gaat over ontslag en verzuim en heeft voldoende lengte."
    response = client.post("/legalcheck/", files={"file": ("dummy.txt", text.encode(), "text/plain")})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "ontslag" in data["herkenning_kernwoorden"]
    assert "verzuim" in data["herkenning_kernwoorden"]
    assert data["legal_markdown"].startswith("## Juridische Analyse")
    assert data["verdiepende_vragen"]
    assert sum(len(h) for h in data["bronnen"].values()) >= 1


def test_legalcheck_accepts_msg_file(monkeypatch):
    from types import SimpleNamespace
    import legalcheck

    class DummyMsg:
        def __init__(self, path):
            self.subject = "Test"
            self.body = "Dit bericht noemt ontslag en is lang genoeg."

    monkeypatch.setattr(legalcheck, "extract_msg", SimpleNamespace(Message=DummyMsg))
    response = client.post(
        "/legalcheck/",
        files={"file": ("dummy.msg", b"binary", "application/vnd.ms-outlook")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["herkenning_kernwoorden"]


def test_upload_route_pdf_output(tmp_path):
    response = client.post(
        "/upload/?formaat=pdf",
        files={"file": ("dummy.txt", b"inhoud", "text/plain")},
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert len(response.content) > 10


def test_upload_route_chart_output(tmp_path):
    response = client.post(
        "/upload/?formaat=grafiek",
        files={"file": ("dummy.txt", b"inhoud", "text/plain")},
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"

