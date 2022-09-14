import matplotlib.pyplot as plt
import numpy as np

from .path_helpers import get_json_target_path, get_target_path
from .data_helpers import get_groups, get_dataframe_from_json
from .models import Group


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


ARTICLES_STR = "articles"
PARAGRAPHS_STR = "paragraphs"
WORDS_STR = "words"


def language_analyzer(group_0: Group, group_1: Group):
    """
    Creates nested dict of languages and their counts of articles, paragraphs, words and categories.
    """
    # create dictionary
    group_0_count_dict: dict = dict()
    group_1_count_dict: dict = dict()

    for group, count_dict in [(group_0, group_0_count_dict), (group_1, group_1_count_dict)]:
        count_dict[group.label] = dict()
        for lang in group.wiki_languages:
            article_count, paragraph_count, words_count = 0, 0, 0
            json_path = get_json_target_path(group.wiki_page, group.label, lang)
            df = get_dataframe_from_json(str(json_path))
            counts = text_counter(df['text'])
            article_count += counts[0]
            paragraph_count += counts[1]
            words_count += counts[2]
            count_dict[group.label][lang] = {ARTICLES_STR: article_count,
                                             PARAGRAPHS_STR: paragraph_count,
                                             WORDS_STR: words_count}

    print("group_0_count_dict=", count_dict)
    print("group_1_count_dict=", group_1_count_dict)
    return group_0_count_dict, group_1_count_dict


def plot_pie_chart(group: Group, group_count_dict: dict, element: str, ax):
    # Plotting articles pie chart
    sizes = [group_count_dict[group.label][lang][element] for lang in group.wiki_languages]
    ax.pie(sizes, labels=group.wiki_languages, autopct=lambda pct: pct_func(pct, sizes))
    ax.set_title(f"{group.label} - Distribution of {element}")


def plot_scraped_data():
    group_0, group_1 = get_groups()
    group_0_count_dict, group_1_count_dict = language_analyzer(group_0, group_1)
    # 3 Pie charts to be side by side
    for group, count_dict in [(group_0, group_0_count_dict), (group_1, group_1_count_dict)]:
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 20))
        for elem, ax in [(ARTICLES_STR, ax1), (PARAGRAPHS_STR, ax2), (WORDS_STR, ax3)]:
            plot_pie_chart(group, count_dict, elem, ax)
            # get current figure
        fig_out = plt.gcf()

        # show plot
        plt.show()

    # save plot
    target = get_target_path().joinpath("reports/figures").resolve()
    target.mkdir(parents=True, exist_ok=True)
    fig_out.savefig(target.joinpath("Sprachverteilungen.pdf"))


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
