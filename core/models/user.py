from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from core.managers.user import UserManager
from core.models.base import BaseModel


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    class Meta:
        app_label = 'core'
        default_permissions = ()
        db_table = 'users'

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    objects = UserManager()
    objects_all = UserManager(alive_only=False)

    def get_full_name(self) -> str:
        return f'{self.name} {self.surname}'

    def get_short_name(self) -> str:
        return self.name

    def __str__(self):
        return self.email
