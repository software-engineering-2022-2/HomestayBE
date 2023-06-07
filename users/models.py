from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    phone_number = models.CharField(max_length=20)
    street_name = models.CharField(max_length=100)
    street_number = models.CharField(max_length=10)
    district = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='users/avatars/', default='users/images/default-avatar.jpg')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['last_name', 'first_name']

    objects = UserManager()

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name
