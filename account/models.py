from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import MaxValueValidator, MinValueValidator
from .managers import UserManager


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    phone = models.CharField(max_length=255, unique=True)
    birth_day = models.DateField()
    gender = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(1)])
    user_type = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(1)])
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'birth_day', 'gender', 'user_type',
                       'first_name', 'last_name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


class OTP(models.Model):
    phone = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=4)
    attempts = models.IntegerField(default=3)
    ban_date = models.DateTimeField(default=None, null=True)

    def __str__(self):
        return self.phone
