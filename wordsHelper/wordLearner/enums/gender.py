from django.db import models

class Gender(models.TextChoices):
    MASCULINE = 'masculine'
    FEMININE = 'feminine'
    NEUTER = 'neuter'
    COMMON = 'common'