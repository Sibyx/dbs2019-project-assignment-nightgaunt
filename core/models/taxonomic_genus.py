from django.db import models

from core.models.base import BaseModel
from core.models.taxonomic_family import TaxonomicFamily


class TaxonomicGenus(BaseModel):
    class Meta:
        app_label = 'core'
        default_permissions = ()
        db_table = 'taxonomic_genuses'

    taxonomic_family = models.ForeignKey(TaxonomicFamily, on_delete=models.CASCADE)
    name = models.CharField(max_length=45, unique=True)

    def __str__(self):
        return self.name
