from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404

from .models import Word


def index(request):
    latest_word_list = Word.objects.order_by("-added_date")[:5]
    context = {"latest_word_list": latest_word_list}
    return render(request, "words/index.html", context)


def detail(request, word_id):
    word = get_object_or_404(Word, pk=word_id)
    return render(request, "words/detail.html", {"word": word})


def definitions(request, word_id):
    response = f"You're looking at the definitions of {word_id}."
    return HttpResponse(response)
