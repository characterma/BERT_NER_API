from src.api.model.schema import doc_example_1


payload = doc_example_1["value"].dict()


def test_single(client):
    resp = client.post("ner/single", json=payload)
    resp_data = resp.json()
    assert resp.status_code == 200
    assert resp_data["content"]["message"] == "OK"
    assert resp_data["content"]["data"]["docid"] == "202401081815"
    assert resp_data["content"]["data"]["entity"]["miscellaneous"] == []
    assert resp_data["content"]["data"]["entity"]["brand"] == ["星巴克"]
    assert set(resp_data["content"]["data"]["entity"]["product"]) == set(["芝士拿铁", "抹茶星冰乐"])



# def test_batch(client):
#     resp = client.post(f"{prefix}/batch", json=payload)
#     resp_data = resp.json()
#     assert resp.status_code == 200
#     assert resp_data["retCode"] == "W"
#     assert (
#         resp_data["retInfo"]
#         == f'Response example of:\n docid:{payload["docid"]}, headline: {payload["headline"]},content: {payload["content"]}'
#     )
#     assert type(resp_data["retData"]) is list
#     assert resp_data["retData"][0] == {
#         "score": 0.9769629240036011,
#         "scores": {
#             "positive": 0.9769629240036011,
#             "neutral": 0.012471978552639484,
#             "negative": 0.01056508906185627,
#         },
#         "label": "positive",
#     }
