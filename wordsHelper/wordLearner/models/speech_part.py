from django.db import models

class SpeechPart(models.Model):
    speech_part_model_name = models.CharField(unique=True, max_length=10)
    speech_part_name = models.CharField(unique=True, max_length=30)
    speech_part_id = models.UUIDField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'speech_part'