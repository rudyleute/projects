from django.db import models
from .language import Language

class Tense(models.Model):
    tense_id = models.UUIDField(primary_key=True)
    tense_name = models.CharField(max_length=70)
    tense_fk_language = models.ForeignKey(Language, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'tense'