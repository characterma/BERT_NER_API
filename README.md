# **NER model for Starbucks**
---
 
## Description
 
This is an NER API for Starbucks project. Target entities include coffee brand and coffee names.

## url
curl --location '{host}:{port}/ner/content'

## I/O format
Input1:
```json
{
  "docid": "202401081522",
  "content": "仅供测试使用，非真实：STARBUCKS的抹茶星冰乐真好喝啊，但是luckin的芝士拿铁好苦。#星巴克 #蜜雪冰城",
  "add_keywords": false
}
```
add_keywords: 默认不使用
NER打标："add_keywords": true
新品发现："add_keywords": false

Output1:
```json
{
    "retCode": "S",
    "retInfo": "OK",
    "retData": {
        "docid": "202401081522",
        "text": [
            {
                "label_name": "Company",
                "text_segment": "星巴克",
                "start_ind": 48,
                "end_ind": 51,
                "resource": "Dictionary matching"
            },
            {
                "label_name": "Company",
                "text_segment": "蜜雪冰城",
                "start_ind": 53,
                "end_ind": 57,
                "resource": "Dictionary matching"
            }
        ]
    }
}
```

Input2:
```json
{
    "docid": "202401081815",
    "content": "中国人民银行 最高人民法院 最高人民检察院 中华人民共和国公安部 中国银行保险监督管理委员会公告〔2023〕第7号 ",
    "add_keywords": "false"
}
```

Output2:
```json
{
    "retCode": "S",
    "retInfo": "OK",
    "retData": {
        "docid": "202401081815",
        "text": [
            {
                "label_name": "Company",
                "text_segment": "中国人民银行",
                "start_ind": 0,
                "end_ind": 6,
                "resource": "Dictionary matching"
            },
            {
                "label_name": "Company",
                "text_segment": "中国人民银行",
                "start_ind": 0,
                "end_ind": 6,
                "resource": "Algorithm prediction"
            },
            {
                "label_name": "Company",
                "text_segment": "最高人民法院",
                "start_ind": 7,
                "end_ind": 13,
                "resource": "Algorithm prediction"
            },
            {
                "label_name": "Company",
                "text_segment": "最高人民检察院",
                "start_ind": 14,
                "end_ind": 21,
                "resource": "Algorithm prediction"
            },
            {
                "label_name": "Company",
                "text_segment": "中华",
                "start_ind": 22,
                "end_ind": 24,
                "resource": "Dictionary matching"
            },
            {
                "label_name": "Company",
                "text_segment": "中华人民共和国公安部",
                "start_ind": 22,
                "end_ind": 32,
                "resource": "Algorithm prediction"
            },
            {
                "label_name": "Company",
                "text_segment": "中国银行",
                "start_ind": 33,
                "end_ind": 37,
                "resource": "Dictionary matching"
            },
            {
                "label_name": "Company",
                "text_segment": "中国银行保险监督管理委员会",
                "start_ind": 33,
                "end_ind": 46,
                "resource": "Algorithm prediction"
            }
        ]
    }
}
```

## Links


## Technologies
 
(optional: briefly describe core technologies used...)
 

## Launch Steps
 
(describe how to install/execute locally...)
 

## Notes
 
(optional: any notes or cautions...)
