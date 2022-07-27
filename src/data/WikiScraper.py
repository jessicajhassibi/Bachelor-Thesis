import json
import os
import wikipediaapi
import re


class WikiScraper:
    wiki_wiki = wikipediaapi.Wikipedia(
        language="de",
        extract_format=wikipediaapi.ExtractFormat.WIKI
    )

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

    def extract_persecuted_composers_texts(self, file):
        if not self.check_exist(file): # not True == dict empty == file does not exist
            pages_texts_dict = {}
            wiki_page = self.wiki_wiki.page("Liste der vom NS-Regime oder seinen Verbündeten verfolgten Komponisten")
            linked_pages = [key for key in wiki_page.links.keys()]
            # print_categories(wiki_page)

            with open(file, "w") as json_file:
                i = 0
                for page in linked_pages:
                    try:
                        wiki_page = self.wiki_wiki.page(page)
                        #set to False, if you want just composers!
                        is_valid_composer = True
                        #for key in composer_wiki_page.categories.keys():
                        # exclude non-existing articles, and all articles which are not about a composer
                        #    if "Komponist" in key or "komponist" in key:
                        #        is_valid_composer = True
                        #        break
                        if is_valid_composer:
                            i+=1
                            print("\nProcessing wikipedia pages of", page)
                            # TODO: add text columns
                            pages_texts_dict[i] = {"de_title": "",
                                                   "en_title": "",
                                                   "ar_title": "",
                                                   "fr_title": "",
                                                   "it_title": "",
                                                   "es_title": "",
                                                   "de_paragraphs": "",
                                                   "en_paragraphs": "",
                                                   "ar_paragraphs": "",
                                                   "fr_paragraphs": "",
                                                   "it_paragraphs": "",
                                                   "es_paragraphs": "",
                                                   "de_categories": "",
                                                   "en_categories": "",
                                                   "ar_categories": "",
                                                   "fr_categories": "",
                                                   "it_categories": "",
                                                   "es_categories": "",
                                                    }
                            linked_page = wiki_page
                            # get all languages:
                            # print(composer_wiki_page.langlinks)
                            languages = ["de", "en", "ar", "fr", "it", "es"]
                            for lang in languages:
                                key_title = lang + "_title"
                                key_paragraphs = lang + "_paragraphs"
                                key_categories = lang + "_categories"
                                try:
                                    if lang != "de":
                                        # get wiki article of composer in foreign language
                                        linked_page = wiki_page.langlinks[lang]
                                    page_lang = linked_page.title # name of page in certain language
                                    pages_texts_dict[i][key_title] = page_lang
                                    page_categories = []
                                    for category in linked_page.categories.keys(): # extract categories related to page
                                        page_categories.append(category)
                                    pages_texts_dict[i][key_categories] = page_categories

                                    # Run this code to set each paragraph as a document
                                    page_sections = linked_page.sections
                                    page_documents = []
                                    for section in page_sections:
                                        #TODO: Werke & Nachweise entfernen?
                                        cleaned_text = re.sub('=+\s*.+\s*=+', '', section.text)  # removes section header "== Einzelnachweise =="
                                        cleaned_text = re.sub('\n\n.+\n', ' ', cleaned_text)  # removes other section headers
                                        cleaned_text = re.sub('\n\n\n', '', cleaned_text)  # removes new lines at end of article
                                        cleaned_text = re.sub('\n', ' ', cleaned_text)
                                        if cleaned_text!="":
                                            page_documents.append(cleaned_text)
                                    pages_texts_dict[i][key_paragraphs] = page_documents

                                    # or whole article as one document:
                                    # cleaned_text = re.sub('=+\s*.+\s*=+', '', linked_page.text)  # removes section header "== Einzelnachweise =="
                                    # cleaned_text = re.sub('\n\n.+\n', ' ', cleaned_text)  # removes other section headers
                                    # cleaned_text = re.sub('\n\n\n', '', cleaned_text)  # removes new lines at end of article
                                    # cleaned_text = re.sub('\n', ' ', cleaned_text)
                                    #pages_texts_dict[i][key_text] = cleaned_text

                                except KeyError:
                                    print(lang, "article not existing.")
                                    pages_texts_dict[i][key_title] = ""
                                    pages_texts_dict[i][key_paragraphs] = ""
                                    pages_texts_dict[i][key_categories] = ""
                    except Exception as err:
                        print("Except")
                json.dump(pages_texts_dict, json_file, indent=4, ensure_ascii=False, separators=(",", ": "))
            print(len(pages_texts_dict), "of", len(linked_pages),
                  "links in wikipedia list used.")
            return pages_texts_dict

    def extract_persecuted_composers_texts(self, file):# TODO: work on that
        if not self.check_exist(file): # not True == dict empty == file does not exist
            pages_texts_dict = {}
            wiki_page = self.wiki_wiki.page("Gottbegnadeten-Liste")


