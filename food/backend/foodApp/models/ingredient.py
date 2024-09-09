from django.db import models
from .category import Category
from .brand import Brand

class Ingredient(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=60)
    brand = models.ForeignKey(Brand, models.DO_NOTHING, blank=True, null=True)
    category = models.ForeignKey(Category, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'ingredient'