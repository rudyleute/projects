from django.db import models
from .brand import Brand
from .category import Category

class CategoryBrand(models.Model):
    category = models.OneToOneField(Category, models.DO_NOTHING, primary_key=True)  # The composite primary key (category_id, brand_id) found, that is not supported. The first column is selected.
    brand = models.ForeignKey(Brand, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'category_brand'
        unique_together = (('category', 'brand'),)