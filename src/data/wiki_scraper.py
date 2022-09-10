import json
import os
from pathlib import Path

import wikipediaapi

from data.data_helpers import get_data_target_path, get_persecuted_composers_path, get_supported_composers_path

WIKI = wikipediaapi.Wikipedia(
    language="de",
    extract_format=wikipediaapi.ExtractFormat.WIKI
)


def check_exist(file):
    # check if file exists
    pages_texts_dict = {}
    if os.path.isfile(file):
        print(f"Texts have already been scraped to: {file}")
        with open(file, "r", encoding="utf-8") as json_file:
            json_file_text = json_file.read()
            pages_texts_dict = json.loads(json_file_text)
    return pages_texts_dict


def extract_texts(pagenames, lang: str, label: str):
    pages_texts_dict: dict = {}
    i = 0
    for page in pagenames:
        try:
            wiki_page = WIKI.page(page)
            i += 1
            print("Processing page of", page)
            if lang != "de":
                # get wiki article of composer in foreign language
                linked_page = wiki_page.langlinks[lang]
            else:
                linked_page = wiki_page

            page_lang = linked_page.title  # name of page in certain language
            page_categories = []
            for category in linked_page.categories.keys():  # extract categories related to page
                page_categories.append(category)
            text = linked_page.summary
            if text != "":
                # create new dict for composer page
                row_dict: dict = {}
                pages_texts_dict[i] = row_dict

                # dictionary keys definitions
                key_title = "title"
                key_text = "text"
                key_categories = "categories"
                key_label = "label"

                pages_texts_dict[i][key_title] = page_lang
                pages_texts_dict[i][key_text] = text
                pages_texts_dict[i][key_categories] = page_categories
                row_dict[key_label] = label
        except KeyError:
            print(f"article for {page} not existing in language {lang}\n    ")
    return pages_texts_dict


def extract_persecuted_composers_texts(langs):


    for lang in langs:
        file = get_persecuted_composers_path().joinpath(f"{lang}_texts_composers_persecuted.json")
        if not check_exist(file):  # not True == dict empty == file does not exist
            print("\nProcessing wikipedia pages in language: ", lang)
            wiki_page = WIKI.page("Liste der vom NS-Regime oder seinen Verbündeten verfolgten Komponisten")
            linked_pages = [key for key in wiki_page.links.keys()]  # TODO: nur Komponisten
            categories = wiki_page.categories
            #for title in sorted(categories.keys()):
            #    print("%s: %s" % (title, categories[title]))
            with open(file, "w") as json_file:
                pages_texts_dict = extract_texts(linked_pages, lang, "persecuted")
                json.dump(pages_texts_dict, json_file, indent=4, ensure_ascii=False, separators=(",", ": "))


def extract_supported_composers_texts(langs):


    # Source "Gottbegnadeten-Liste" on Wikipedia
    supported_composers = ["Richard Strauss", "Hans Pfitzner", "Johann Nepomuk David", "Werner Egk",
                           "Gerhard Frommel", "Harald Genzmer", "Ottmar Gerster", "Kurt Hessenberg",
                           "Paul Höffer", "Karl Höller", "Mark Lothar", "Josef Marx", "Gottfried Müller",
                           "Carl Orff", "Ernst Pepping", "Max Trapp", "Fried Walter", "Hermann Zilcher"]
    for lang in langs:
        file = get_supported_composers_path().joinpath(f"{lang}_texts_composers_supported.json")
        if not check_exist(file):  # not True == dict empty == file does not exist
            with open(file, "w") as json_file:
                print("\nProcessing wikipedia pages in language: ", lang)
                pages_texts_dict = extract_texts(supported_composers, lang, "supported")
                json.dump(pages_texts_dict, json_file, indent=4, ensure_ascii=False, separators=(",", ": "))


def scrape_pages_multiple_languages(pagename, langs):
    # create pandas dataframe with composers as keys and \
    # for each key a dictionary with the texts of the wikipedia articles \
    # in the languages german, arabic, english, italian, french and spanish
    if pagename == "Liste der vom NS-Regime oder seinen Verbündeten verfolgten Komponisten":
        extract_persecuted_composers_texts(langs)
    elif pagename == "Gottbegnadeten-Liste":
        extract_supported_composers_texts(langs)
    else:
        raise "WikiScraper does not know how to read composers from given wikipedia page name."
