from django.http import HttpResponse, Http404
from django.shortcuts import render

from .models import Word


def index(request):
    latest_word_list = Word.objects.order_by("-added_date")[:5]
    context = {"latest_word_list": latest_word_list}
    return render(request, 'words/index.html', context)


def detail(request, word_id):
    try:
        word = Word.objects.get(pk=word_id)
    except Word.DoesNotExist:
        raise Http404("Word does not exist")
    return render(request, 'words/detail.html', {'word': word})


def definitions(request, word_id):
    response = f"You're looking at the definitions of {word_id}."
    return HttpResponse(response)
