import pandas as pd
from ast import literal_eval
from .nlp import clean_texts, clean_paragraphs
from .path_helpers import get_cleaned_dataframes_path, get_dataframes_path, get_json_target_path
from .config_helpers import get_groups, get_languages


def get_dataframe_from_json(file: str):
    df = pd.read_json(file)
    # transpose index and columns of df
    df = df.transpose()
    return df


def get_documents_list(text_type='paragraphs'):
    """
    Get list of documents.
    Can be either 'texts' or 'paragraphs'
    or their cleaned versions 'cleaned_texts' or 'cleaned_paragraphs'
    """
    if text_type == 'paragraphs' or text_type == 'cleaned_paragraphs':
        paragraphs_list = get_dataframes()[text_type].values.tolist()
        documents = list()
        for paragraphs in paragraphs_list:
            for paragraph in paragraphs:
                documents.append(paragraph)
    elif text_type == 'cleaned_texts':  # full (raw/ cleaned) text of article chosen as text type
        documents = get_cleaned_dataframes()['cleaned_texts'].values.tolist()
    else:
        documents = get_dataframes()['texts'].values.tolist()
    return documents


def get_cleaned_dataframes():
    lang_dfs_list = []
    for lang in get_languages():
        # apply conversion to cleaned_text to avoid multiple quotation marks due to wrong pandas csv reading
        lang_df = pd.read_csv(get_cleaned_dataframes_path().joinpath(f"{lang}_df_cleaned.csv").resolve(),
                              converters={'cleaned_texts': lambda x: x.strip("[]").split(", "),
                                          'cleaned_paragraphs': lambda x: x.strip("[]").split(", ")})
        lang_dfs_list.append(lang_df)
    df = pd.concat(lang_dfs_list)
    df.drop(labels="Unnamed: 0", axis="columns", inplace=True)
    return df


def get_dataframes():
    lang_dfs_list = []
    for lang in get_languages():
        lang_df = pd.read_csv(get_dataframes_path().joinpath(f"{lang}_df.csv").resolve(),
                  converters={'texts': lambda x: x.strip("[]").split(", "),
                              'paragraphs': lambda x: x.strip("[]").split(", ")})
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
        df["paragraphs"] = df["paragraphs"].apply(lambda x: [p.replace("\n", " ") for p in x])
        df["texts"] = pd.concat([df_group_0["text"], df_group_1["text"]], ignore_index=True)
        df["texts"] = df["texts"].apply(lambda x: x.replace("\n", " "))
        df["label"] = pd.concat([df_group_0["label"], df_group_1["label"]], ignore_index=True)
        # Encoding the label column
        df['label'] = df['label'].map({group_1.label: 1, group_0.label: 0})
        df.to_csv(get_dataframes_path().joinpath(f'{lang}_df.csv'))

        # create the same dataframe with cleaned texts
        cleaned_df = pd.DataFrame()
        cleaned_df["cleaned_paragraphs"] = df["paragraphs"].apply(lambda x: clean_paragraphs(x, lang))
        cleaned_df["cleaned_texts"] = df["texts"].apply(lambda x: clean_texts(x, lang))
        cleaned_df["label"] = df["label"]
        df.reset_index()
        cleaned_df.to_csv(get_cleaned_dataframes_path().joinpath(f'{lang}_df_cleaned.csv'))
# %%
