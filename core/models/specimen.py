from enum import Enum

from django.db import models
from django.utils.translation import gettext as _

from core.models.base import BaseModel
from core.models.boxes import Box
from core.models.organism import Organism
from core.models.user import User


class GenderChoice(Enum):
    MALE = _("Male")
    FEMALE = _("Female")


class Specimen(BaseModel):
    class Meta:
        app_label = 'core'
        default_permissions = ()
        db_table = 'specimens'

    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    box = models.ForeignKey(Box, on_delete=models.CASCADE)
    organism = models.ForeignKey(Organism, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=[(tag, tag.value) for tag in GenderChoice], null=True)
    form = models.CharField(max_length=50)
    notes = models.TextField(null=True)
    dna = models.TextField(null=True)

    def __str__(self):
        return self.nickname if self.nickname else str(self.organism)
