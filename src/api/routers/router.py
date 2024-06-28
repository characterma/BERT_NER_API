from typing import List

from fastapi import Body
from fastapi.responses import JSONResponse

from src.api.model.ner_doc import InputSchema, examples, ResultSchema
from src.base.model import ModelPath
from src.base.router import APIRouter
from src.base.schema import APIResponse, ResponseSchema
# from src.infer import BERT_NER
from src.api.bussiness_entity_extract import Bussiness_Entity_Match_And_NER


router = APIRouter()

NerResponse = ResponseSchema("NerResponse", ret_data=ResultSchema)

# model = BERT_NER()

entity_extractor = Bussiness_Entity_Match_And_NER()

@router.post("/ner/content", tags=['extract entity in the content'])
async def single(body: InputSchema = Body(..., examples=examples)):
    """ ### <u>NER Model API</u>

    **URL: /ner/single**

    **Type: POST**

    **Description**

    1. Complete the NER task with a BERT backbone model.
    2. Support Chinese text preprocessing mainly. English words are processed in character level.

    """

    result = entity_extractor.predict_content(content=body.content, add_keywords=body.add_keywords)

    res = NerResponse(
        retData = {
            "docid": body.docid,
            "text": result
        }
    )
    return res

# @router.post("/")
# async def single(body: InputSchema = Body(..., examples=examples)):
#     """Sample endpoint.

#     Args:
#         body (Doc, optional): Input Doc class which include docid, content, headline. Defaults to Body(..., examples=examples).

#     Returns:
#         Dict: Single sample response with standard key(retCode, retInfo, retData).
#     """
#     text = body.content

#     result = onnx_ner(text)

#     res = JSONResponse(
#         status_code=200,
#         content={
#             "message": "OK",
#             "data": result,
#         }
#     )
#     return res



# @router.post("/batch", response_model=List[SentiResult])  # Use typing.List
# def batch(body: Doc = Body(..., examples=examples)):
#     """Sample endpoint.  return a List of SentiResult in key `retData`.

#     Args:
#         body (Doc, optional): Input Doc class which include docid, content, headline. Defaults to Body(..., examples=examples).

#     Returns:
#         Dict: Batch sample response with standard key(retCode, retInfo, retData).
#     """
#     _ = ModelPath("tiny_model.sample", "weight.sample").open("r")  # ModelPath sample
#     # Use APIResponse to package your response data with interface.
#     res = APIResponse(
#         retCode="W",  # Optional, default S
#         retInfo=f"Response example of:\n docid:{body.docid}, headline: {body.headline},content: {body.content}",  # Optional, default OK
#         retData=[
#             {
#                 "score": 0.9769629240036011,
#                 "scores": {
#                     "positive": 0.9769629240036011,
#                     "neutral": 0.012471978552639484,
#                     "negative": 0.01056508906185627,
#                 },
#                 "label": "positive",
#             }
#         ],
#     )
#     # or create your own response dictionary
#     res = {
#         "retCode": "W",  # Optional, default S
#         "retInfo": f"Response example of:\n docid:{body.docid}, headline: {body.headline},content: {body.content}",  # Optional, default OK
#         "retData": [
#             {
#                 "score": 0.9769629240036011,
#                 "scores": {
#                     "positive": 0.9769629240036011,
#                     "neutral": 0.012471978552639484,
#                     "negative": 0.01056508906185627,
#                 },
#                 "label": "positive",
#             }
#         ],
#     }
#     return res
