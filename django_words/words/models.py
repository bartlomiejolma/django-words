import datetime
import random

from django.db import models
from django.utils import timezone


class RandomSelectable(models.Model):
    @classmethod
    def random(cls):
        count = cls.objects.count()
        random_index = random.randint(1, count)
        return cls.objects.get(pk=random_index)

    class Meta:
        abstract = True


class Word(RandomSelectable):
    word_text = models.CharField(max_length=200)
    added_date = models.DateTimeField("date added")
    word_class = models.CharField(max_length=200, default="")

    def __str__(self):
        phonetic: str = self.definition_set.all()[0].phonetic
        if phonetic:
            return f"{self.word_text} /{phonetic}/"
        else:
            return self.word_text

    def was_added_recently(self):
        return self.added_date >= timezone.now() - datetime.timedelta(days=1)


class Definition(RandomSelectable):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    definition_text = models.CharField(max_length=500)
    example = models.CharField(max_length=500, default="", null=True)
    phonetic = models.CharField(max_length=500, default="", null=True)

    def __str__(self):
        return self.definition_text


class Exercise(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    correct_answer = models.BooleanField()
    exercised_date = models.DateTimeField("exercised date")
