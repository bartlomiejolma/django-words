from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def detail(request, word_id):
    return HttpResponse(f"You're looking at word {word_id}.")

def definitions(request, word_id):
    response = f"You're looking at the definitions of {word_id}."
    return HttpResponse(response)
