from django.db import models
from .recipy import Recipy

class Meal(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.TextField()  # This field type is a guess.
    time = models.DateTimeField()
    recipy = models.ForeignKey(Recipy, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'meal'