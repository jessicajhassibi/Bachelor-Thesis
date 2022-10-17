from pathlib import Path
from top2vec import Top2Vec
from bertopic import BERTopic
from data import get_documents_list, get_topic_modeling_path, get_top2vec_embedding_model, get_languages, \
    get_full_language_word, get_stop_words, get_dataframes
from sklearn.feature_extraction.text import CountVectorizer


def get_top2vec_model(text_type: str) -> Top2Vec:
    """
    Loads and returns top2vec model if already existing.
    If not, train a new model and save before returning it.
    """
    topic_models_path: Path = Path(get_topic_modeling_path())
    languages_string = "_".join(get_languages())
    top2vec_model_path = topic_models_path.joinpath(f"Top2Vec_{languages_string}_{text_type}")
    try:
        top2vec_model = Top2Vec.load(str(top2vec_model_path))
    except FileNotFoundError as err:
        print("Top2Vec model not found.")
        documents = get_documents_list(text_type)
        print(f"Training new model on {len(documents)} documents.")
        top2vec_model = Top2Vec(documents, verbose=True, ngram_vocab=True)
        print("Saving model.")
        top2vec_model.save(str(top2vec_model_path))
    return top2vec_model


def get_BERTopic_model(text_type: str) -> BERTopic:
    """
    Loads and returns BERTopic model if already existing.
    If not, train a new model and save before returning it.
    """
    topic_models_path: Path = Path(get_topic_modeling_path())
    languages_string = "_".join(get_languages())
    bertopic_model_path = topic_models_path.joinpath(f"BERTopic_{languages_string}_{text_type}")
    try:
        topic_model = BERTopic.load(bertopic_model_path)
    except Exception as err:
        print("BERTopic model not found.")
        # case A: model trained on monolingual datasets
        language = get_languages()[0]
        stopwords = get_stop_words(language)
        language_model = get_full_language_word(language)

        # case B: model trained on multilingual datasets
        if len(get_languages()) > 1:
            language_model = "multilingual"             # TODO: try sentence transformer distiluse-base-multilingual-cased
            for lang in get_languages()[1:]:
                stopwords.extend(get_stop_words(lang))

        documents = get_documents_list(text_type)
        print(f"Training new model on {len(documents)} documents.")
        vectorizer_model = CountVectorizer(ngram_range=(1, 2), stop_words=stopwords)
        topic_model = BERTopic(verbose=True, language=language_model, vectorizer_model=vectorizer_model)
        topics, probs = topic_model.fit_transform(documents)
        topic_model.save(bertopic_model_path)
        print(f"Loaded BERTopic model: {bertopic_model_path}")
    return topic_model

