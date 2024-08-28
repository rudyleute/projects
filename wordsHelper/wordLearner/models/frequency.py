from django.db import models

class Frequency(models.Model):
    frequency_id = models.UUIDField(primary_key=True)
    frequency_label = models.CharField(unique=True, max_length=50)
    frequency_lowest_class = models.IntegerField(unique=True)
    frequency_highest_class = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'frequency'