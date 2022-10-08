from gensim.models import Word2Vec
from pathlib import Path
from data import get_classification_models_path, get_languages
from gensim import models


def get_word2vec_model(train_data, text_type):
    classification_models_path: Path = Path(get_classification_models_path())
    languages_string = "_".join(get_languages())
    word2vec_model_path = classification_models_path.joinpath(f"Word2Vec_{languages_string}_{text_type}")
    try:
        word2vec_model = Word2Vec.load(f"{word2vec_model_path}.model")
        # load model as KeyedVectors
        wv = models.KeyedVectors.load(f"{word2vec_model_path}.wordvectors")
    except FileNotFoundError as err:
        print("Word2Vec model not found.")
        print(f"Training new model on {len(train_data)} documents.")
        word2vec_model = Word2Vec(sentences=train_data, vector_size= 100, window=5, min_count=2) # try different params
        print("Saving new model.")
        word2vec_model.save(f"{word2vec_model_path}.model")
        # save model as KeyedVectors
        wv = word2vec_model.wv
        wv.save(f"{word2vec_model_path}.wordvectors")
    print("Model: ", word2vec_model_path, " loaded")
    return word2vec_model, wv
