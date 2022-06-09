"""
Author: texttechnologylab
"""
import numpy as np
from typing import List, Dict, Any
from tqdm import tqdm
from gensim import models
import json
import gzip
import os

model = models.KeyedVectors

def get_word_in_static_embbedings(model_word2vec: models.KeyedVectors, words: List[str], save_path: str):
    words_list = []
    vocab = list(model_word2vec.index_to_key)
    embedding_dict = dict()
    all_words = "Word\tIn_Model\n"
    for one_word in tqdm(words, desc="Check which word are in the static embeddings"):
        if one_word.lower() in vocab:
            all_words += f"{one_word.lower()}\tTrue\n"
            words_list.append(one_word.lower())
            embedding_dict[one_word.lower()] = model_word2vec.get_vector(one_word.lower())
        else:
            all_words += f"{one_word.lower()}\tFalse\n"
    print(f"Number of one words in model: {len(embedding_dict)}/{len(words)}")
    word_array = np.array(list(embedding_dict.keys()))
    embedding_array = np.array(list(embedding_dict.values()))
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    out_words_dir = save_path.replace(".npz", ".txt")
    with open(out_words_dir, "w", encoding="UTF-8") as txt_file:
        txt_file.write(all_words)
    np.savez(save_path, word=word_array, embeddings=embedding_array)
    out_list_dir = out_words_dir.replace(".txt", ".json")
    with open(out_list_dir, "w", encoding="UTF-8") as json_file:
        json.dump(words_list, json_file)
        
def load_word2vec_model(path):
    """
    load the model from a path
    :param path: path of the file
    :return: Word2vec model
    """
    loaded_model = models.KeyedVectors.load_word2vec_format(path, binary=False)
    print("Model: ", path, " loaded")
    return loaded_model
