from django.db import models

class Language(models.Model):
    language_id = models.UUIDField(primary_key=True)
    language_name = models.CharField(unique=True, max_length=20)
    language_set_1_code = models.CharField(unique=True, max_length=2)
    language_set_2t_code = models.CharField(unique=True, max_length=3)

    class Meta:
        managed = False
        db_table = 'language'