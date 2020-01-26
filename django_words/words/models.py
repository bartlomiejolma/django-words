from django.db import models

class Word(models.Model):
    word_text = models.CharField(max_length=200)
    added_date = models.DateTimeField('date added')

class Definition(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    definition_text = models.CharField(max_length=500)

    # class PartOfSpeech(models.TextChoices):
    #     VERB = 'v.';_('verb')
    # world_part_of_speech = models
