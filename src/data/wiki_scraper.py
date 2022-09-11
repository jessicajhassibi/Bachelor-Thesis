import json
from pathlib import Path

import wikipediaapi

from .data_helpers import get_groups, get_json_target_path
from .models import Group


def scrape_and_generate_data():
    print("Collecting groups...")
    group_0, group_1 = get_groups()
    _scrape_page_with_list(group_0)
    _scrape_page_with_list(group_1)
    print("")
    print("")
    print("----------------------------------")
    print("FINISHED WIKIPEDIA SCRAPING!")
    print("----------------------------------")
    print("")
    print("")


def _scrape_page_with_list(group: Group):
    wiki_api = wikipediaapi.Wikipedia(
        language=group.wiki_main_language,
        extract_format=wikipediaapi.ExtractFormat.WIKI
    )
    print("\nProcessing wikipedia page: {} \nin language: {}".format(group.wiki_page, group.wiki_main_language))
    wiki_page = wiki_api.page(group.wiki_page)

    print(f"Collecting sub-pages that contains {'or'.join(group.wiki_categories)} categories only...")
    # collect pages name if it refers to one of the defined categories only.
    filtered_pages: list = []
    for page in wiki_page.links.keys():
        sub_page = wiki_api.page(page)
        if not sub_page.exists():
            print(f"IGNORED: {sub_page.title} PAGE DOESN'T EXIST...")
        elif not _matches_defined_categories(group.wiki_categories, group.wiki_alternative_categories,
                                             sub_page.categories.keys(), sub_page.summary):
            print(f"IGNORED: {sub_page.title} CATEGORIES DIDN'T MATCH...")
        else:
            print(f"FOUND: {sub_page.title} is {'or'.join(group.wiki_categories)}")
            filtered_pages.append(page)

    _scrape_pages(filtered_pages, group)


def _scrape_pages(pages_name: list, group: Group):
    print("")
    print("")
    print("-----------------------------------------------------")
    print(f"Scraping filtered list of pages for {group.label}...")
    print("-----------------------------------------------------")
    print("")
    print("")

    for lang in group.wiki_languages:
        json_path: Path = get_json_target_path(group.wiki_page, group.label, lang)
        if not json_path.exists():  # not True == dict empty == file does not exist
            pages_data_dict: dict = {}
            i = 1
            for page_name in pages_name:
                wiki_api = wikipediaapi.Wikipedia(
                    language=lang,
                    extract_format=wikipediaapi.ExtractFormat.WIKI
                )
                wiki_page = wiki_api.page(page_name)

                print("Processing page: {} \nin language: {}".format(page_name, lang))
                # page language is predefined in wiki_api object

                # ------ creating new json dict ------
                # first get the page title
                json_dict: dict = {"title": page_name}
                # then page summary
                text = wiki_page.summary
                if not text:
                    # if empty page then skip
                    continue
                json_dict["text"] = text
                # then categories
                page_categories = []
                for category in wiki_page.categories.keys():  # extract categories related to page
                    page_categories.append(category)
                json_dict["categories"] = page_categories
                # then labels
                json_dict["label"] = group.label
                # ------ and finally append it -------
                pages_data_dict[i] = json_dict

                # increment for next element
                i += 1
            # dump the collected data into target folder
            _dump_data(json_path, pages_data_dict)
        else:
            print(f"\nPage was already scraped under: {json_path}")


def _dump_data(json_path: Path, pages_data_dict):
    with open(json_path, "w") as json_file:
        print("Dumping data into:", json_path)
        json.dump(pages_data_dict, json_file, indent=4, ensure_ascii=False, separators=(",", ": "))


def _matches_defined_categories(defined_categories, defined_alternative_categories, page_categories, page_summary):
    # if one of the defined categories are found in the subpages categories then use it
    # First case
    for defined_category in defined_categories:
        for page_category in page_categories:
            if defined_category.lower() in page_category.lower():
                return True

    # Second case
    for defined_category in defined_categories:
        if defined_category.lower() in page_summary.lower():
            for alt_category in defined_alternative_categories:
                for page_category in page_categories:
                    if alt_category.lower() in page_category.lower():
                        return True

    # else ignore this subpage/link
    return False
