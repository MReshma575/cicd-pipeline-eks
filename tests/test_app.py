from app import app


def test_index_returns_ok():
    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["service"] == "cicd-demo-app"
    assert body["status"] == "ok"


def test_health_returns_healthy():
    client = app.test_client()
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "healthy"
