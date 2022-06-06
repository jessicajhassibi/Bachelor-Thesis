"""
Holds the from the bachelor_thesis jupyter notebook in case the reader doesn't use jupyter.
"""
import json
import os
import wikipediaapi


def print_categories(page):
    categories = page.categories
    for title in sorted(categories.keys()):
        print("%s: %s" % (title, categories[title]))

if __name__ == '__main__':
    page_of_all_composers = "Liste der vom NS-Regime oder seinen Verbündeten verfolgten Komponisten"
    wiki_wiki = wikipediaapi.Wikipedia(
        language="de",
        extract_format=wikipediaapi.ExtractFormat.WIKI
    )
    wiki_page = wiki_wiki.page(page_of_all_composers)
    persecuted_composers = [key for key in wiki_page.links.keys()] # TODO: Entferne Links, zu Seiten, die keine Komponisten sind? Oder drin lassen?
    #print_categories(wiki_page)

    file = "data/komponisten_texte_deutsch.json"
    # check if file exists
    if os.path.isfile(file):
        print("Texts have already been scraped to:", file)
        with open(file, "r", encoding="utf8") as json_file:
            json_file_text = json_file.read()
            composer_texts_dict = json.loads(json_file_text)

    else:
        # get german text from each composers wikipedia page and save in json-file
        with open(file, "w") as json_file:
            composer_texts_dict = {}
            for composer in persecuted_composers:
                composer_wiki_page = wiki_wiki.page(composer)
                # exclude non-existing articles, and all articles which are not about a composer
                valid_composer = False
                for key in composer_wiki_page.categories.keys():
                    if "Komponist" in key or "komponist" in key:
                        valid_composer = True
                        break
                if valid_composer:
                    print("Processing wikipedia page of", composer)
                    # composer_wiki_page.sections TODO: Überschriften, Literatur etc. aus Text entfernen?
                    composer_text = composer_wiki_page.text
                    # composer_text = composer_text.replace("\n\n\n", " ")
                    # composer_text = composer_text.replace("\n\n", " ")
                    # composer_text = composer_text.replace("\n", " ")
                    composer_texts_dict[composer] = composer_text
                    # get other languages:
                    # composer_wiki_page.langlinks
            json.dump(composer_texts_dict, json_file, indent=4, ensure_ascii=False)

        print(len(composer_texts_dict), "of", len(persecuted_composers), "are valid wikipedia pages of composers.")





