from django.db import models

class Brand(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'brand'