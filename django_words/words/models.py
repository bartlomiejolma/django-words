import datetime
import random

from django.db import models
from django.utils import timezone


class Word(models.Model):
    word_text = models.CharField(max_length=200)
    added_date = models.DateTimeField("date added")
    word_class = models.CharField(max_length=200, default="")

    def __str__(self):
        return self.word_text

    def was_added_recently(self):
        return self.added_date >= timezone.now() - datetime.timedelta(days=1)

    @classmethod
    def random(cls):
        count = cls.objects.count()
        random_index = random.randint(1, count)
        return cls.objects.get(pk=random_index)


class Definition(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    definition_text = models.CharField(max_length=500)
    example = models.CharField(max_length=500, default="")
    phonetic = models.CharField(max_length=500, default="")

    def __str__(self):
        return self.definition_text


class Exercise(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    correct_answer = models.BooleanField()
    exercised_date = models.DateTimeField("exercised date")
