import json
import sys
from typing import Dict, List


sys.path.append(".")

from random import shuffle

import diskcache as dc
from commonlib.data_manager.query_helper import LinkedField, ListQuery, UapEnv
from locust import HttpUser, tag, task


access_token = "eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyaWQiOiIzIiwibmFtZSI6Imx1a2VjaHUiLCJ1c2VybmFtZSI6Imx1a2VjaHUiLCJyb2xlIjoi" \
               "YWRtaW4iLCJyYW5kb20iOjg4Mjg3MjA3MDkxMjk2Njc5NDUsImlzcyI6InVhcCBkbWdyIiwic3ViIjoiYWNjZXNzIGNvbnRyb2wiL" \
               "CJpYXQiOjE2MjMxNDYzMjR9.tKFKmExBeY6dr_Jr9eDvH0s-OvJeB6JrUBY9yT8Q_nM"
disk_cache = dc.Cache("tmp")
memory_cache = {}
_first = False


def loadtest_fixture(name, extra_params=None, use_diskcache=False):
    def decorator(func):
        def wrap():
            cache = memory_cache if not use_diskcache else disk_cache
            if not _first:
                # Clear disk cache
                disk_cache.clear()

            if cache.get(name) is not None:
                # Get data in cache by args `name`
                data = cache.get(name)
            else:
                # Get data by `func` and save cache
                data = func()
                disk_cache[name] = data
            if extra_params is not None:
                data = sum([[dict(**i, **j) for i in data] for j in extra_params], [])
            shuffle(data)
            return data

        return wrap

    return decorator

@loadtest_fixture("from_data_manager", extra_params=[{"a": 1}, {"a": 2}])
def get_test_data_from_dm():
    data = []
    qo = ListQuery("WisersDocDataset", env=UapEnv.UAT)
    qo.filter('name:{eq:"API Loading Test"} version:{eq:"1.0"}')
    qo.rtn_linked_fields([
         LinkedField("HasWisersDocs", force_rtn_id=False).rtn_fields("docid content").filter('content:{len_lt:300}').
             iterate(req_max=-1, step_size=500),
        ])
    for res, _ in qo.exec_query():
        data += res[0].get('HasWisersDocs')
    return data

@loadtest_fixture("from_local_file")
def get_test_data_from_local_file() -> List[Dict]:
    with open("./load-test/sample_test_data.txt", "r", encoding="utf8") as f:
        raw = f.read()
        data = json.loads(raw)
    return data 

class LocustUser(HttpUser):
    @tag('/ner/single')  # endpoint name
    @task
    # def test_from_dm(self):
    #     for data in get_test_data_from_dm():
    #     # for data in get_test_data_from_local_file(): # Can swtich to local test data
    #         self.client.post(
    #             url="/ner/single",  # endpoint name
    #             json=data,
    #             name="/ner/single"  # endpoint name
    #         )
    
    def test_predict_single(self):
        docid = "202401081815"
        content = "星巴克的抹茶星冰乐好好喝啊，但是芝士拿铁好苦。"

        payload = {
            "docid": docid
            "content": content
        }
        self.client.post(
            url="/ner/single", 
            json=payload, 
            name="/ner/single"
        )
    
