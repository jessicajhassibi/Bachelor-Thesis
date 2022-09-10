import json
import os
from typing import List

import numpy as np
from gensim import models
from tqdm import tqdm

model = models.KeyedVectors


def get_words_in_static_embeddings(kv_word2vec: models.KeyedVectors, words_list: List[List[str]], save_path: str):
    """
    Checks if words are in the vocab of the model. 
    Writes all words of the given list in a txt file in folder and all words existing in vocab in a json file.
    Out-directory: data/models/words
    :return: missing_words: dictionary of missing words in the vocabulary and their count
    """
    vocab = kv_word2vec.index_to_key
    embedding_dict = dict()
    all_words_str = "Word\tIn_Model\n"
    missing_words = dict()
    all_words = []
    for words in tqdm(words_list, desc="Check which words are in the static embeddings of the model"):
        all_words += words
        for one_word in words:
            one_word = one_word.lower()
            if one_word in vocab:
                all_words_str += f"{one_word}\tTrue\n"
                embedding_dict[one_word] = kv_word2vec.get_vector(one_word)
            else:
                all_words_str += f"{one_word}\tFalse\n"
                missing_words[one_word] = missing_words.get(one_word, 0) + 1
    print(len(all_words), "words given.")
    print(f"Number of one words in model: {len(embedding_dict)}/{len(all_words)}")
    print(f"Number of missing words in model: {len(missing_words)}/{len(all_words)}")
    word_array = np.array(list(embedding_dict.keys()))
    embedding_array = np.array(list(embedding_dict.values()))
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    out_words_dir = save_path.replace(".npz", ".txt")
    with open(out_words_dir, "w", encoding="UTF-8") as txt_file:
        txt_file.write(all_words_str)
    np.savez(save_path, word=word_array, embeddings=embedding_array)
    out_list_dir = out_words_dir.replace(".txt", ".json")
    with open(out_list_dir, "w", encoding="UTF-8") as json_file:
        json.dump(words_list, json_file)
    return missing_words


def load_word2vec_keyed_vectors(path):
    """
    load the model from a path
    :param path: path of the file
    :return: Word2vec model
    """
    try:
        # C format:
        loaded_model = model.load_word2vec_format(path, binary=False)
    except:
        # .kv file
        loaded_model = model.load(path)
    print("Model: ", path, " loaded")
    return loaded_model
