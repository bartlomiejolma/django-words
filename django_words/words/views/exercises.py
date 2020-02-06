from django.http import Http404
from django.shortcuts import render, get_object_or_404

from ..models import Exercise, Word


def index(request):
    selected_word = Word.random()
    context = {"selected_word": selected_word}
    return render(request, "exercises/index.html", context)
