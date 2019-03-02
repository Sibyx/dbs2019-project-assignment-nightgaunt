from django.db import models

from core.models.base import BaseModel
from core.models.specimen import Specimen
from core.models.user import User


class Photo(BaseModel):
    class Meta:
        app_label = 'core'
        default_permissions = ()
        db_table = 'photos'

    specimen = models.ForeignKey(Specimen, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True)
    mime = models.CharField(max_length=100)
    path = models.ImageField(upload_to='photos')
    happened_at = models.DateTimeField(null=True)
    description = models.TextField(null=True)
