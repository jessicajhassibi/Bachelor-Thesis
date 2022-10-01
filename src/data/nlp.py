import re
from .config_helpers import get_spacy_language_models
from .nlp_helpers import get_stop_words

spacy_models: dict = get_spacy_language_models()


def clean_texts(text, lang="en") -> list():
    """
    Cleans data by applying tokenization, removal of stop words
    """
    nlp = spacy_models[lang]
    text = re.sub("(\[.*\])", "", text)  # remove phonetic spelling like [ˈbeːlɒ:ˈbɒrtoːk']
    words = list()
    doc = nlp(text)
    punctuation_marks = [",", ".", ";", ":", "(;", "-", "–", '"', '„',  '“', "/", '""', "''" "'", "(", ")", "[", "]",
                         "!", "?", "=", "{", "}", "&", '*', '†']
    for sent in list(doc.sents):
        for token in sent:
            lemmatized_word = token.lemma_
            if is_stop_word(lemmatized_word, lang):
                continue
            elif token.text in punctuation_marks:
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
    else:
        return False

