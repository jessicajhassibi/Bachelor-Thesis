import json
import os

import pandas as pd
import wikipediaapi
import re


class WikiScraper:
    wiki_wiki = wikipediaapi.Wikipedia(
        language="de",
        extract_format=wikipediaapi.ExtractFormat.WIKI
    )

    def __init__(self):
        print("New WikiScraper initialized.\n")

    def check_exist(self, file):
        # check if file exists
        pages_texts_dict = {}
        if os.path.isfile(file):
            print("Texts have already been scraped to:", file)
            with open(file, "r", encoding="utf-8") as json_file:
                json_file_text = json_file.read()
                pages_texts_dict = json.loads(json_file_text)
        return pages_texts_dict

    def print_categories(self, page):
        categories = page.categories
        for title in sorted(categories.keys()):
            print("%s: %s" % (title, categories[title]))

    def clean_text(self, text):
        cleaned_text = re.sub('=+\s*.+\s*=+', '',
                              text)  # removes section header "== Einzelnachweise =="
        cleaned_text = re.sub('\n\n.+\n', ' ', cleaned_text)  # removes other section headers
        cleaned_text = re.sub('\n\n\n', '', cleaned_text)  # removes new lines at end of article
        cleaned_text = re.sub('\n', ' ', cleaned_text)
        return cleaned_text

    def extract_texts(self, pagenames, lang: str, label: str):
        pages_texts_dict: dict = {}
        i = 0
        for page in pagenames:
            try:
                wiki_page = self.wiki_wiki.page(page)
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
                # Run this code to set each paragraph as a document
                page_documents = []
                page_documents.append(linked_page.summary) # Summary of the page as one document
                for section in linked_page.sections:
                    cleaned_text = self.clean_text(section.text)
                    if cleaned_text != "":
                        page_documents.append(cleaned_text)

                # or whole article as one document:
                cleaned_text = self.clean_text(linked_page.text)
                if cleaned_text != "":
                    # create new dict for composer page
                    row_dict: dict = {}
                    pages_texts_dict[i] = row_dict

                    # dictionary keys definitions
                    key_title = "title"
                    key_paragraphs = "paragraphs"
                    key_text = "text"
                    key_categories = "categories"
                    key_label = "label"

                    pages_texts_dict[i][key_title] = page_lang
                    pages_texts_dict[i][key_text] = cleaned_text
                    pages_texts_dict[i][key_paragraphs] = page_documents
                    pages_texts_dict[i][key_categories] = page_categories
                    row_dict[key_label] = label
            except KeyError:
                print(f"article for {page} not existing in language {lang}\n    ")
        return pages_texts_dict

    def extract_persecuted_composers_texts(self, langs):
        for lang in langs:
            file = f"../data/persecuted_composers/{lang}_texts_composers_persecuted.json"
            if not self.check_exist(file): # not True == dict empty == file does not exist
                print("\nProcessing wikipedia pages in language: ", lang)
                wiki_page = self.wiki_wiki.page("Liste der vom NS-Regime oder seinen Verbündeten verfolgten Komponisten")
                linked_pages = [key for key in wiki_page.links.keys()] # TODO: nur Komponisten
                # print_categories(wiki_page)
                with open(file, "w") as json_file:
                    pages_texts_dict = self.extract_texts(linked_pages, lang, "persecuted")
                    json.dump(pages_texts_dict, json_file, indent=4, ensure_ascii=False, separators=(",", ": "))

    def extract_supported_composers_texts(self, langs):# TODO: work on that
        # Source "Gottbegnadeten-Liste" on Wikipedia
        supported_composers = ["Richard Strauss", "Hans Pfitzner", "Johann Nepomuk David", "Werner Egk",
                               "Gerhard Frommel", "Harald Genzmer", "Ottmar Gerster", "Kurt Hessenberg",
                               "Paul Höffer", "Karl Höller", "Mark Lothar", "Josef Marx", "Gottfried Müller",
                               "Carl Orff", "Ernst Pepping", "Max Trapp", "Fried Walter", "Hermann Zilcher"]
        for lang in langs:
            file = f"../data/supported_composers/{lang}_texts_composers_supported.json"
            if not self.check_exist(file):  # not True == dict empty == file does not exist
                with open(file, "w") as json_file:
                    print("\nProcessing wikipedia pages in language: ", lang)
                    pages_texts_dict = self.extract_texts(supported_composers, lang, "supported")
                    json.dump(pages_texts_dict, json_file, indent=4, ensure_ascii=False, separators=(",", ": "))

    def scrape_pages_multiple_languages(self, pagename, langs):
        # create pandas dataframe with composers as keys and \
        # for each key a dictionary with the texts of the wikipedia articles \
        # in the languages german, arabic, english, italian, french and spanish
        if pagename == "Liste der vom NS-Regime oder seinen Verbündeten verfolgten Komponisten":
            self.extract_persecuted_composers_texts(langs)
        elif pagename == "Gottbegnadeten-Liste":
            self.extract_supported_composers_texts(langs)
        else:
            print("WikiScraper does not know how to read composers from given wikipedia page name.")



