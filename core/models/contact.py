from django.db import models

from core.models.base import BaseModel
from core.models.user import User


class Contact(BaseModel):
    class Meta:
        app_label = 'core'
        default_permissions = ()
        db_table = 'contacts'

    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=45)
    surname = models.CharField(max_length=45)
    organization = models.CharField(max_length=100, null=True)
    email = models.EmailField()
    skype = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    address = models.TextField(null=True)

    @property
    def full_name(self) -> str:
        return f'{self.name} {self.surname}'

    @property
    def short_name(self) -> str:
        return self.name

    def __str__(self):
        return f"{self.full_name} ({self.email})"
