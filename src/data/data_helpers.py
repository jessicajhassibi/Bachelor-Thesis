import os
import pandas as pd
import nlp


def get_full_language_word(lang):
    langs_dict = {"en":"english", "de":"german", "es":"spanish", "ar":"arabic", "fr":"french", "it":"italian"}
    return langs_dict[lang]


def get_dataframe_from_json(file: str):
    df = pd.read_json(file)
    # transpose index and columns of df
    df = df.transpose()
    return df


def get_documents_list(languages):
    documents = list()
    for lang in languages:
        lang_df = pd.read_csv(f"../data/dataframes/{lang}_df.csv")
        text_list = lang_df["text"].values.tolist()
        documents = documents + text_list
    return documents


def create_dataframes(langs: list):
    os.makedirs('../data/dataframes', exist_ok=True)
    for lang in langs:
        df_supported = get_dataframe_from_json(f"../data/supported_composers/{lang}_texts_composers_supported.json")
        df_persecuted = get_dataframe_from_json(f"../data/persecuted_composers/{lang}_texts_composers_persecuted.json")
        # create train dataframe using texts and labels
        combined_df = pd.DataFrame()
        combined_df["text"] = pd.concat([df_supported["text"], df_persecuted["text"]], ignore_index=True)
        combined_df["label"] = pd.concat([df_supported["label"], df_persecuted["label"]], ignore_index=True)
        combined_df.to_csv(f'../data/dataframes/{lang}_df.csv')

# TODO: geburtsdaten cleanen
# create new dataframes with cleaned text
def create_cleaned_dataframes(langs: list):
    os.makedirs('../data/dataframes/cleaned', exist_ok=True)
    for lang in langs:
        df_cleaned = pd.read_csv(f"../data/dataframes/{lang}_df.csv")
        df_cleaned.insert(1, "cleaned_text", df_cleaned["text"].apply(lambda x: nlp.clean_texts(x, "english")))
        df_cleaned.drop(labels="text",axis="columns", inplace=True)
        df_cleaned.drop(labels="Unnamed: 0",axis="columns", inplace=True)
        # Encoding the label column
        df_cleaned['label']=df_cleaned['label'].map({'supported': 1, 'persecuted': 0})
        # save cleaned dataframe
        df_cleaned.to_csv(f'../data/dataframes/cleaned/{lang}_df_cleaned.csv')


