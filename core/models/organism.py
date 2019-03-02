from django.db import models

from core.models.base import BaseModel
from core.models.taxonomic_species import TaxonomicSpecies
from core.models.taxonomic_subspecies import TaxonomicSubspecies


class Organism(BaseModel):
    class Meta:
        app_label = 'core'
        default_permissions = ()
        db_table = 'organisms'

    taxonomic_species = models.ForeignKey(TaxonomicSpecies, on_delete=models.CASCADE)
    taxonomic_subspecies = models.ForeignKey(TaxonomicSubspecies, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=150)
    author = models.CharField(max_length=100, null=True)
    year = models.PositiveSmallIntegerField(null=True)  # pozri sa ci neexituje typ, s ktorym by sa robilo lepsie

    def __str__(self):
        return self.name
