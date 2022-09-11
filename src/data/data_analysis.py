import data_helpers
from data.data_helpers import get_groups, get_languages


def text_counter(texts_array):
    """
    Counts how many articles, paragraphs and words in texts of texts_array exist.
    """
    a = 0
    p = 0
    w = 0
    for text in texts_array.values:
        if text != "" and text != []:
            a += 1
            for paragraph in text:
                p += 1

                # count words in paragraph
                word_list = paragraph.split()
                w += len(word_list)
    return a, p, w


def language_analyzer():
    """
    Creates nested dict of languages and their counts of articles, paragraphs, words and categories.
    """
    # create dictionary
    count_dict = dict()

    group_0, group_1 = get_groups()

    # get counts
    for lang in get_languages():
        dfs = [data_helpers.get_dataframe_from_json(
            str(get_persecuted_composers_path().joinpath(f"{lang}_texts_composers_persecuted.json"))),
            data_helpers.get_dataframe_from_json(
                str(get_supported_composers_path().joinpath(f"{lang}_texts_composers_supported.json")))]

        a, p, w = 0, 0, 0
        for df in dfs:
            texts = df["paragraphs"]
            counts = text_counter(texts)
            a += counts[0]
            p += counts[1]
            w += counts[2]
        count_dict[lang] = {"articles": a,
                            "paragraphs": p,
                            "words": w}

    print("count_dict=", count_dict)
    return count_dict


def get_total_counts(count_dict):
    a = 0
    p = 0
    w = 0
    for lang in count_dict.keys():
        a += count_dict[lang]["articles"]
        p += count_dict[lang]["paragraphs"]
        w += count_dict[lang]["words"]
    return a, p, w
