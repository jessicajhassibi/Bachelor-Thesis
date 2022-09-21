import os
import spacy
import re
from .config_helpers import get_spacy_language_model
from .nlp_helpers import get_stop_words

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# TODO: try with large model
nlp = spacy.load(get_spacy_language_model())
print("SpaCy pipeline loaded")
# Adding the 'sentencizer component to the pipeline
nlp.add_pipe('sentencizer')


def clean_texts(text, lang="en") -> list():
    """
    Cleans data by applying tokenization, removal of stop words
    """
    text = re.sub("(\[.*\])", "", text)  # remove phonetic spelling like [ˈbeːlɒ:ˈbɒrtoːk']
    words = list()
    doc = nlp(text)
    punctuation_marks = [",", ".", ";", ":", "-", "–", '"', '„',  '“', "/", '""', "''" "'", "(", ")", "[", "]", "!",
                         "?", "=", "{", "}", "&", '*', '†']
    for sent in list(doc.sents):
        for token in sent:
            lemmatized_word = token.lemma_
            if is_stop_word(lemmatized_word, lang):
                continue
            elif lemmatized_word in punctuation_marks:
                continue
            else:
                words.append(lemmatized_word)
    return words


def clean_paragraphs(paragraphs, lang):
    words_list = list()
    for p in paragraphs:
        words = clean_texts(p, lang)
        words_list.append(words)
    return words_list


def is_stop_word(word, lang):
    sw = get_stop_words(lang)
    if word in sw:
        return True
    # elif re.match(r"\d+", word):  # e.g. "1" or "20" but not a year (1994) as it may contain historical information:
    #    return True  # TODO: remove month and day; but years gone?!
    else:
        return False


def get_sentences(texts: list):
    sentences = list()
    for text in texts:
        doc = nlp(text)
        for sent in list(doc.sents):
            sentences.append(sent.text)
    return sentences


def get_cleaned_sentences(texts: list):
    sentences = list()
    for text in texts:
        doc = nlp(text)
        for sent in list(doc.sents):
            cleaned_sent = clean_texts(sent.text)
            sentences.append(cleaned_sent)
    return sentences
