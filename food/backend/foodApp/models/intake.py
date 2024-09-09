from django.db import models

class Intake(models.Model):
    date = models.DateField(primary_key=True)
    weight = models.FloatField()
    height = models.IntegerField()
    age = models.IntegerField()
    calories_delta = models.FloatField()

    class Meta:
        managed = False
        db_table = 'intake'