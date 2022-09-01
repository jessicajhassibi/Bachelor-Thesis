import WikiScraper
import pandas as pd

def get_dataframe_from_path(file: str):
    df = pd.read_json(file)
    #transpose index and columns of df
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


def language_analyzer(langs, dataframe):
    """
    Creates nested dict of languages and their counts of articles, paragraphs, words and categories.
    :param langs:
    :param dataframe:
    :return:
    """
    # create dictionary
    count_dict = dict()

    #count_dict = dict.fromkeys(langs, language_dict)

    langs_texts = []
    # get counts
    for lang in langs:
        col_name = f"{lang}_paragraphs"
        texts = dataframe[col_name]
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

