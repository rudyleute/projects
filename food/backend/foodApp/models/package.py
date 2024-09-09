from django.db import models
from .ingredient import Ingredient
from .unit import Unit

class Package(models.Model):
    barcode = models.CharField(max_length=48, blank=True, null=True)
    id = models.UUIDField(primary_key=True)
    calories = models.IntegerField()
    metric = models.FloatField(blank=True, null=True)
    ingredient = models.ForeignKey(Ingredient, models.DO_NOTHING)
    unit = models.ForeignKey(Unit, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'package'