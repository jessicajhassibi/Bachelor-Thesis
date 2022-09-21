from pathlib import Path
from top2vec import Top2Vec
from bertopic import BERTopic
from data import get_documents_list, get_topic_modeling_path
from data import get_top2vec_embedding_model
from data import get_languages
from data import get_full_language_word
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
        top2vec_model = Top2Vec.load(top2vec_model_path)
    except Exception as err:
        print("Top2Vec model not found.")
        print("Training new model...")
        multilingual_documents = get_documents_list(text_type)
        top2vec_model = Top2Vec(multilingual_documents, verbose=True, ngram_vocab=True,
                                embedding_model=get_top2vec_embedding_model())
        top2vec_model.save(top2vec_model_path)
    return top2vec_model


def get_BERTopic_model(text_type: str) -> BERTopic:
    """
    Loads and returns BERTopic model if already existing.
    If not, train a new model and save before returning it.
    """
    topic_models_path: Path = Path(get_topic_modeling_path())
    languages_string = "_".join(get_languages())
    top2vec_model_path = topic_models_path.joinpath(f"BERTopic_{languages_string}_{text_type}")
    if len(get_languages()) > 1:
        language_model = "multilingual"
    else:
        language = get_languages()[0]
        language_model = get_full_language_word(language)
    try:
        topic_model = BERTopic.load(top2vec_model_path)
    except Exception as err:
        print("BERTopic model not found.")
        print("Training new model...")
        # use cleaned documents
        documents_cleaned = get_documents_list('cleaned_paragraphs')
        vectorizer_model = CountVectorizer(ngram_range=(1, 2))
        topic_model = BERTopic(verbose=True, language=language_model, vectorizer_model=vectorizer_model)
        topics, probs = topic_model.fit_transform(documents_cleaned)
        topic_model.save(top2vec_model_path)
    return topic_model