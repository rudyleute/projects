from django.db import models

class Unit(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(unique=True, max_length=30)
    short_name = models.CharField(unique=True, max_length=5)
    proportion_of_parent = models.FloatField(blank=True, null=True)
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'unit'