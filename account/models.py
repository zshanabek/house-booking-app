from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import MaxValueValidator, MinValueValidator
from .managers import UserManager
from phonenumber_field.modelfields import PhoneNumberField

GUEST = 0
HOST = 1
USER_TYPE_CHOICES = (
    (GUEST, 'Guest'),
    (HOST, 'Host'),
)


WOMAN = 0
MAN = 1
GENDER_CHOICES = (
    (WOMAN, 'Female'),
    (MAN, 'Male'),
)


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    phone = PhoneNumberField(unique=True)
    birth_day = models.DateField()
    gender = models.IntegerField(choices=GENDER_CHOICES)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    user_type = models.IntegerField(default=0, choices=USER_TYPE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    userpic = models.ImageField(
        upload_to='userpics', max_length=254, blank=True, null=True)
    is_phone_confirmed = models.BooleanField(default=False)
    objects = UserManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ('email', 'birth_day', 'gender',
                       'first_name', 'last_name')
    FIELDS_TO_UPDATE = ('birth_day', 'email', 'gender',
                        'first_name', 'last_name', 'user_type')

    def __str__(self):
        return f"{self.id}; {self.email}; {self.first_name} {self.last_name}"

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def to_json(self):
        return {'full_name': f'{self.first_name} {self.last_name}', 'id': self.id}


class OTP(models.Model):
    phone = PhoneNumberField(unique=True)
    code = models.CharField(max_length=4)
    attempts = models.IntegerField(default=3)
    ban_date = models.DateTimeField(default=None, null=True)

    def __str__(self):
        return f"{self.phone}"
