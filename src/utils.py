import emoji
import torch
from zhconv import convert
from transformers import BertTokenizer
from datetime import datetime
from src.logger import logger 

def timer(func):
    def func_wrapper(*args, **kwargs):
        time_start = datetime.now()
        result = func(*args, **kwargs)
        time_end = datetime.now()
        time_spend = (time_end - time_start)
        logger.info(f'Function: {func.__name__}, start time: {time_start} - end time: {time_end}, cost time: {time_spend.seconds}S / {time_spend.microseconds/1000}ms')
        return result

    return func_wrapper

# ========================== Preprocessing ==========================
def remove_emoji(text):
    return emoji.replace_emoji(text, replace="")


def t2s(text):
    return convert(text, "zh-cn")


def remove_inprintable(text):
    return ''.join([x for x in text if x.isprintable()])


# ========================== words2ids, add masks ==========================
def add_keywords_to_text(text, keyword_list):
    matched_keywords = []
    for keyword in keyword_list:
        if keyword in text:
            matched_keywords.append(keyword)

    labels = list(set(matched_keywords))
    labels_ = []
    for i in labels:
        temp = labels.copy()
        temp.remove(i)
        flag = 1
        for j in temp:
            if i not in j:
                continue
            else:
                flag = 0
                break
        if flag:
            labels_.append(i)
    
    text_list = []
    separator = "。！？#?!"
    start, end = 0, 0
    while end < len(text):
        if text[end] in separator:
            text_list.append(text[start:end+1])
            start, end = end + 1, end + 1
        else:
            end += 1
        
        if end == len(text) - 1:
            text_list.append(text[start:end+1])

    for idx, t in enumerate(text_list):
        temp = []
        for l in labels_:
            if l in t:
                temp.append(l)
        if temp != []:
            text_list[idx] = text_list[idx] + '||可能的实体：' + ",".join(temp) + '||' 
    return "".join(text_list)


# @timer
def tokenize_single_text_and_add_masks(text, tokenizer,  max_len=512):
    # tokenizer = BertTokenizer.from_pretrained("/ailab/src/models/chinese-roberta-wwm-ext_tokenizer")
    tokenized_text, tokenized_content = [], []
    headline_content = text
    for char in headline_content:
        if tokenizer.tokenize(char):
            tokenized_text.append(char)
            tokenized_content.extend(tokenizer.tokenize(char))
        else:
            # 如果不存在字符，要原样保留，tokenizer.convert_tokens_to_ids会自动映射为特殊字符“[UNK]”
            tokenized_text.append(char)
            tokenized_content.extend(char)
    
    tokenized_content = [tokenizer.cls_token] + tokenized_content + [tokenizer.sep_token]
    if len(tokenized_content) > max_len: 
        tokenized_content = tokenized_content[:max_len]
        attn_mask = [1] * max_len
    else:
        tokenized_content = tokenized_content + [tokenizer.pad_token] * (max_len - len(tokenized_content))
        attn_mask = [1] * len(tokenized_content) + [0] * (max_len - len(tokenized_content))
    
    # attn_mask = [1 if tok != tokenizer.pad_token else 0 for tok in tokenized_content]
    ids = tokenizer.convert_tokens_to_ids(tokenized_content)

    return tokenized_text, ids, attn_mask


# @timer
def generate_single_input(text, keyword_list, tokenizer, add_keywords=False, max_len=512):
    """generate input given the text
    Args:
        arg: NameSpace, argumentation
        text: str, input text
    
    Returns:
        tokenized_content, ids, attn_mask: List
    """
    text = remove_emoji(text)
    text = t2s(text)
    text = remove_inprintable(text)
    # text = text.lower()

    if add_keywords:
        text = add_keywords_to_text(text, keyword_list)

    # 此前没问题
    tokenized_text, ids, attn_mask = tokenize_single_text_and_add_masks(text=text, tokenizer=tokenizer, max_len=max_len)
    ids, attn_mask = torch.tensor([ids], dtype=torch.long), torch.tensor([attn_mask], dtype=torch.long)

    return tokenized_text, ids, attn_mask


# @timer
def convert_labels_to_entity(entity_type_list, tokenized_text, label_pred):
    output = {label: [] for label in entity_type_list}
    tokenized_words = tokenized_text
    label_pred = label_pred
    start_idx, end_idx = -1, -1
    for idx, label in enumerate(label_pred):
        if label == 'O':
            if start_idx != -1:
                end_idx = idx
                # print(idx, entity_type, tokenized_words[start_idx:end_idx])
                output[entity_type].append("".join(tokenized_words[start_idx:end_idx]))
                start_idx, end_idx = -1, -1
            continue
        elif "B" in label:
            if start_idx != -1:
                end_idx = idx
                # print(idx, entity_type, tokenized_words[start_idx:end_idx])
                output[entity_type].append("".join(tokenized_words[start_idx:end_idx]))
                start_idx = idx
                entity_type = label.strip("B-")
            else:
                start_idx = idx
                entity_type = label.strip("B-")
        elif "I" in label:   
            if start_idx != -1:
                if entity_type != label.strip("I-"):
                    end_idx = idx
                    # print(idx, entity_type, tokenized_words[start_idx:end_idx])
                    output[entity_type].append("".join(tokenized_words[start_idx:end_idx]))
                    start_idx, end_idx = -1, -1
                else:
                    continue
            else:
                continue
    if start_idx != -1:
        end_idx = idx + 1
        output[entity_type].append("".join(tokenized_words[start_idx:end_idx]))
    output = {k: list(set([i for i in v if len(i)>1])) for (k, v) in output.items()}
    return output


def find_entity_index(text, entity):
    indices = []
    start = 0
    while True:
        start_index = text.find(entity, start)
        if start_index == -1:
            break
        end_index = start_index + len(entity)
        
        indices.append((start_index, end_index))
        start = end_index
    return indices

# @timer
def get_entity_index(text, pred_entity):
    text = text.lower()
    details = []
    for entity_type, entity_list in pred_entity.items():
        for entity in set(entity_list):
            indices = find_entity_index(text, entity)
            # details.append(
            #     {
            #         "entity_type": entity_type, 
            #         "entity": entity, 
            #         "index": indices
            #     })
            for (start_ind, end_ind) in indices:
                details.append(
                    {
                        "label_name": entity_type,
                        "text_segment": entity,
                        "start_ind": start_ind,
                        "end_ind": end_ind,
                        "resource": "Algorithm prediction"
                    })
    return details