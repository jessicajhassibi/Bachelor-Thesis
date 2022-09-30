import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords


def get_full_language_word(lang):
    langs_dict = {"en": "english", "de": "german", "es": "spanish", "ar": "arabic", "fr": "french", "it": "italian"}
    return langs_dict[lang]


def get_stop_words(lang):
    sw: list = stopwords.words(get_full_language_word(lang))
    sw.append("isbn")
    return sw
