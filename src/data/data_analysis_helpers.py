import WikiScraper
import pandas as pd

def get_composers_dataframe(path):
    # create dictionary with composers as keys and \
    # for each key a dictionary with the texts of the wikipedia articles \
    # in the languages german, arabic, english, italian, french and spanish
    if path == "":
        data_dict = WikiScraper.extract_persecuted_composers_texts(path)
    elif path == "":
        data_dict = WikiScraper.extract_supported_composers_texts(path)
    df = pd.read_json(path)
    # transpose index and columns of df
    df = df.transpose()
    return df

def text_counter(texts_array):
    """
    Counts how many articles, paragraphs and words in texts of texts_array exist.
    """
    a = 0
    p = 0
    w = 0
    for text in texts_array.values:
        if text != "" and text != []:
            a+=1
            for paragraph in text:
                p+=1

                # count words in paragraph
                word_list = paragraph.split()
                w += len(word_list)
    return(a, p, w)


def language_analyzer(langs, langs_texts):
    """
    Creates nested dict of languages and their counts of articles, paragraphs, words and categories.
    :param langs:
    :param langs_texts:
    :return:
    """
    # create dictionary
    count_dict = dict()

    #count_dict = dict.fromkeys(langs, language_dict)

    # get counts
    for lang in langs:
        index = langs.index(lang)
        texts = langs_texts[index]
        counts = text_counter(texts)
        count_dict[lang] = {"articles": counts[0],
                            "paragraphs": counts[1],
                            "words": counts[2]}
    return count_dict

def get_total_counts(count_dict):
    a = 0
    p = 0
    w = 0
    for lang in count_dict.keys():
        a += count_dict[lang]["articles"]
        p += count_dict[lang]["paragraphs"]
        w += count_dict[lang]["words"]
    return (a, p, w)
