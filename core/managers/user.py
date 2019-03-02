from django.contrib.auth.base_user import BaseUserManager

from core.managers.base import BaseManager


class UserManager(BaseUserManager, BaseManager):
    pass
