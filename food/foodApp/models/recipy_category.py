from django.db import models
from .category import Category
from .recipy import Recipy
from .unit import Unit

class RecipyCategory(models.Model):
    metric = models.FloatField()
    category = models.OneToOneField(Category, models.DO_NOTHING, primary_key=True)  # The composite primary key (category_id, recipy_id) found, that is not supported. The first column is selected.
    recipy = models.ForeignKey(Recipy, models.DO_NOTHING)
    unit = models.ForeignKey(Unit, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'recipy_category'
        unique_together = (('category', 'recipy'),)