from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app


def test_health_and_catalog_pages():
    with TestClient(app) as client:
        assert client.get("/health").json() == {"status": "ok"}
        response = client.get("/products")
        assert response.status_code == 200
        assert "Contractor Job Profit Tracker" in response.text
        assert client.get("/tools").status_code == 200


def test_demo_checkout_delivers_real_file():
    with TestClient(app, follow_redirects=False) as client:
        response = client.post("/checkout/contractor-job-profit-tracker")
        assert response.status_code == 303
        success = client.get(response.headers["location"])
        assert "Download now" in success.text
        link = success.text.split('href="/download/', 1)[1].split('"', 1)[0]
        download = client.get(f"/download/{link}")
        assert download.status_code == 200
        assert len(download.content) > 100


def test_admin_requires_token():
    with TestClient(app) as client:
        assert client.get("/admin").status_code == 401
        assert client.get("/admin?token=change-me-before-deploying").status_code == 200

