from django.db import models
from .article import Article

class Nouns(models.Model):
    noun_fk_word = models.OneToOneField('Word', models.DO_NOTHING, primary_key=True)
    noun_fk_article = models.ForeignKey(Article, models.DO_NOTHING)
    noun_plural = models.CharField(max_length=50)
    noun_plural_taken_at = models.DateTimeField(blank=True, null=True)
    noun_article_taken_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nouns'