from django.db import models
from .package import Package
from .nutritional_element import NutritionalElement
from .unit import Unit

class Nutrition(models.Model):
    metric = models.FloatField()
    package = models.OneToOneField(Package, models.DO_NOTHING, primary_key=True)  # The composite primary key (package_id, nutritional_element_id) found, that is not supported. The first column is selected.
    nutritional_element = models.ForeignKey(NutritionalElement, models.DO_NOTHING)
    unit = models.ForeignKey(Unit, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'nutrition'
        unique_together = (('package', 'nutritional_element'),)