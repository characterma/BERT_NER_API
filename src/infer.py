import argparse
import torch
import numpy as np
import pandas as pd
from tqdm import tqdm
from torch import cuda
import json
from transformers import BertTokenizer, BertForTokenClassification

import sys
sys.path.insert(0, '/workspace/ner-starbucks')
from src.base.configs import get_conf
from src.utils import *
from src.logger import logger
from langchain_text_splitters import RecursiveCharacterTextSplitter


class BERT_NER():
    def __init__(self):
        ## setting
        self.labels_to_ids_path, self.ids_to_labels_path = get_conf("MAPPING")["LABELS_TO_IDS"], get_conf("MAPPING")["IDS_TO_LABELS"]
        self.labels_to_ids = json.load(open(self.labels_to_ids_path, 'r', encoding='utf-8'))
        self.ids_to_labels = {int(id): label for id, label in json.load(open(self.ids_to_labels_path, 'r', encoding='utf-8')).items()}
        print(self.labels_to_ids, self.ids_to_labels)
        self.entity_types = list(set(label_name.split("-")[1] for label_name in self.labels_to_ids.keys() if "-" in label_name and "O" != label_name))
        self.device = get_conf("APP")["DEVICE"]
        self.num_labels = len(self.labels_to_ids)
        self.max_len = get_conf("MODEL")["MAX_LEN"]
        
        self.company_file_path = get_conf("COMPANY_ENTITY")["ENTITY_FILE_PATH"]
        self.keyword_list = list(json.load(open(self.company_file_path, 'r', encoding='utf-8')).keys())
        
        ## tokenizer
        self.tokenizer_path = get_conf("MODEL")["TOKENIZER_PATH"]
        self.tokenizer = BertTokenizer.from_pretrained(self.tokenizer_path)

        ## pretrained_model
        self.pretrained_model_path = get_conf("MODEL")["PRETRAINED_MODEL_PATH"]
        self.model = BertForTokenClassification.from_pretrained(self.pretrained_model_path, num_labels=self.num_labels)
        
        ## model
        self.model_path = get_conf("MODEL")["MODEL_PATH"]
        self.model.load_state_dict(torch.load(self.model_path))
        # self.model.load_state_dict(torch.load("/workspace/ner-starbucks/src/models/model.pth"))
        
        ## device
        self.model.to(self.device)
        
        ## placeholder
        self.placeholder = set(['[CLS]', '[SEP]', '[PAD]'])


        ## text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n", "。", "！", "!", "？", "?", "；", ";"],
            chunk_size=self.max_len,
            chunk_overlap=100,
            length_function=len
        )

    def predict(self, text, add_keywords=False):
        """
        Perform entity extraction on the input text
        """
        tokenized_text, ids, masks = generate_single_input(text, self.keyword_list, self.tokenizer, add_keywords, self.max_len)
        ids, masks = ids.to(self.device), masks.to(self.device)

        output = self.model(input_ids=ids, attention_mask=masks, return_dict=True)
        output = output['logits']

        pred_labels = torch.argmax(output, dim=2).cpu().tolist() # (batchsize, seq_len)
        pred_labels = [self.ids_to_labels[j] for i in pred_labels for j in i] # list

        tokens = [self.tokenizer.convert_ids_to_tokens(i) for i in ids.squeeze().cpu().tolist()]
        p_l_temp = []
        for pair in zip(tokens, pred_labels):
            if pair[0] in self.placeholder:
                continue
            else:
                p_l_temp.append(pair[1])

        pred_entity = convert_labels_to_entity(self.entity_types, tokenized_text, p_l_temp)
        return pred_entity
        

    def predict_single(self, input_data):
        # print(input_data)
        docid = input_data['docid']
        texts = input_data['content']
        add_keywords = input_data.get("add_keywords", True)

        text_list = self.text_splitter.split_text(texts)
        output_dict = {"docid": docid, "entity":{entity_type: [] for entity_type in self.entity_types}}

        for text in text_list:
            tokenized_text, ids, masks = generate_single_input(text, self.keyword_list, self.tokenizer, add_keywords, self.max_len)
            # print("".join(tokenized_text))
            ids, masks = ids.to(self.device), masks.to(self.device)

            output = self.model(input_ids=ids, attention_mask=masks, return_dict=True)
            output = output['logits']

            pred_labels = torch.argmax(output, dim=2).cpu().tolist() # (batchsize, seq_len)
            pred_labels = [self.ids_to_labels[j] for i in pred_labels for j in i] # list

            tokens = [self.tokenizer.convert_ids_to_tokens(i) for i in ids.squeeze().cpu().tolist()]

            p_l_temp = []
            for pair in zip(tokens, pred_labels):
                if pair[0] in self.placeholder:
                    continue
                else:
                    p_l_temp.append(pair[1])

            pred_entity = convert_labels_to_entity(self.entity_types, tokenized_text, p_l_temp)
            
            # output_dict["entity"].update(pred_entity)
            for entity_type in self.entity_types:
                output_dict["entity"][entity_type].extend(pred_entity[entity_type])
        
        for entity_type in self.entity_types:
            output_dict["entity"][entity_type] = list(set(output_dict["entity"][entity_type]))
        pred_entity = output_dict["entity"]

        ### add index
        details = get_entity_index(texts, pred_entity)
        output_dict.update({"details": details})

        return output_dict

    # ========================== utils ==========================
    def to_numpy(self, tensor):
        return tensor.detach().cpu().numpy() if tensor.requires_grad else tensor.cpu().numpy()


if __name__ == "__main__":
    # input_ = {
    #     "docid": "202401081815",
    #     "content": "抹茶星冰乐真好喝啊，但是芝士拿铁好苦，所以我还是喜欢摩卡星冰乐。#星巴克 #蜜雪冰城",
    #     "add_keywords": True
    # }
    input_ = {
        "docid": "2023050400008799690",
        "content": "中国人民银行 最高人民法院 最高人民检察院 中华人民共和国公安部 中国银行保险监督管理委员会公告〔2023〕第7号 ",
        "add_keywords": False
    }

    # input_ = {
    #     "docid": "202401081815",
    #     "content": "抹茶星冰乐真好喝啊，但是芝士拿铁好苦，所以我还是喜欢摩卡星冰乐。#星巴克 #蜜雪冰城"
    # }

    model = BERT_NER()
    print(model.predict_single(input_))
    
    print(model.predict(input_['content']))
