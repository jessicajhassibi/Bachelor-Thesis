import pandas as pd
from ast import literal_eval
from .nlp import clean_texts, clean_paragraphs, get_sentences
from .path_helpers import get_cleaned_dataframes_path, get_dataframes_path, get_json_target_path
from .config_helpers import get_groups, get_languages
import csv


def get_dataframe_from_json(file: str):
    df = pd.read_json(file)
    # transpose index and columns of df
    df = df.transpose()
    return df


def get_documents_list(text_type='paragraphs'):
    """
    Get list of documents.
    Can be either 'texts', 'paragraphs' or 'sentences'
    or their cleaned versions 'cleaned_texts' etc. (Note: no cleaned_sentences option)
    """
    documents = list()
    if text_type == 'cleaned_paragraphs':
        paragraphs_list = get_cleaned_dataframe_with_topics()[text_type].values.tolist()
        for paragraphs in paragraphs_list:
            for paragraph in paragraphs:
                documents.append(paragraph)
    elif text_type == 'cleaned_texts':  # full (raw/ cleaned) text of article chosen as text type
        documents.extend(get_cleaned_dataframe_with_topics()['cleaned_texts'].values.tolist())
    elif text_type == 'paragraphs':
        paragraphs_list = get_dataframes()['paragraphs'].values.tolist()
        for paragraphs in paragraphs_list:
            for paragraph in paragraphs:
                documents.append(paragraph)
    else:
        texts_list = get_dataframes()['texts'].values.tolist()
        if text_type == 'sentences':
            sentences_list = get_dataframes()['sentences'].values.tolist()
            for sentence in sentences_list:
                documents.extend(sentence)
        else:
            documents.extend(texts_list)
    print("Document_list:", documents)
    return documents


def get_cleaned_dataframes():
    lang_dfs_list = []
    for lang in get_languages():
        # apply conversion to cleaned_text to avoid multiple quotation marks due to wrong pandas csv reading
        lang_df = pd.read_csv(get_cleaned_dataframes_path().joinpath(f"{lang}_df_cleaned.csv").resolve(),
                              converters={'cleaned_texts': lambda x: x.strip("[]").split(", "),
                                          'cleaned_paragraphs': lambda x:  x[1:-1].split(", ")})
        lang_dfs_list.append(lang_df)
    df = pd.concat(lang_dfs_list)
    df.drop(labels="Unnamed: 0", axis="columns", inplace=True)
    return df


def get_dataframes():
    lang_dfs_list = []
    for lang in get_languages():
        lang_df = pd.read_csv(get_dataframes_path().joinpath(f"{lang}_df.csv").resolve(),
                              converters={'paragraphs': lambda x: literal_eval(x),
                                          'sentences': lambda x: literal_eval(x)})
        lang_dfs_list.append(lang_df)
    df = pd.concat(lang_dfs_list)
    df.drop(labels="Unnamed: 0", axis="columns", inplace=True)
    return df


def create_dataframes():
    for lang in get_languages():
        group_0, group_1 = get_groups()
        df_group_0 = get_dataframe_from_json(
            str(get_json_target_path(group_0.wiki_page, group_0.label, lang)))
        df_group_1 = get_dataframe_from_json(
            str(get_json_target_path(group_1.wiki_page, group_1.label, lang)))

        # get sentences
        sentences_group_0: list = get_sentences(df_group_0["text"].values.tolist(), lang)
        sentences_group_1: list = get_sentences(df_group_1["text"].values.tolist(), lang)
        # convert lists to dataframes
        sentences_df_group_0 = pd.Series((s for s in sentences_group_0))
        sentences_df_group_1 = pd.Series((s for s in sentences_group_1))

        # create dataframe with both groups
        df = pd.DataFrame()
        df["texts"] = pd.concat([df_group_0["text"], df_group_1["text"]], ignore_index=True)
        df["texts"] = df["texts"].apply(lambda x: x.replace("\n", " "))
        df["paragraphs"] = pd.concat([df_group_0["paragraphs"], df_group_1["paragraphs"]], ignore_index=True)
        df["paragraphs"] = df["paragraphs"].apply(lambda x: [p.replace("\n", " ") for p in x])
        df["sentences"] = pd.concat([sentences_df_group_0, sentences_df_group_1], ignore_index=True)
        df["label"] = pd.concat([df_group_0["label"], df_group_1["label"]], ignore_index=True)
        # Encoding the label column
        df['label'] = df['label'].map({group_1.label: 1, group_0.label: 0})
        df.to_csv(get_dataframes_path().joinpath(f'{lang}_df.csv'))

        # create the same dataframe with cleaned texts
        cleaned_df = pd.DataFrame()
        cleaned_df["cleaned_texts"] = df["texts"].apply(lambda x: clean_texts(x, lang))
        cleaned_df["cleaned_paragraphs"] = df["paragraphs"].apply(lambda x: clean_paragraphs(x, lang))
        cleaned_df["label"] = df["label"]
        df.reset_index()
        cleaned_df.to_csv(get_cleaned_dataframes_path().joinpath(f'{lang}_df_cleaned.csv'))
# %%


def get_topic_of_every_doc(bertopic_model, docs, number_topics):
    # TODO: mark author TTLAB
    """
    Author: Derived from https://github.com/mevbagci/Topic-Modelling/
    Returns list of topics for documents in docs.
    For each document it stores the topics in a dictionary of topics.
    Those Topics consist of 10 words defining that topic."""
    topic_list = []
    topics_names = bertopic_model.get_topics()
    if number_topics > len(topics_names):
        number_topics = len(topics_names)
    topics_names_dict = {}
    for i in topics_names:
        topics_names_dict[i] = dict((x, y) for x, y in topics_names[i])
    for doc_i in docs:
        topic_rep = bertopic_model.find_topics(doc_i, number_topics)
        documents_per_document = {}
        for c, topic_i in enumerate(topic_rep[0]):
            documents_per_document[f"Topic {topic_i}"] = {
                "Probability": topic_rep[1][c],
                "topic": topics_names_dict[topic_i]
            }
        topic_list.append(documents_per_document)
    return topic_list


def get_topics_for_articles(bertopic_model, num_topics):
    """
    Finds fixed number of most probable topics of articles.
    Creates a list for the num_topics * 10 topic words (10 words describe one topic) for each article.
    Returns list of lists.
    """
    topics_for_each_article = []
    documents = get_dataframes()["sentences"]
    topic_list = get_topic_of_every_doc(bertopic_model, documents, num_topics)
    for article_topics in topic_list:
        article_topics_words = []
        for topic_dict in article_topics:
            topic_words = article_topics[topic_dict].get("topic").keys()
            # append topic words for article to list for all articles
            article_topics_words.extend(list(topic_words))
        topics_for_each_article.append(article_topics_words)
    return topics_for_each_article


# TODO: save correctly to df
def get_cleaned_dataframe_with_topics(bertopic_model, num_topics=3): # TODO: set num_topics to average text size
    topic_df = get_cleaned_dataframes()
    topics_list = get_topics_for_articles(bertopic_model, num_topics)
    topics_series = pd.Series((t for t in topics_list))
    topic_df["topics"] = topics_series  # TODO: add paragraph_topics column with paragraph num of row for the topics
    topic_df.to_csv(get_cleaned_dataframes_path().joinpath(f'topics_df.csv'))
    return topic_df #TODO: paragraphs messed up and strings
