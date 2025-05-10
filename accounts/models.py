from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, name=None, grade="general", **extra_fields):
        if not email:
            raise ValueError('이메일은 필수입니다.')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, grade=grade, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, name=None, grade="general", **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, name, grade, **extra_fields)


GRADE_CHOICES = [
        ("general", '일반'),
        ("vip", '우수'),
    ]

class User (AbstractUser):
    name = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    grade = models.CharField(
        max_length=10,
        choices=GRADE_CHOICES,
        default="general",
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'grade'] 

    objects = UserManager()


