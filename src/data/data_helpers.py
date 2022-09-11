from configparser import ConfigParser
from pathlib import Path

import pandas as pd

from data import Group


def get_groups_ini_path() -> Path:
    return Path('../groups.ini').resolve()


def get_groups() -> (Group, Group):
    # read data from groups.ini file
    groups = ConfigParser()
    groups.read(filenames=get_groups_ini_path(), encoding="ISO-8859-1")

    # set up the two groups
    group_0: Group = Group(label=groups["GROUP_0"]["LABEL"],
                           wiki_page=groups["GROUP_0"]["WIKI_PAGE_WITH_LIST"],
                           wiki_categories=groups["GROUP_0"]["WIKI_TARGET_CATEGORIES"].split(","),
                           wiki_alternative_categories=groups["GROUP_0"]["WIKI_ALTERNATIVE_TARGET_CATEGORIES"].split(
                               ","),
                           wiki_main_language=groups["GROUP_0"]["WIKI_MAIN_LANGUAGE"],
                           wiki_languages=groups["GROUP_0"]["WIKI_LANGUAGES"].split(","))

    group_1: Group = Group(label=groups["GROUP_1"]["LABEL"],
                           wiki_page=groups["GROUP_1"]["WIKI_PAGE_WITH_LIST"],
                           wiki_categories=groups["GROUP_1"]["WIKI_TARGET_CATEGORIES"].split(","),
                           wiki_alternative_categories=groups["GROUP_1"]["WIKI_ALTERNATIVE_TARGET_CATEGORIES"].split(
                               ","),
                           wiki_main_language=groups["GROUP_1"]["WIKI_MAIN_LANGUAGE"],
                           wiki_languages=groups["GROUP_1"]["WIKI_LANGUAGES"].split(","))

    return group_0, group_1


def get_languages():
    group_0, group_1 = get_groups()
    # TODO why group:0 and not 1
    return group_0.wiki_languages


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


def get_full_language_word(lang):
    langs_dict = {"en": "english", "de": "german", "es": "spanish", "ar": "arabic", "fr": "french", "it": "italian"}
    return langs_dict[lang]


def get_dataframe_from_json(file: str):
    df = pd.read_json(file)
    # transpose index and columns of df
    df = df.transpose()
    return df


def get_documents_list(languages):
    documents = list()
    for lang in languages:
        lang_df = pd.read_csv(get_dataframes_path().joinpath(f"{lang}_df.csv").resolve())
        text_list = lang_df["text"].values.tolist()
        documents = documents + text_list
    return documents
