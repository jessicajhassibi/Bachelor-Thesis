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



