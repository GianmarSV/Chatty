from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import UserManager


class ChatUser(AbstractBaseUser, PermissionsMixin):
    username    = models.CharField(max_length=50, unique=True)
    email       = models.EmailField(unique=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active   = models.BooleanField(default=True)
    is_staff    = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
