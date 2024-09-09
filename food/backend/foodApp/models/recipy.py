from django.db import models

class Recipy(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'recipy'