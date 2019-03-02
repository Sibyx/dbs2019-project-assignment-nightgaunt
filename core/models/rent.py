from django.db import models

from core.models.base import BaseModel
from core.models.boxes import Box
from core.models.contact import Contact
from core.models.specimen import Specimen
from core.models.user import User


class Rent(BaseModel):
    class Meta:
        app_label = 'core'
        default_permissions = ()
        db_table = 'rents'

    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    date_from = models.DateField()
    date_to = models.DateField()
    description = models.TextField(null=True)
    boxes = models.ManyToManyField(Box)
    specimens = models.ManyToManyField(Specimen)
