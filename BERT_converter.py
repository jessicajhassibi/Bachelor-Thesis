"""
Author: texttechnologylab
"""
import json
from transformers import AutoModel, AutoTokenizer
from sentence_transformers import SentenceTransformer


class BertConverter:
    def __init__(self, model_name='bert-base-uncased', device_number=0):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.device_number = device_number
        self.model = AutoModel.from_pretrained(model_name)#.to(device_number)
        self.model.eval()

    def encode(self, sentences, ret_input=False):
        if type(sentences) == str:
            sentences = [sentences]

        for c, sentence in enumerate(sentences):
            if len(sentence) > 0 and sentence[-1] != ".":
                sentences[c] = sentence + "."

        # arrays mit sentences als tensoren
        encoded_input = self.tokenizer(sentences, return_tensors='pt', padding=True, truncation=True, max_length=512)#.to(self.device_number)
        output = self.model(**encoded_input)
        if ret_input:
            return output, encoded_input
        else:
            return output

    def encode_to_vec(self, sentences):
        bert_results = self.encode(sentences)
        return bert_results.last_hidden_state[:, 0, :].detach().cpu().numpy().tolist()


class BertSentenceConverter:
    def __init__(self, model_name='all-MiniLM-L6-v2', device_number=0):
        self.model = SentenceTransformer(model_name)#.to(device_number)
        self.model.eval()

    def encode_to_vec(self, sentences, token=None, nlp=False):
        if type(sentences) == str:
            sentences = [sentences]

        for c, sentence in enumerate(sentences):
            if len(sentence) > 0 and sentence[-1] != ".":
                sentences[c] = sentence + "."

        embeddings = self.model.encode(sentences, convert_to_tensor=True)

        return embeddings.detach().cpu().numpy().tolist()




