from src.api.model.doc import doc_example_1


prefix = "/nonstandard/sample"
payload = doc_example_1["value"].dict()


def test_single(client):
    resp = client.post(f"{prefix}/single", json=payload)
    resp_data = resp.json()
    assert resp.status_code == 200
    assert resp_data == {
        "score": 0.9769629240036011,
        "scores": {
            "positive": 0.9769629240036011,
            "neutral": 0.012471978552639484,
            "negative": 0.01056508906185627,
        },
        "label": "positive",
    }


def test_batch(client):
    resp = client.post(f"{prefix}/batch", json=payload)
    resp_data = resp.json()
    assert resp.status_code == 200
    assert type(resp_data) is list
    assert resp_data[0] == {
        "score": 0.9769629240036011,
        "scores": {
            "positive": 0.9769629240036011,
            "neutral": 0.012471978552639484,
            "negative": 0.01056508906185627,
        },
        "label": "positive",
    }
