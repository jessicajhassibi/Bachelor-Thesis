import nltk
import pandas as pd
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
nltk.download('stopwords')
import re
import data_helpers

# TODO: make it work for all langs
# TODO: numbers/years  as stop words?
def clean_texts(text, lang="english"):
    """
    Cleans data by applying tokenization, removal of stop words
    """
    tokens = []
    punctuation_marks = [",", ".", ";", ":", "-", "–", '"', "/",'""', "''" "'", "(", ")", "[", "]", "!", "?", "=", "{",
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
    elif re.match(r"\d+", word): # e.g. "1" or "20" but not a year (1994) as it may contain historical information:
        return True # TODO: but years gone?!
    else:
        return False


def get_stop_words(langs: list) -> list:
    """
    merges stopwords for each language
    """
    stop_words = list()
    for lang in langs:
        lang = data_helpers.get_full_language_word(lang)
        stop_words = stop_words + stopwords.words(lang)
    return stop_words