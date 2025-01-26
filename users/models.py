from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="Phone_number")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True, verbose_name="Avatar")
    country = models.CharField(max_length=50, blank=True, null=True, verbose_name="Country")

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["email",]
        permissions = [
            ("can_block_user", "Can block user")
        ]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email