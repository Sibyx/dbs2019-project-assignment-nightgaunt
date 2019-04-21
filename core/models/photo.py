import pathlib

from django.db import models
from django.conf import settings

from core.models.base import BaseModel
from core.models.specimen import Specimen
from core.models.user import User


class Photo(BaseModel):
    class Meta:
        app_label = 'core'
        default_permissions = ()
        db_table = 'photos'

    def _upload_to_path(self, filename):
        # pathlib.Path(f"{settings.MEDIA_ROOT}/photos/{self.specimen.box.id}").mkdir(parents=True, exist_ok=True)
        return f"photos/{self.specimen.box.id}/{filename}"

    specimen = models.ForeignKey(Specimen, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True)
    mime = models.CharField(max_length=100)
    path = models.ImageField(upload_to=_upload_to_path)
    happened_at = models.DateTimeField(null=True)
    description = models.TextField(null=True)
