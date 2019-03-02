import uuid
from django.db import models
from django.utils import timezone
from core.managers.base import BaseManager


class BaseModel(models.Model):
	class Meta:
		abstract = True

	id = models.UUIDField(primary_key=True, default=uuid.uuid4)
	deleted_at = models.DateTimeField(blank=True, null=True)
	updated_at = models.DateTimeField(auto_now=True)
	created_at = models.DateTimeField(auto_now_add=True)

	objects = BaseManager()
	objects_all = BaseManager(alive_only=False)

	def delete(self, using=None, keep_parents=False):
		self.deleted_at = timezone.now()
		self.save()

	def hard_delete(self):
		super(BaseModel, self).delete()
