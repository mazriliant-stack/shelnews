from fastapi.testclient import TestClient

from shelnews.app import app

client = TestClient(app)


def test_classify_endpoint():
    r = client.post("/classify", json={"headline": "US Treasury Buyback Results"})
    assert r.status_code == 200
    assert r.json() == {"categories": ["macro"], "highlights": [], "noise": None}


def test_classify_noise():
    r = client.post("/classify", json={"headline": "$VKTX shares at lows -4.7% around $31 level"})
    assert r.json()["noise"] == "market_commentary"
