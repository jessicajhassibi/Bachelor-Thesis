import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from typing import Tuple

from .path_helpers import get_json_target_path, get_target_path
from .data_helpers import get_groups, get_dataframe_from_json, get_sentences
from .models import Group

ARTICLES_STR = "articles"
PARAGRAPHS_STR = "paragraphs"
SENTENCES_STR = "sentences"
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
            json_path = get_json_target_path(group.wiki_page, group.label, lang)
            df = get_dataframe_from_json(str(json_path))
            article_count, paragraph_count, sentences_count, words_count = counter(df, lang)
            count_dict[group.label][lang] = {ARTICLES_STR: article_count,
                                             PARAGRAPHS_STR: paragraph_count,
                                             SENTENCES_STR: sentences_count,
                                             WORDS_STR: words_count}
    return group_0_count_dict, group_1_count_dict


def counter(df: pd.DataFrame, language) -> Tuple[int,int,int]:
    """
    Counts how many articles, paragraphs and words in texts of texts_array exist.
    """
    a, p, s, w = 0, 0, 0, 0
    a = df["text"].count()
    for paragraphs_wiki_page in df["paragraphs"].values:
        for paragraph in paragraphs_wiki_page:
            p += 1
            w += len(paragraph.split())
    for sentences_wiki_page in get_sentences(df["text"].values.tolist(), language):
        s += len(sentences_wiki_page)
    return a, p, s, w


def plot_pie_chart(group: Group, group_count_dict: dict, element: str, ax):
    # Plotting articles pie chart
    #add colors
    colors = ['#66b3ff','#99ff99','#ffcc99']
    sizes = [group_count_dict[group.label][lang][element] for lang in group.wiki_languages]
    ax.pie(sizes, labels=group.wiki_languages, autopct=lambda pct: pct_func(pct, sizes), colors=colors)
    ax.set_title(f"{group.label} - Distribution of {element}")


def plot_scraped_data():
    group_0, group_1 = get_groups()
    group_0_count_dict, group_1_count_dict = language_analyzer(group_0, group_1)
    # 3 Pie charts to be side by side
    for group, count_dict in [(group_0, group_0_count_dict), (group_1, group_1_count_dict)]:
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(20, 20))
        for elem, ax in [(ARTICLES_STR, ax1), (PARAGRAPHS_STR, ax2), (SENTENCES_STR, ax3), (WORDS_STR, ax4)]:
            plot_pie_chart(group, count_dict, elem, ax)
            # get current figure
        fig_out = plt.gcf()

        # show plot
        plt.show()

        # save plot
        target = get_target_path().joinpath("reports/figures").resolve()
        target.mkdir(parents=True, exist_ok=True)
        fig_out.savefig(target.joinpath(f"Sprachverteilungen_{group.label}.png"))


def pct_func(pct, allvalues):
    """Creating autocpt arguments."""
    absolute = int(pct / 100. * np.sum(allvalues))
    return "{:.1f}%\n({:d})".format(pct, absolute)


