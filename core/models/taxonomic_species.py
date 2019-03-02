from django.db import models

from core.models.base import BaseModel
from core.models.taxonomic_genus import TaxonomicGenus


class TaxonomicSpecies(BaseModel):
    class Meta:
        app_label = 'core'
        default_permissions = ()
        db_table = 'taxonomic_species'

    taxonomic_genus = models.ForeignKey(TaxonomicGenus, on_delete=models.CASCADE)
    name = models.CharField(max_length=45, unique=True)
