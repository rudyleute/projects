from django.db import models
from .package import Package
from .unit import Unit
from .meal import Meal

class Consumption(models.Model):
    id = models.UUIDField(primary_key=True)
    package = models.ForeignKey(Package, models.DO_NOTHING)
    meal = models.ForeignKey(Meal, models.DO_NOTHING)
    metric = models.FloatField()
    unit = models.ForeignKey(Unit, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'consumption'