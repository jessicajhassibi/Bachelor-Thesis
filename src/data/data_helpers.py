import os
from pathlib import Path

import pandas as pd
import nlp


def get_data_target_path() -> Path:
    target_folder: Path = Path("../target/data").resolve()
    target_folder.mkdir(parents=True, exist_ok=True)
    return target_folder


def get_supported_composers_path() -> Path:
    supported_composers_folder: Path = get_data_target_path().joinpath("supported_composers")
    supported_composers_folder.mkdir(exist_ok=True)
    return supported_composers_folder


def get_persecuted_composers_path() -> Path:
    persecuted_composers_folder: Path = get_data_target_path().joinpath("persecuted_composers")
    persecuted_composers_folder.mkdir(exist_ok=True)
    return persecuted_composers_folder


def get_dataframes_path() -> Path:
    dataframes_folder: Path = get_data_target_path().joinpath('dataframes')
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


def create_dataframes(langs: list):
    get_data_target_path().joinpath('dataframes').mkdir(exist_ok=True)
    for lang in langs:
        df_supported = get_dataframe_from_json(
            str(get_supported_composers_path().joinpath(f"{lang}_texts_composers_supported.json")))
        df_persecuted = get_dataframe_from_json(str(get_persecuted_composers_path().joinpath(
            f"{lang}_texts_composers_persecuted.json")))
        # create train dataframe using texts and labels
        combined_df = pd.DataFrame()
        combined_df["text"] = pd.concat([df_supported["text"], df_persecuted["text"]], ignore_index=True)
        combined_df["label"] = pd.concat([df_supported["label"], df_persecuted["label"]], ignore_index=True)
        combined_df.to_csv(get_dataframes_path().joinpath(f'{lang}_df.csv'))


# TODO: geburtsdaten cleanen
# create new dataframes with cleaned text
def create_cleaned_dataframes(langs: list):
    for lang in langs:
        df_cleaned = pd.read_csv(get_dataframes_path().joinpath(f"{lang}_df.csv"))
        df_cleaned.insert(1, "cleaned_text", df_cleaned["text"].apply(lambda x: nlp.clean_texts(x, "english")))
        df_cleaned.drop(labels="text", axis="columns", inplace=True)
        df_cleaned.drop(labels="Unnamed: 0", axis="columns", inplace=True)
        # Encoding the label column
        df_cleaned['label'] = df_cleaned['label'].map({'supported': 1, 'persecuted': 0})
        # save cleaned dataframe
        df_cleaned.to_csv(get_cleaned_dataframes_path().joinpath(f'{lang}_df_cleaned.csv'))
