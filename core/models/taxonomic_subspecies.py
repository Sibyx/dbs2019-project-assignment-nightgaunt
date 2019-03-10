from django.db import models

from core.models.base import BaseModel
from core.models.taxonomic_species import TaxonomicSpecies


class TaxonomicSubspecies(BaseModel):
    class Meta:
        app_label = 'core'
        default_permissions = ()
        db_table = 'taxonomic_subspecies'
        unique_together = ("taxonomic_species", "name")

    taxonomic_species = models.ForeignKey(TaxonomicSpecies, on_delete=models.CASCADE)
    name = models.CharField(max_length=45)

    def __str__(self):
        return self.name
