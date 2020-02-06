from django.urls import path

from .views import list_words, exercises

app_name = "words"
urlpatterns = [
    path("list", list_words.index, name="index"),
    path("list/<int:word_id>/", list_words.detail, name="detail"),
    path("exercises", exercises.index, name="exercises"),
]
