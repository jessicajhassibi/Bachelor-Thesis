import json
import os
import wikipediaapi
from jsonlines import jsonlines


def print_categories(page):
    categories = page.categories
    for title in sorted(categories.keys()):
        print("%s: %s" % (title, categories[title]))


def extract_composers_texts(file):
    # check if file exists
    # TODO remove not
    if os.path.isfile(file):
        print("Texts have already been scraped to:", file)
        with open(file, "r", encoding="utf8") as json_file:
            json_file_text = json_file.read()
            composer_texts_dict = json.loads(json_file_text)
    else:
        page_of_all_composers = "Liste der vom NS-Regime oder seinen Verbündeten verfolgten Komponisten"
        wiki_wiki = wikipediaapi.Wikipedia(
            language="de",
            extract_format=wikipediaapi.ExtractFormat.WIKI
        )
        wiki_page = wiki_wiki.page(page_of_all_composers)
        persecuted_composers = [key for key in wiki_page.links.keys()]
        # print_categories(wiki_page)

        with open(file, "w") as json_file:
            composer_texts_dict = {}
            i = 0
            for composer in persecuted_composers:
                try:
                    composer_wiki_page = wiki_wiki.page(composer)
                    # exclude non-existing articles, and all articles which are not about a composer
                    #TODO set to False
                    is_valid_composer = True
                    #for key in composer_wiki_page.categories.keys():
                    #    if "Komponist" in key or "komponist" in key:
                    #        is_valid_composer = True
                    #        break
                    if is_valid_composer:
                        i+=1
                        print("\nProcessing wikipedia pages of", composer)
                        composer_texts_dict[i] = {"de_title": "",
                                                  "de_text": "",
                                                  "en_title": "",
                                                  "en_text": "",
                                                  "ar_title": "",
                                                  "ar_text": "",
                                                  "fr_title": "",
                                                  "fr_text": "",
                                                  "it_title": "",
                                                  "it_text": "",
                                                  "es_title": "",
                                                  "es_text": "",
                                                  }
                        composer_page = composer_wiki_page
                        # get all languages:
                        # print(composer_wiki_page.langlinks)
                        languages = ["de", "en", "ar", "fr", "it", "es"]
                        for lang in languages:
                            key_title = lang + "_title"
                            key_text = lang + "_text"
                            try:
                                if lang != "de":
                                    # get wiki article of composer in foreign language
                                    composer_page = composer_wiki_page.langlinks[lang]
                                composer_lang = composer_page.title
                                composer_text = composer_page.text
                                # composer_wiki_page.sections TODO: Überschriften, Literatur etc. aus Text entfernen?
                                # composer_text = composer_text.replace("\n\n\n", " ")
                                # composer_text = composer_text.replace("\n\n", " ")
                                # composer_text = composer_text.replace("\n", " ")
                                composer_texts_dict[i][key_title] = composer_lang
                                composer_texts_dict[i][key_text] = composer_text
                            except KeyError:
                                print(lang, "article not existing.")
                                composer_texts_dict[i][key_title] = ""
                                composer_texts_dict[i][key_text] = ""
                except Exception as err:
                    print("Except")
            json.dump(composer_texts_dict, json_file, indent=4, ensure_ascii=False, separators=(",", ": "))
        print(len(composer_texts_dict), "of", len(persecuted_composers),
              "links in wikipedia liste are valid composers.")
        return composer_texts_dict
