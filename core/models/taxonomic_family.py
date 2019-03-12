from django.db import models

from core.models.base import BaseModel
from core.models.taxonomic_order import TaxonomicOrder


class TaxonomicFamily(BaseModel):
    class Meta:
        app_label = 'core'
        default_permissions = ()
        db_table = 'taxonomic_families'

    taxonomic_order = models.ForeignKey(TaxonomicOrder, on_delete=models.CASCADE)
    name = models.CharField(max_length=45, unique=True)

    def __str__(self):
        return self.name
