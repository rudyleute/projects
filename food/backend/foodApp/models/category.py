from django.db import models

class Category(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=60)
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category'
        unique_together = (('name', 'parent'),)