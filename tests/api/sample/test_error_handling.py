prefix = "/error_handling/sample"


def test_arr_exc_handl_sample(client):
    url = f"{prefix}/attention_required_response/"
    resp = client.get(url)
    assert resp.json()["retCode"] == "W-1"


def test_psr_exc_handl_sample(client):
    url = f"{prefix}/partial_success_response/"
    resp = client.get(url)
    assert resp.json()["retCode"] == "W-2"


def test_iiel_exc_handl_sample(client):
    url = f"{prefix}/invalid_inputs_exception/lang/"
    data = {"docid": "docid123", "headline": "Sample", "content": "Sample."}
    resp = client.post(url, json=data)
    assert resp.status_code == 400
    assert resp.json()["retCode"] == "Sch-2"


def test_iiec_exc_handl_sample(client):
    url = f"{prefix}/invalid_inputs_exception/char/"
    data = {"docid": "docid123", "headline": "Sample", "content": "@Sample."}
    resp = client.post(url, json=data)
    assert resp.status_code == 400
    assert resp.json()["retCode"] == "Sch-2"


def test_ede_db_exc_handl_sample(client):
    url = f"{prefix}/external_dependency_exception/db/"
    resp = client.get(url)
    assert resp.status_code == 500
    assert resp.json()["retCode"] == "DB-1"


def test_ede_api_exc_handl_sample(client):
    url = f"{prefix}/external_dependency_exception/api/"
    resp = client.get(url)
    assert resp.status_code == 500
    assert resp.json()["retCode"] == "Ext-1"


def test_ipe_exc_handl_sample(client):
    url = f"{prefix}/internal_program_exception/"
    resp = client.get(url)
    assert resp.status_code == 500
    assert resp.json()["retCode"] == "Pgrm-1"


def test_psr_exc_handl_sample(client):
    url = f"{prefix}/validation_error/"
    data = {"docid": "docid123", "headline": "Sample", "content": "Sample."}
    resp = client.post(url, json=data)
    assert resp.status_code == 500
    assert resp.json()["retCode"] == "Pgrm-1"
