from django.db import models

class Person(models.TextChoices):
    FIRST = "first"
    SECOND = "second"
    THIRD = "third"