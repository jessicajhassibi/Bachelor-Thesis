# %%
import matplotlib.pyplot as plt
import numpy as np

from .data_helpers import get_groups, get_dataframe_from_json, get_json_target_path


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
    group_0_count_dict: dict = dict()
    group_1_count_dict: dict = dict()

    article_count, paragraph_count, words_count = 0, 0, 0
    group_0, group_1 = get_groups()

    # ---------- group 0 -----------
    for lang in group_0.wiki_languages:
        json_path = get_json_target_path(group_0.wiki_page, group_0.label, lang)
        df_0 = get_dataframe_from_json(str(json_path))
        counts = text_counter(df_0['text'])
        article_count += counts[0]
        paragraph_count += counts[1]
        words_count += counts[2]
        group_0_count_dict[group_0.label][lang] = {"articles": article_count,
                                                   "paragraphs": paragraph_count,
                                                   "words": words_count}

    # ---------- group 1 -----------
    article_count, paragraph_count, words_count = 0, 0, 0
    for lang in group_1.wiki_languages:
        json_path = get_json_target_path(group_1.wiki_page, group_1.label, lang)
        df_1 = get_dataframe_from_json(str(json_path))
        counts = text_counter(df_1['text'])
        article_count += counts[0]
        paragraph_count += counts[1]
        words_count += counts[2]
        group_1_count_dict[group_1.label][lang] = {"articles": article_count,
                                                   "paragraphs": paragraph_count,
                                                   "words": words_count}

    print("group_0_count_dict=", group_0_count_dict)
    print("group_1_count_dict=", group_1_count_dict)
    return group_0_count_dict, group_1_count_dict


def jupyter():
    # 3 Pie charts to be side by side
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 20))

    # Plotting articles pie chart
    sizes = [languages_count_dict[lang]["articles"] for lang in languages_count_dict.keys()]
    ax1.pie(sizes, labels=data_analysis.get_languages(), autopct=lambda pct: pct_func(pct, sizes))
    ax1.set_title("Verteilung der Artikel")

    # Plotting paragraphs pie chart
    sizes = [languages_count_dict[lang]["paragraphs"] for lang in languages_count_dict.keys()]
    ax2.pie(sizes, labels=languages, autopct=lambda pct: pct_func(pct, sizes))
    ax2.set_title("Verteilung der Paragraphen")

    # Plotting words pie chart
    sizes = [languages_count_dict[lang]["words"] for lang in languages_count_dict.keys()]
    ax3.pie(sizes, labels=languages, autopct=lambda pct: pct_func(pct, sizes))
    ax3.set_title("Verteilung der Wörter")

    # get current figure
    fig_out = plt.gcf()

    # show plot
    plt.show()

    # save plot
    fig_out.savefig("../reports/figures/Sprachverteilungen.pdf")


def pct_func(pct, allvalues):
    """Creating autocpt arguments."""
    absolute = int(pct / 100. * np.sum(allvalues))
    return "{:.1f}%\n({:d})".format(pct, absolute)


def get_total_counts(count_dict):
    a = 0
    p = 0
    w = 0
    for lang in count_dict.keys():
        a += count_dict[lang]["articles"]
        p += count_dict[lang]["paragraphs"]
        w += count_dict[lang]["words"]
    return a, p, w
