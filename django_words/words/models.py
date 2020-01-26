from django.db import models

class World(models.Model):
    world_text = models.CharField(max_length=200)
    added_date = models.DateTimeField('date added')

class Definition(models.Model):
    world = models.ForeignKey(World, on_delete=models.CASCADE)
    definition_text = models.CharField(max_length=500)

    # class PartOfSpeech(models.TextChoices):
    #     VERB = 'v.';_('verb')
    # world_part_of_speech = models
