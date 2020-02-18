import time

import requests
import json

from .settings_oxford_dict import APP_ID, APP_KEY

def request_word(word_id: str):

    LANGUAGE = "en-gb"
    url = f"https://od-api.oxforddictionaries.com:443/api/v2/entries/{LANGUAGE}/{word_id.lower()}"
    r = requests.get(url, headers={"app_id": APP_ID, "app_key": APP_KEY})
    return r.json()


def get_definition_data(sense, lexicalEntry):
    wanted_keys = ["definitions", "examples"]
    defintion_data = {
        wanted_key: sense.get(wanted_key, [None])[0] for wanted_key in wanted_keys
    }
    defintion_data["phoneticSpelling"] = lexicalEntry.get("pronunciations", [{}])[
        0
    ].get("phoneticSpelling", None)
    return defintion_data


def extract_definitions(result):
    return [
        get_definition_data(sense=sense, lexicalEntry=lexicalEntry)
        for lexicalEntry in result["lexicalEntries"]
        for entry in lexicalEntry["entries"]
        for sense in entry["senses"]
    ]


def extract_relevant_data(oxford_results: dict):
    relevant_word_keys = ["word", "type"]
    words_definitions = []
    for result in oxford_results.get("results", []):
        word_data = {
            relevant_word_key: result[relevant_word_key]
            for relevant_word_key in relevant_word_keys
        }
        definitions = extract_definitions(result)
        words_definitions.append((word_data, definitions))
    return words_definitions


def request_data_about_line(valid_word_line):
    word = valid_word_line.split(" - ")[0]
    print(f"{word}")
    time.sleep(1)
    r = request_word(word)
    return extract_relevant_data(r)


def get_data_for_words(word_lines):
    valid_word_lines = [
        word_line for word_line in word_lines if next(iter(word_line), "").isalnum()
    ]
    return [
        request_data_about_line(valid_word_line) for valid_word_line in valid_word_lines
    ]


def get_data_from_file(words_file_path):
    with open(words_file_path, "r", encoding="utf-8") as words_file:
        get_data_from_file_stream(words_file)


def get_data_from_file_stream(words_file):
    word_lines = words_file.readlines()
    return get_data_for_words(word_lines)

