from enum import Enum

from django.db import models
from django.urls import reverse
from django.utils import formats

from core.models.base import BaseModel
from core.models.boxes import Box
from core.models.organism import Organism
from core.models.user import User


class GenderChoice(Enum):
    MALE = "Male"
    FEMALE = "Female"


class Specimen(BaseModel):
    class Meta:
        app_label = 'core'
        default_permissions = ()
        db_table = 'specimens'

    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    box = models.ForeignKey(Box, on_delete=models.CASCADE)
    organism = models.ForeignKey(Organism, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=[(tag.value, tag.value) for tag in GenderChoice], null=True)
    form = models.CharField(max_length=50)
    happened_at = models.DateField(null=True)
    notes = models.TextField(null=True)
    dna = models.TextField(null=True)

    def __str__(self):
        return self.organism.name

    @property
    def summary(self) -> dict:
        return {
            'id': self.id,
            'creator': str(self.creator),
            'organism__name': self.organism.name,
            'box__title': self.box.title,
            'gender': self.gender,
            'form': self.form,
            'happened_at': formats.date_format(self.happened_at),
            'notes': self.notes,
            'dna': self.dna,
            "url": reverse('specimens-detail', None, [self.id])
        }
