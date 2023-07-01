from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager,BaseUserManager

# 커스텀 유저 모델(Custom User Model) 생성

class UserManager(BaseUserManager):
    def create_user(self,username,nickname,email,password=None):
        if not username:
            raise ValueError("The Username field must be set.")
        if not email:
            raise ValueError("The Email field must be set.")
        if not nickname:
            raise ValueError("The nickname field must be set.")
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,nickname=nickname)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,username,nickname,email,password=None):
        user = self.create_user(
            username,
            nickname,
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user



class User(AbstractBaseUser):

    username = models.CharField(max_length=24)
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=20,unique=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','nickname']

    objects = UserManager()

    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self,app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin
    
    class Meta:
        db_table = "User"