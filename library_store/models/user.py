from django.contrib.auth import get_user_model
from django.db import models

from library_store.constants.enums import UserRoleEnum


User = get_user_model()


class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=UserRoleEnum.choices())
    is_active = models.BooleanField(default=True)
