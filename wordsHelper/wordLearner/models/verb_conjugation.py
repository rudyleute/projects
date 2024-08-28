from django.db import models

from .tense import Tense
from .mood import Mood
from wordLearner.enums.voice import Voice
from wordLearner.enums.number import Number
from wordLearner.enums.gender import Gender
from wordLearner.enums.person import Person

class VerbConjugation(models.Model):
    verb_conjugation_id = models.UUIDField(primary_key=True)
    verb_conjugation_voice = models.CharField(
        choices=Voice.choices
    )
    verb_conjugation_fk_tense = models.ForeignKey(Tense, models.DO_NOTHING)
    verb_conjugation_fk_mood = models.ForeignKey(Mood, models.DO_NOTHING)
    verb_conjugation_form = models.CharField(max_length=100)
    verb_conjugation_person = models.CharField(
        choices=Person.choices
    )
    verb_conjugation_gender = models.CharField(
        blank=True,
        null=True,
        choices=Gender.choices
    )
    verb_conjugation_number = models.CharField(
        choices=Number.choices
    )
    verb_conjugation_fk_word = models.ForeignKey('Word', models.DO_NOTHING)
    verb_conjugation_taken_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'verb_conjugation'