from django.db import models

class Sentence(models.Model):
    sentence_id = models.UUIDField(primary_key=True)
    sentence_form = models.TextField()
    sentence_source = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sentence'