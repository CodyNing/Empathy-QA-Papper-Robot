import argparse
import json
import os
from collections import OrderedDict
import torch
import csv
import util
from transformers import BertTokenizer, BertForQuestionAnswering


def QA(question):
    # device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    device = "cuda:0"
    checkpoint_path = os.path.join('./model/checkpoint')
    model = BertForQuestionAnswering.from_pretrained(checkpoint_path)
    tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
    model.to(device)
    model.eval()
    # question = "what do you think?"
    passage = ""
    input_ids = tokenizer.encode(question, passage)
    tokens = tokenizer.convert_ids_to_tokens(input_ids)
    sep_index = input_ids.index(tokenizer.sep_token_id)
    num_seg_a = sep_index + 1
    num_seg_b = len(input_ids) - num_seg_a
    segment_ids = [0]*num_seg_a + [1]*num_seg_b
    assert len(segment_ids) == len(input_ids)
    start_scores, end_scores = model(torch.tensor([input_ids]).to(device), token_type_ids=torch.tensor([segment_ids]).to(device), return_dict=False)
    answer_start = torch.argmax(start_scores)
    answer_end = torch.argmax(end_scores)
    answer = ' '.join(tokens[answer_start:answer_end+1])
    return answer
