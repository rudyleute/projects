from django.db import models
from .speech_part import SpeechPart
from .frequency import Frequency
from .language import Language

class Word(models.Model):
    word_lemma = models.CharField(max_length=50)
    word_id = models.UUIDField(primary_key=True)
    word_fk_speech_part = models.ForeignKey(SpeechPart, models.DO_NOTHING, blank=True, null=True)
    word_initial_form = models.CharField(unique=True, max_length=100)
    word_fk_frequency = models.ForeignKey(Frequency, models.DO_NOTHING, blank=True, null=True)
    word_frequency_class = models.IntegerField(blank=True, null=True)
    word_fk_language = models.ForeignKey(Language, models.DO_NOTHING)
    word_taken_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'word'