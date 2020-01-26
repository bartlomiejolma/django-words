import datetime

from django.db import models
from django.utils import timezone


class Word(models.Model):
    word_text = models.CharField(max_length=200)
    added_date = models.DateTimeField("date added")

    def __str__(self):
        return self.word_text

    def was_added_recently(self):
        return self.added_date >= timezone.now() - datetime.timedelta(days=1)


class Definition(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    definition_text = models.CharField(max_length=500)

    def __str__(self):
        return self.definition_text

    # class PartOfSpeech(models.TextChoices):
    #     VERB = 'v.';_('verb')
    # world_part_of_speech = models
