from django.db import models

from core.models.base import BaseModel
from core.models.taxonomic_class import TaxonomicClass


class TaxonomicOrder(BaseModel):
    class Meta:
        app_label = 'core'
        default_permissions = ()
        db_table = 'taxonomic_orders'

    taxonomic_class = models.ForeignKey(TaxonomicClass, on_delete=models.CASCADE)
    name = models.CharField(max_length=45, unique=True)
