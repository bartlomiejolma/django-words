from django.urls import path

from .views import list_words, exercises

app_name = "words"
urlpatterns = [
    path("list", list_words.index, name="index"),
    path("list/<int:word_id>/", list_words.detail, name="detail"),
    path("exercises", exercises.index, name="exercises"),
    path("exercises/<int:exercise_id>/result", exercises.result, name="exercises_results"),
    path("exercises/<int:exercise_id>/verify", exercises.verify, name="exercises_verify")
]
