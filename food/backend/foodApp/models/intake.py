from django.db import models
from .activity_level import ActivityLevel

class Intake(models.Model):
    date = models.DateField(primary_key=True)
    weight = models.FloatField()
    height = models.IntegerField()
    age = models.IntegerField()
    calories_delta = models.FloatField()
    activity_level = models.ForeignKey(ActivityLevel, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'intake'