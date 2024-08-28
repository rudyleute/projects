from django.db import models

class Voice(models.TextChoices):
    ACTIVE = "active"
    PASSIVE = "passive"