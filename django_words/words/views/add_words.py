import os

from django.db import transaction
from django.utils import timezone

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from ..utils import oxford_dict
from ..models import Word, Definition


def add_definition_to_word(definition_data: dict, word):
    if definition_data["definitions"]:
        word.definition_set.create(
            definition_text=definition_data["definitions"],
            example=definition_data["examples"],
            phonetic=definition_data["phoneticSpelling"],
        )


def add_word_to_database(word_data: list):
    for (word_dict, definitions) in word_data:
        word = Word(
            word_text=word_dict["word"],
            added_date=timezone.now(),
            word_class=word_dict["type"],
        )
        with transaction.atomic():
            word.save()

            for definition_data in definitions:
                add_definition_to_word(definition_data, word)


def add_words_from_file(file):

    words_data = oxford_dict.get_data_for_words(file.read().decode("utf-8").split("\n"))
    add_words_to_database(words_data)


def add_words_from_text_blob(text_blob):
    words_data = oxford_dict.get_data_for_words(text_blob.split("\n"))
    add_words_to_database(words_data)


def add_words_to_database(words_data):
    for word_data in words_data:
        add_word_to_database(word_data)


def add(request):
    return render(request, "words/add.html")


def batch(request):
    if request.method == "POST":
        if "fileToUpload" in request.FILES:
            file = request.FILES["fileToUpload"]
            add_words_from_file(file)
            return HttpResponseRedirect(reverse("words:index"))
        if "textToUpload" in request.POST:
            text_blob = request.POST["textToUpload"]
            add_words_from_text_blob(text_blob)
            return HttpResponseRedirect(reverse("words:index"))

    return HttpResponseRedirect(reverse("words:add_words"))
