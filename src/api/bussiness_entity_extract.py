import json
from langchain_text_splitters import RecursiveCharacterTextSplitter
from zhconv import convert

import sys
sys.path.insert(0, '/workspace/ner-starbucks')

from src.infer import BERT_NER
from src.api.keyword_match import KeyWordExtractor
from src.utils import get_entity_index, timer
from src.base.configs import get_conf

class Bussiness_Entity_Match_And_NER:
    def __init__(self, 
                 # use_fixed=True
                ):
        # read company entity file 
        self.use_fixed = get_conf("COMPANY_ENTITY")["USE_FIXED"]
        self.company_file_path = get_conf("COMPANY_ENTITY")["ENTITY_FILE_PATH"]
        self.company_entities = {convert(key, 'zh-cn').lower(): value for key, value in json.load(open(self.company_file_path, 'r', encoding='utf-8')).items()}
        print(f"company entities: {len(self.company_entities)}")
        self.key_word_extrator = KeyWordExtractor(dictionary=list(self.company_entities.keys()), use_fixed=self.use_fixed)
        self.model = BERT_NER()
        self.max_len = get_conf("MODEL")["MAX_LEN"]

        
        self.text_splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n", "。", "！", "!", "？", "?", "；", ";"],
            chunk_size=self.max_len,
            chunk_overlap=100,
            length_function=len
        )
    
    @timer
    def evaled_entity_match(self, content, ner_company):
        """
        Dictionary matching, evaled company entity dictionary
        """
        dictionary_match_res = self.key_word_extrator.extract(content)
        dictionary_match_response = [{
            "label_name": "Company",
            "text_segment": entity,
            "start_ind": start_ind,
            "end_ind": end_ind,
            "resource": "Dictionary matching"
        } for (entity, start_ind, end_ind) in dictionary_match_res if entity not in ner_company]
        return dictionary_match_response
        
    # @timer
    def NER_predict(self, content, add_keywords=False):
        """
        Algorithm prediction, (bert ner model)
        """
        text_list = self.text_splitter.split_text(content)
        content_ner_result = {}
        for text in text_list:
            text_ner_result = self.model.predict(text, add_keywords)
            for key, value in text_ner_result.items():
                if key in content_ner_result:
                    content_ner_result[key].extend(value)
                else:
                    content_ner_result[key] = value
        ner_companys = set(content_ner_result['Company'])
        NER_response = get_entity_index(content, content_ner_result)
        return NER_response, ner_companys
    
    # @timer
    def predict_content(self, content, add_keywords=False, **kwargs):
        """
        extract entity from content
        """
        content = convert(content, 'zh-cn').lower()
        NER_response, ner_companys = self.NER_predict(content)
        dictionary_match_response = self.evaled_entity_match(content, ner_companys)
        
        # 将以上两个环节识别到的实体，进行合并，并通过起始索引进行排序
        complete_entity_info = dictionary_match_response + NER_response
        
        # complete_entity_info = NER_response

        final_entity_response = sorted(complete_entity_info, key=lambda dic: dic['start_ind'])
        return final_entity_response
        
if __name__ == "__main__":
    input_ = {
        "docid": "202401081815",
        "content": "抹茶星冰乐真好喝啊，但是芝士拿铁好苦，所以我还是喜欢摩卡星冰乐。#星巴克 #蜜雪冰城",
        "add_keywords": True
    }
    # input_ = {
    #     "docid": "2023050400008799690",
    #     "content": "中国人民银行 最高人民法院 最高人民检察院 中华人民共和国公安部 中国银行保险监督管理委员会公告〔2023〕第7号 ",
    #     "add_keywords": False
    # }

    # input_ = {
    #     "docid": "202401081815",
    #     "content": "抹茶星冰乐真好喝啊，但是芝士拿铁好苦，所以我还是喜欢摩卡星冰乐。#星巴克 #蜜雪冰城"
    # }

    model = Bussiness_Entity_Match_And_NER()
    # print(model.predict_single(input_))
    
    print(model.predict_content(input_['content']))
