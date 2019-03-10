from django.db import models

from core.models.base import BaseModel


class TaxonomicKingdom(BaseModel):
    class Meta:
        app_label = 'core'
        default_permissions = ()
        db_table = 'taxonomic_kingdoms'

    name = models.CharField(max_length=45, unique=True)

    def __str__(self):
        return self.name
