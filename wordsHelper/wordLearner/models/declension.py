from django.db import models

class Declension(models.Model):
    declension_id = models.UUIDField(primary_key=True)
    declension_predecessor = models.CharField(max_length=20, blank=True, null=True)
    declension_person = models.TextField()  # This field type is a guess.
    declension_form = models.CharField(max_length=50)
    declension_taken_at = models.DateTimeField(blank=True, null=True)
    declension_number = models.TextField()  # This field type is a guess.
    declension_fk_word = models.ForeignKey('Word', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'declension'