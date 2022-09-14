from configparser import ConfigParser

import pandas as pd
from .models import Group
from .path_helpers import get_groups_ini_path


def get_groups() -> (Group, Group):
    # read data from groups.ini file
    groups = ConfigParser()
    groups.read(filenames= get_groups_ini_path(), encoding="ISO-8859-1")

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


def get_full_language_word(lang):
    langs_dict = {"en": "english", "de": "german", "es": "spanish", "ar": "arabic", "fr": "french", "it": "italian"}
    return langs_dict[lang]


def get_dataframe_from_json(file: str):
    df = pd.read_json(file)
    # transpose index and columns of df
    df = df.transpose()
    return df


def get_documents_list():
    documents = list()
    for lang in get_languages():
        lang_df = pd.read_csv(path_helpers.get_dataframes_path().joinpath(f"{lang}_df.csv").resolve())
        text_list = lang_df["text"].values.tolist()
        documents = documents + text_list
    return documents