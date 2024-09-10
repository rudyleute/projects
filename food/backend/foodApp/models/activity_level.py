from django.db import models

class ActivityLevel(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(unique=True, max_length=15)
    multiplier = models.FloatField(unique=True)
    description = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'activity_level'