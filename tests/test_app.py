from fastapi.testclient import TestClient

from shelnews.app import app

client = TestClient(app)


def test_classify_endpoint():
    r = client.post("/classify", json={"headline": "US Treasury Buyback Results"})
    assert r.status_code == 200
    body = r.json()
    assert body["categories"] == ["macro"]
    assert body["highlights"] == []
