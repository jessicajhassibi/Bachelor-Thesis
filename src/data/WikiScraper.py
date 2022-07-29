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
        print("New WikiScraper initialized.")

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

    def extract_texts(self, pagenames, langs: list):
        pages_texts_dict: dict = {}
        i = 0
        for page in pagenames:
            try:
                wiki_page = self.wiki_wiki.page(page)

                i += 1
                print("\nProcessing wikipedia pages of", page)
                # TODO: add text columns

                row_dict: dict = {}
                for col_name in ["title", "paragraphs", "categories"]:
                    for lang in langs:
                        row_dict[f"{lang}_{col_name}"] = ""
                pages_texts_dict[i] = row_dict

                linked_page = wiki_page
                # ro get all languages:
                # print(composer_wiki_page.langlinks)
                for lang in langs:
                    key_title = lang + "_title"
                    key_paragraphs = lang + "_paragraphs"
                    key_categories = lang + "_categories"
                    try:
                        if lang != "de":
                            # get wiki article of composer in foreign language
                            linked_page = wiki_page.langlinks[lang]
                        page_lang = linked_page.title  # name of page in certain language
                        pages_texts_dict[i][key_title] = page_lang
                        page_categories = []
                        for category in linked_page.categories.keys():  # extract categories related to page
                            page_categories.append(category)
                        pages_texts_dict[i][key_categories] = page_categories

                        # Run this code to set each paragraph as a document
                        page_sections = linked_page.sections
                        page_documents = []
                        for section in page_sections:
                            cleaned_text = re.sub('=+\s*.+\s*=+', '',
                                                  section.text)  # removes section header "== Einzelnachweise =="
                            cleaned_text = re.sub('\n\n.+\n', ' ', cleaned_text)  # removes other section headers
                            cleaned_text = re.sub('\n\n\n', '', cleaned_text)  # removes new lines at end of article
                            cleaned_text = re.sub('\n', ' ', cleaned_text)
                            if cleaned_text != "":
                                page_documents.append(cleaned_text)
                        pages_texts_dict[i][key_paragraphs] = page_documents

                        # or whole article as one document:
                        # cleaned_text = re.sub('=+\s*.+\s*=+', '', linked_page.text)  # removes section header "== Einzelnachweise =="
                        # cleaned_text = re.sub('\n\n.+\n', ' ', cleaned_text)  # removes other section headers
                        # cleaned_text = re.sub('\n\n\n', '', cleaned_text)  # removes new lines at end of article
                        # cleaned_text = re.sub('\n', ' ', cleaned_text)
                        # pages_texts_dict[i][key_text] = cleaned_text

                    except KeyError:
                        # article not existing in selected language
                        pages_texts_dict[i][key_title] = ""
                        pages_texts_dict[i][key_paragraphs] = ""
                        pages_texts_dict[i][key_categories] = ""
            except Exception as err:
                print("Except")
        return pages_texts_dict

    def extract_persecuted_composers_texts(self, langs):
        file = "../data/verfolgte_komponisten_texte.json"
        if not self.check_exist(file): # not True == dict empty == file does not exist
            wiki_page = self.wiki_wiki.page("Liste der vom NS-Regime oder seinen Verbündeten verfolgten Komponisten")
            linked_pages = [key for key in wiki_page.links.keys()]
            # print_categories(wiki_page)
            with open(file, "w") as json_file:
                pages_texts_dict = self.extract_texts(linked_pages, langs)
                json.dump(pages_texts_dict, json_file, indent=4, ensure_ascii=False, separators=(",", ": "))
        df = pd.read_json(file)
        # transpose index and columns of df
        df = df.transpose()
        return df

    def extract_supported_composers_texts(self, langs):# TODO: work on that
        file = "../data/unterstützte_komponisten_texte.json"
        if not self.check_exist(file): # not True == dict empty == file does not exist
            # Source "Gottbegnadeten-Liste" on Wikipedia
            supported_composers = ["Richard Strauss", "Hans Pfitzner", "Johann Nepomuk David", "Werner Egk",
                                   "Gerhard Frommel", "Harald Genzmer", "Ottmar Gerster", "Kurt Hessenberg",
                                   "Paul Höffer", "Karl Höller", "Mark Lothar", "Josef Marx", "Gottfried Müller",
                                   "Carl Orff", "Ernst Pepping", "Max Trapp", "Fried Walter", "Hermann Zilcher"]
            with open(file, "w") as json_file:
                pages_texts_dict = self.extract_texts(supported_composers, langs)
                json.dump(pages_texts_dict, json_file, indent=4, ensure_ascii=False, separators=(",", ": "))
        df = pd.read_json(file)
        # transpose index and columns of df
        df = df.transpose()
        return df


