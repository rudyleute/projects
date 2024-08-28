from django.db import models

class Number(models.TextChoices):
    SINGULAR = 'singular',
    PLURAL = 'plural'