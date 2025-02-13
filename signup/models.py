from typing import Any, Collection
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.utils import timezone
# Create your models here.
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError("Email error")
        email = self.normalize_email(email)

        user = self.model(email=email, **kwargs)
        #self.modelはUserクラスを呼び出して、インスタンスを作成してる
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password, **kwargs):
        kwargs.setdefault("is_staff", False)
        kwargs.setdefault("is_superuser", False)
        return self._create_user(email, password, **kwargs)
    
    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        if kwargs.get("is_staff") is not True:
            raise ValueError("Superuser must be is_staff=True")
        
        if kwargs.get("is_superuser") is not True:
            raise ValueError("Superuser must be is_superuser=True")
        return self._create_user(email, password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=20,unique=True,null=True, blank=True)
    create_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()
    # 上記コードを書くとBaseUserManager内で下記のような処理が裏で行われる。
    #user_model = User

    # マネージャーのインスタンスを作成
    #manager = UserManager()
    #manager.model = user_model  # ここで model 属性が設定される

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def validate_email(self):
        return len(self.email) <= 255
    
