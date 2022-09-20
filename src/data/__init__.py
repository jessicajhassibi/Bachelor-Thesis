import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
from .data_analysis import language_analyzer
from .data_analysis import plot_scraped_data
from .models import Group
from .wiki_scraper import scrape_and_generate_data
from .data_helpers import get_documents_list, get_cleaned_dataframes, \
    get_dataframes, create_dataframes, get_languages, get_dataframe_from_json
from .path_helpers import get_topic_modeling_path
from .config_helpers import get_groups, get_languages, get_top2vec_embedding_model

