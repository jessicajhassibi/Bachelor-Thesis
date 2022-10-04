from configparser import ConfigParser

import spacy
from .models import Group
from .path_helpers import get_config_ini_path

config = ConfigParser()
config.read(filenames= get_config_ini_path(), encoding="ISO-8859-1")


def get_groups() -> (Group, Group):
    # read data from config.ini file

    # set up the two groups
    group_0: Group = Group(label=config["GROUP_0"]["LABEL"],
                           wiki_page=config["GROUP_0"]["WIKI_PAGE_WITH_LIST"],
                           wiki_categories=config["GROUP_0"]["WIKI_TARGET_CATEGORIES"].split(","),
                           wiki_alternative_categories=config["GROUP_0"]["WIKI_ALTERNATIVE_TARGET_CATEGORIES"].split(
                               ","),
                           wiki_main_language=config["GROUP_0"]["WIKI_MAIN_LANGUAGE"],
                           wiki_languages=config["GROUP_0"]["WIKI_LANGUAGES"].split(","))

    group_1: Group = Group(label=config["GROUP_1"]["LABEL"],
                           wiki_page=config["GROUP_1"]["WIKI_PAGE_WITH_LIST"],
                           wiki_categories=config["GROUP_1"]["WIKI_TARGET_CATEGORIES"].split(","),
                           wiki_alternative_categories=config["GROUP_1"]["WIKI_ALTERNATIVE_TARGET_CATEGORIES"].split(
                               ","),
                           wiki_main_language=config["GROUP_1"]["WIKI_MAIN_LANGUAGE"],
                           wiki_languages=config["GROUP_1"]["WIKI_LANGUAGES"].split(","))

    return group_0, group_1


def get_languages():
    group_0, group_1 = get_groups()
    return group_0.wiki_languages


def get_spacy_language_models()-> dict:
    language_models: dict = dict()
    for lang in get_languages():
        if lang == "de":
            model_name = "SPACY_LANGUAGE_MODEL_DE"
        elif lang == "en":
            model_name = "SPACY_LANGUAGE_MODEL_EN"
        else:  # use multilingual model for other languages
            model_name = "SPACY_LANGUAGE_MODEL_XX"
        lang_model = config["SPACY_MODEL"][model_name]
        nlp = spacy.load(lang_model)
        print(f"loaded spacy language model: {lang_model}")
        nlp.add_pipe('sentencizer')
        language_models[lang] = nlp
    # TODO: Load only once
    return language_models


def get_top2vec_embedding_model():
    return config["TOP2VEC_MODEL"]["TOP2VEC_EMBEDDING_MODEL"]