from django.db import models

from core.models.base import BaseModel
from core.models.user import User


class Box(BaseModel):
    class Meta:
        app_label = 'core'
        default_permissions = ()
        db_table = 'boxes'

    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True)

    def __str__(self):
        return self.title
