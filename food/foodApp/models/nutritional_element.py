from django.db import models
from .unit import Unit

class NutritionalElement(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(unique=True, max_length=40)
    min = models.FloatField(blank=True, null=True)
    max = models.FloatField(blank=True, null=True)
    unit = models.ForeignKey(Unit, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'nutritional_element'