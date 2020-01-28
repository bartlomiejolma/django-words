from django.urls import path

from .views import list_words

app_name = "words"
urlpatterns = [
    path("list", list_words.index, name="index"),
    path("list/<int:word_id>/", list_words.detail, name="detail"),
    path("list/<int:word_id>/definitions/", list_words.definitions, name="definition"),
]
