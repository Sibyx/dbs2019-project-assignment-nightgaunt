from django.db import models

from core.models.base import BaseModel
from core.models.taxonomic_phylum import TaxonomicPhylum


class TaxonomicClass(BaseModel):
    class Meta:
        app_label = 'core'
        default_permissions = ()
        db_table = 'taxonomic_classes'

    taxonomic_phylum = models.ForeignKey(TaxonomicPhylum, on_delete=models.CASCADE)
    name = models.CharField(max_length=45, unique=True)
