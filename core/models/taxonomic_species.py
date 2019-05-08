from django.db import models

from core.models.base import BaseModel
from core.models.taxonomic_genus import TaxonomicGenus


class TaxonomicSpecies(BaseModel):
    class Meta:
        app_label = 'core'
        default_permissions = ()
        db_table = 'taxonomic_species'
        unique_together = ("taxonomic_genus", "name")

    taxonomic_genus = models.ForeignKey(TaxonomicGenus, on_delete=models.CASCADE)
    name = models.CharField(max_length=45, db_index=True)

    def __str__(self):
        return self.name
