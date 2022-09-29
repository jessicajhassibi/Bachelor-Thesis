import pandas as pd
from .path_helpers import get_dataframes_path, get_cleaned_dataframes_path
from ast import literal_eval
from .nlp import get_sentences, get_cleaned_sentences, clean_texts, clean_paragraphs
from .path_helpers import get_cleaned_dataframes_path, get_dataframes_path, get_json_target_path
from .config_helpers import get_groups, get_languages


def get_dataframe_from_json(file: str):
    df = pd.read_json(file)
    # transpose index and columns of df
    df = df.transpose()
    return df


def get_documents_list(text_type = 'paragraphs'):
    # TODO: Add sentences to csv like paragraphs
    """
    Get list of documents.
    Can be either 'texts', 'paragraphs' or 'sentences'
    """
    if text_type == 'paragraphs':
        paragraphs_list = get_dataframes()['paragraphs'].values.tolist()
        documents = [paragraph for paragraphs in paragraphs_list for paragraph in paragraphs]
    elif text_type == 'cleaned_paragraphs':
        paragraphs_list = get_cleaned_dataframes()['cleaned_paragraphs'].values.tolist()
        documents = list()
        for paragraphs in paragraphs_list:
            for paragraph in paragraphs:
                for words in paragraph:
                    documents.append(words)
    elif text_type == 'sentences':
        documents = get_dataframes()['sentences'].values.tolist()
    elif text_type == 'cleaned_sentences':
        documents = get_cleaned_dataframes()['cleaned_texts'].values.tolist()
    elif text_type == 'cleaned_text':  # full (raw/ cleaned) text of article chosen as text type
        documents = get_cleaned_dataframes()['cleaned_texts'].values.tolist()
    else:
        documents = get_dataframes()['texts'].values.tolist()
    return documents


def get_cleaned_dataframes():
    lang_dfs_list = []
    for lang in get_languages():
        # apply conversion to cleaned_text to avoid multiple quotation marks due to wrong pandas csv reading
        lang_df = pd.read_csv(get_cleaned_dataframes_path().joinpath(f"{lang}_df_cleaned.csv").resolve(),
                              converters={'cleaned_texts': lambda x: literal_eval(x),
                                          'cleaned_paragraphs': lambda x: literal_eval(x),
                                          'cleaned_sentences': lambda x: literal_eval(x)})
        lang_dfs_list.append(lang_df)
    df = pd.concat(lang_dfs_list)
    df.drop(labels="Unnamed: 0", axis="columns", inplace=True)
    return df


def get_dataframes():
    lang_dfs_list = []
    for lang in get_languages():
        lang_df = pd.read_csv(get_dataframes_path().joinpath(f"{lang}_df.csv").resolve(),
                              converters={'texts': lambda x: literal_eval(x),
                                          'paragraphs': lambda x: literal_eval(x),
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


        # create dataframe with both groups
        df = pd.DataFrame()
        df["paragraphs"] = pd.concat([df_group_0["paragraphs"], df_group_1["paragraphs"]], ignore_index=True)
        df["texts"] = pd.concat([df_group_0["text"], df_group_1["text"]], ignore_index=True)
        sentences = get_sentences(df_group_0["text"]).append(get_sentences(df_group_1["text"].values.tolist()))
        df["label"] = pd.concat([df_group_0["label"], df_group_1["label"]], ignore_index=True)
        # Encoding the label column
        df['label'] = df['label'].map({group_1.label: 1, group_0.label: 0})

        # split texts to sentences and save in df
        df.reset_index()
        for index, row in df.iterrows():
            text = row["texts"]
            sentences = get_sentences(text, lang)
            df["sentences"][index] = sentences
        df.to_csv(get_dataframes_path().joinpath(f'{lang}_df.csv'))

        # create the same dataframe with cleaned texts
        cleaned_df = pd.DataFrame()
        cleaned_df["cleaned_paragraphs"] = df["paragraphs"].apply(lambda x: clean_paragraphs(x, lang))
        cleaned_df["cleaned_texts"] = df["texts"].apply(lambda x: clean_texts(x, lang))
        cleaned_df["cleaned_sentences"] = df["sentences"].apply(lambda x: clean_texts(x, lang))
        cleaned_df["label"] = df["label"]
        df.reset_index()
        for index, row in df.iterrows():
            text = row["cleaned_texts"]
            sentences = get_sentences(text, lang)
            df["sentences"][index] = sentences
        cleaned_df.to_csv(get_cleaned_dataframes_path().joinpath(f'{lang}_df_cleaned.csv'))