from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
# Create your models here.

class User(AbstractBaseUser):

    username = models.CharField(max_length=24,unique=True)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'username'

    class Meta:
        db_table = "User"