def test_health_check(client):
    resp = client.get(
        "/healthz",
    )
    assert resp.status_code == 200
    assert not resp.text == str({"status": "OK"})
    assert resp.json() == {"status": "OK"}


def test_post_(client):
    payload = {"data": "test"}
    resp = client.post("/test", json=payload)
    assert resp.status_code == 200
    assert resp.json() == payload
