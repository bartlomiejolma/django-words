from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views import generic

from ..models import Word


class IndexView(generic.ListView):
    template_name = "words/index.html"
    context_object_name = "latest_word_list"

    def get_queryset(self):
        """Return the last five added words."""
        return Word.objects.order_by("-added_date")[:5]


class DetailView(generic.DetailView):
    model = Word
    template_name = "words/detail.html"
