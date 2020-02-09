import random

from django.utils import timezone
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

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
    exercise = Exercise(
        word=selected_word, exercised_date=timezone.now(), correct_answer=False
    )
    exercise.save()
    definitions = get_definitions_for_exercise(selected_word)
    context = {
        "selected_word": selected_word,
        "definitions": definitions,
        "exercise": exercise,
    }
    return render(request, "exercises/index.html", context)


def result(request, exercise_id):
    exercise = get_object_or_404(Exercise, pk=exercise_id)
    context = {"word": exercise.word}
    if exercise.correct_answer:
        context["message"] = "Correct answer"
    else:
        context["message"] = "You didn't select a correct answer"
    return render(request, "exercises/result.html", context)


def verify(request, exercise_id):
    exercise: Exercise = get_object_or_404(Exercise, pk=exercise_id)
    try:
        _ = exercise.word.definition_set.get(pk=request.POST["definition"])
    except (KeyError, Definition.DoesNotExist):
        print(request)
        exercise.correct_answer = False
    else:
        exercise.correct_answer = True
    finally:
        print(exercise)
        exercise.save()
        return HttpResponseRedirect(
            reverse("words:exercises_results", kwargs={"exercise_id": exercise_id},)
        )

