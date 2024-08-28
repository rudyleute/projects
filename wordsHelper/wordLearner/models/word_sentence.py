from django.db import models
from .word import Word
from .sentence import Sentence

class WordSentence(models.Model):
    word = models.OneToOneField(Word, models.DO_NOTHING, primary_key=True)  # The composite primary key (word_id, sentence_id) found, that is not supported. The first column is selected.
    sentence = models.ForeignKey(Sentence, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'word_sentence'
        unique_together = (('word', 'sentence'),)