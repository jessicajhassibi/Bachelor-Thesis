from pathlib import Path


def get_config_ini_path() -> Path:
    return Path('../config.ini').resolve()


def get_target_path() -> Path:
    target_folder: Path = Path("../target").resolve()
    target_folder.mkdir(parents=True, exist_ok=True)
    return target_folder


def get_groups_target_path() -> Path:
    target_folder: Path = get_target_path().joinpath("groups").resolve()
    target_folder.mkdir(parents=True, exist_ok=True)
    return target_folder


def get_json_target_path(wiki_page, label, lang) -> Path:
    target_folder: Path = get_groups_target_path().joinpath(label)
    target_folder.mkdir(exist_ok=True)
    return target_folder.joinpath(f"{lang}_{wiki_page.replace(' ', '_')}.json").resolve()


def get_dataframes_path() -> Path:
    dataframes_folder: Path = get_target_path().joinpath('dataframes')
    dataframes_folder.mkdir(parents=True, exist_ok=True)
    return dataframes_folder


def get_cleaned_dataframes_path() -> Path:
    cleaned_dataframes_folder: Path = get_dataframes_path().joinpath('cleaned')
    cleaned_dataframes_folder.mkdir(parents=True, exist_ok=True)
    return cleaned_dataframes_folder


def get_models_path() -> Path:
    models_path: Path = Path("../models").resolve()
    models_path.mkdir(parents=True, exist_ok=True)
    return models_path


def get_topic_modeling_path():
    topic_modeling_folder: Path = get_models_path().joinpath('topic_modeling')
    topic_modeling_folder.mkdir(parents=True, exist_ok=True)
    return topic_modeling_folder


def get_classification_models_path():
    classification_models_folder: Path = get_models_path().joinpath('classification')
    classification_models_folder.mkdir(parents=True, exist_ok=True)
    return classification_models_folder

def get_sbert_models_path():
    sbert_models_folder: Path = get_classification_models_path().joinpath('SentenceTransformer')
    sbert_models_folder.mkdir(parents=True, exist_ok=True)
    return sbert_models_folder


def get_word2vec_models_path():
    word2vec_models_folder: Path = get_classification_models_path().joinpath('Word2Vec')
    word2vec_models_folder.mkdir(parents=True, exist_ok=True)
    return word2vec_models_folder

def get_fasttext_models_path():
    fasttext_models_folder: Path = get_classification_models_path().joinpath('FastText')
    fasttext_models_folder.mkdir(parents=True, exist_ok=True)
    return fasttext_models_folder

def get_fasttext_aligned_models_path():
    fasttext_aligned_models_folder: Path = get_fasttext_models_path().joinpath('aligned_embeddings')
    fasttext_aligned_models_folder.mkdir(parents=True, exist_ok=True)
    return fasttext_aligned_models_folder


def get_fasttext_pretrained_aligned_models_path():
    fasttext_aligned_pretrained_models_folder: Path = get_fasttext_aligned_models_path().joinpath('pretrained')
    fasttext_aligned_pretrained_models_folder.mkdir(parents=True, exist_ok=True)
    return fasttext_aligned_pretrained_models_folder

def get_datasets_path() -> Path:
    datasets_folder: Path = Path("../notebooks/datasets").resolve()
    datasets_folder.mkdir(parents=True, exist_ok=True)
    return datasets_folder

def get_datasets_embedding_classification_path() -> Path:
    dataset_enbedding_classification_folder: Path = Path("../notebooks/datasets_embedding_classification").resolve()
    dataset_enbedding_classification_folder.mkdir(parents=True, exist_ok=True)
    return dataset_enbedding_classification_folder
