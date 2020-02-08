import random

from django.http import Http404
from django.shortcuts import render, get_object_or_404

from ..models import Exercise, Word, Definition


def get_wrong_definition(selected_word) -> Definition:
    definition = Definition.random()
    while definition in selected_word.definition_set.all():
        definition = Definition.random()
    return definition


def get_correct_definition(selected_word) -> Definition:
    count = selected_word.definition_set.count()
    random_index = random.randint(0, count - 1)
    return selected_word.definition_set.all()[random_index]


def get_definitions_for_exercise(selected_word: Word, no_definitions: int = 4) -> list:
    wrong_definitions = [
        get_wrong_definition(selected_word) for _ in [0] * (no_definitions - 1)
    ]
    all_definitions = wrong_definitions + [get_correct_definition(selected_word)]
    random.shuffle(all_definitions)
    return all_definitions


def index(request):
    selected_word = Word.random()
    definitions = get_definitions_for_exercise(selected_word)
    print(definitions)
    context = {"selected_word": selected_word, "definitions": definitions}
    return render(request, "exercises/index.html", context)
