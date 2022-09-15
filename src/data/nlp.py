import re

import pandas as pd
import spacy
from nltk.corpus import stopwords
from .data_helpers import get_full_language_word, get_languages, get_groups, get_dataframe_from_json
from .path_helpers import get_cleaned_dataframes_path, get_dataframes_path, get_json_target_path

# python -m spacy download 'xx_ent_wiki_sm'
# instantiating multiple languages pipeline package
# TODO: try with large model
nlp = spacy.load('xx_ent_wiki_sm')
print("SpaCy pipeline loaded")
# Adding the 'sentencizer component to the pipeline
nlp.add_pipe('sentencizer')
import re


# TODO: make it work for all langs -> switch to spacy -> trained on 73 other languages
# TODO: numbers/years  as stop words?
def clean_texts(text, lang="en"):
    """
    Cleans data by applying tokenization, removal of stop words
    """
    text = re.sub("(\[.*\])", "", text) # remove phonetic spelling like [ˈbeːlɒ:ˈbɒrtoːk']
    tokens = list()
    doc = nlp(text)
    punctuation_marks = [",", ".", ";", ":", "-", "–", '"', "/", '""', "''" "'", "(", ")", "[", "]", "!", "?", "=", "{",
                         "}", "&", '*', '†']
    for sent in list(doc.sents):
        for token in sent:
            #print(token, token.lemma_)
            token = str(token)
            if is_stop_word(token, lang):
                continue
            elif token in punctuation_marks:
                continue
            else:
                tokens.append(token)
    return tokens


def is_stop_word(word, lang):
    sw = stopwords.words(get_full_language_word(lang))
    sw.append("isbn")
    if word in sw:
        return True
    #elif re.match(r"\d+", word):  # e.g. "1" or "20" but not a year (1994) as it may contain historical information:
    #    return True  # TODO: but years gone?!
    else:
        return False


def get_stop_words() -> list:
    """
    merges stopwords for each language
    """
    stop_words = list()
    for lang in get_languages():
        lang = get_full_language_word(lang)
        stop_words = stop_words + stopwords.words(lang)
    return stop_words


def create_dataframes():
    for lang in get_languages():
        group_0, group_1 = get_groups()
        df_group_0 = get_dataframe_from_json(
            str(get_json_target_path(group_0.wiki_page, group_0.label, lang)))
        df_group_1 = get_dataframe_from_json(
            str(get_json_target_path(group_1.wiki_page, group_1.label, lang)))

        # create train dataframe using texts and labels
        combined_df = pd.DataFrame()
        combined_df["text"] = pd.concat([df_group_0["text"], df_group_1["text"]], ignore_index=True)
        combined_df["label"] = pd.concat([df_group_0["label"], df_group_1["label"]], ignore_index=True)
        combined_df.to_csv(get_dataframes_path().joinpath(f'{lang}_df.csv'))


# TODO: geburtsdaten cleanen
def create_cleaned_dataframes():
    for lang in get_languages():
        group_0, group_1 = get_groups()
        df_cleaned = pd.read_csv(get_dataframes_path().joinpath(f"{lang}_df.csv"))
        print(f"Cleaning texts in language {lang}")
        cleaned_text = df_cleaned["text"].apply(lambda x: clean_texts(x, lang))
        df_cleaned.insert(1, "cleaned_text", cleaned_text)
        df_cleaned.drop(labels="text", axis="columns", inplace=True)
        df_cleaned.drop(labels="Unnamed: 0", axis="columns", inplace=True)
        # Encoding the label column
        df_cleaned['label'] = df_cleaned['label'].map({group_1.label: 1, group_0.label: 0})
        # save cleaned dataframe
        df_cleaned.to_csv(get_cleaned_dataframes_path().joinpath(f'{lang}_df_cleaned.csv'))
