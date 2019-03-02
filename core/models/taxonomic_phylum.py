from django.db import models

from core.models.base import BaseModel
from core.models.taxonomic_kingdom import TaxonomicKingdom


class TaxonomicPhylum(BaseModel):
    class Meta:
        app_label = 'core'
        default_permissions = ()
        db_table = 'taxonomic_phylums'

    kingdom = models.ForeignKey(TaxonomicKingdom, on_delete=models.CASCADE)
    name = models.CharField(max_length=45, unique=True)
