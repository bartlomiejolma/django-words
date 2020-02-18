from django.urls import path

from .views import list_words, exercises, add_words

app_name = "words"
urlpatterns = [
    path("batch", add_words.add, name="add_words"),
    path("batch/add", add_words.batch, name="add_batch"),
    path("list", list_words.IndexView.as_view(), name="index"),
    path("list/<int:pk>/", list_words.DetailView.as_view(), name="detail"),
    path("exercises", exercises.index, name="exercises"),
    path("exercises/<int:exercise_id>/result", exercises.result, name="exercises_results"),
    path("exercises/<int:exercise_id>/verify", exercises.verify, name="exercises_verify")
]
