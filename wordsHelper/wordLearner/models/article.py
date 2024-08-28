from django.db import models


class Article(models.Model):
    article_id = models.UUIDField(primary_key=True)
    article_form = models.CharField(max_length=5)
    article_fk_language = models.ForeignKey('Language', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'article'