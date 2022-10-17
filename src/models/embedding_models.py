from gensim.models import Word2Vec, FastText
from pathlib import Path
from data import get_fasttext_models_path, get_word2vec_models_path, get_languages
from gensim import models


def get_embedding_model(train_data, text_type, method= "Word2Vec"):
    languages_string = "_".join(get_languages())
    if method == "Word2Vec":
        word2vec_models_path = get_word2vec_models_path.joinpath(f"Word2Vec_{languages_string}_{text_type}")
        try:
            model = Word2Vec.load(f"{word2vec_models_path}.model")
            # load model as KeyedVectors
            wv = models.KeyedVectors.load(f"{word2vec_models_path}.wordvectors")
        except FileNotFoundError as err:
            print("Word2Vec model not found.")
            print(f"Training new model on {len(train_data)} documents.")
            model = Word2Vec(sentences=train_data, vector_size= 100, window=5, min_count=2) # TODO: try different params
            print("Saving new model.")
            model.save(f"{word2vec_models_path}.model")
            # save model as KeyedVectors
            wv = model.wv
            wv.save(f"{word2vec_models_path}.wordvectors")
        print("Model: ", word2vec_models_path, " loaded")

    elif method == "fastText":
        fasttext_models_path = get_fasttext_models_path().joinpath(f"FastText_{languages_string}_{text_type}")
        try:
            model = Word2Vec.load(f"{fasttext_models_path}.model")
            # load model as KeyedVectors
            wv = models.KeyedVectors.load(f"{fasttext_models_path}.wordvectors")
        except FileNotFoundError as err:
            print("fastText model not found.")
            print(f"Training new model on {len(train_data)} documents.")
            model = FastText(sentences=train_data, vector_size= 100, window=5, min_count=2) # TODO: try different params
            print("Saving new model.")
            model.save(f"{fasttext_models_path}.model")
            # save model as KeyedVectors
            wv = model.wv
            wv.save(f"{fasttext_models_path}.wordvectors")
        print("Model: ", fasttext_models_path, " loaded")

    return model, wv
