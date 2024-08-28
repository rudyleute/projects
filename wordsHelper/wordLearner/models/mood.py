from django.db import models
from .language import Language

class Mood(models.Model):
    mood_id = models.UUIDField(primary_key=True)
    mood_name = models.CharField(max_length=50)
    mood_fk_language = models.ForeignKey(Language, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'mood'