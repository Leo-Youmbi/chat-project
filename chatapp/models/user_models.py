from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


# Create your models here.


class ChatUsersManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        try:
            user = ChatUsers.objects.get(username=username, **extra_fields)
        except ChatUsers.DoesNotExist:
            user = self.model(username=username, **extra_fields)
            user.set_password(password)
            user.save()
        return user

    def get_query(self, excluded_user_id):
        return super().get_queryset().exclude(
            id=excluded_user_id
        )


class ChatUsers(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=150, default=username)
    password = models.CharField(max_length=128)
    email = models.EmailField(max_length=150)
    objects = ChatUsersManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username
