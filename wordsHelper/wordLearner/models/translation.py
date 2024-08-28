from django.db import models

class Translation(models.Model):
    translation_source = models.OneToOneField('Word', models.DO_NOTHING, primary_key=True)  # The composite primary key (translation_source_id, translation_target_id) found, that is not supported. The first column is selected.
    translation_target = models.ForeignKey('Word', models.DO_NOTHING, related_name='translation_translation_target_set')

    class Meta:
        managed = False
        db_table = 'translation'
        unique_together = (('translation_source', 'translation_target'),)
