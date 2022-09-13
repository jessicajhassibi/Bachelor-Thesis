import re

import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

from data import data_helpers

nltk.download('stopwords')


# TODO: make it work for all langs
# TODO: numbers/years  as stop words?
def clean_texts(text, lang="english"):
    """
    Cleans data by applying tokenization, removal of stop words
    """
    tokens = []
    punctuation_marks = [",", ".", ";", ":", "-", "–", '"', "/", '""', "''" "'", "(", ")", "[", "]", "!", "?", "=", "{",
                         "}", "&", '*', '†']
    for sent in sent_tokenize(text, lang):
        for token in word_tokenize(sent, lang):
            token = token.lower()
            if not is_stop_word(token, lang) and token not in punctuation_marks:
                # additionally lemmatize?!
                tokens.append(token)
    return tokens


def is_stop_word(word, lang):
    sw = stopwords.words(lang)
    sw.append("isbn")
    if word in sw:
        return True
    elif re.match(r"\d+", word):  # e.g. "1" or "20" but not a year (1994) as it may contain historical information:
        return True  # TODO: but years gone?!
    else:
        return False


def get_stop_words() -> list:
    """
    merges stopwords for each language
    """
    stop_words = list()
    for lang in data_helpers.get_languages():
        lang = data_helpers.get_full_language_word(lang)
        stop_words = stop_words + stopwords.words(lang)
    return stop_words


def create_dataframes():
    for lang in data_helpers.get_languages():
        group_0, group_1 = data_helpers.get_groups()
        df_group_0 = data_helpers.get_dataframe_from_json(
            str(data_helpers.get_json_target_path(group_0.wiki_page, group_0.label, lang)))
        df_group_1 = data_helpers.get_dataframe_from_json(
            str(data_helpers.get_json_target_path(group_1.wiki_page, group_1.label, lang)))

        # create train dataframe using texts and labels
        combined_df = pd.DataFrame()
        combined_df["text"] = pd.concat([df_group_0["text"], df_group_1["text"]], ignore_index=True)
        combined_df["label"] = pd.concat([df_group_0["label"], df_group_1["label"]], ignore_index=True)
        combined_df.to_csv(data_helpers.get_dataframes_path().joinpath(f'{lang}_df.csv'))


# TODO: geburtsdaten cleanen
# create new dataframes with cleaned text
def create_cleaned_dataframes():
    for lang in data_helpers.get_languages():
        df_cleaned = pd.read_csv(data_helpers.get_dataframes_path().joinpath(f"{lang}_df.csv"))
        df_cleaned.insert(1, "cleaned_text", df_cleaned["text"].apply(lambda x: clean_texts(x, "english")))
        df_cleaned.drop(labels="text", axis="columns", inplace=True)
        df_cleaned.drop(labels="Unnamed: 0", axis="columns", inplace=True)
        # Encoding the label column
        df_cleaned['label'] = df_cleaned['label'].map({'supported': 1, 'persecuted': 0})
        # save cleaned dataframe
        df_cleaned.to_csv(data_helpers.get_cleaned_dataframes_path().joinpath(f'{lang}_df_cleaned.csv'))
