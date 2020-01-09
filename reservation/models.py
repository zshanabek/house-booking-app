from django.db import models
from account.models import User
from house.models import House
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator


class Reservation(models.Model):
    DEFAULT = 0
    CANCELED = 1
    STATUS_CHOICES = (
        (DEFAULT, 'Default'),
        (CANCELED, 'Canceled'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.IntegerField()
    status = models.IntegerField(default=0, choices=STATUS_CHOICES)
    created_at = models.DateField(default=timezone.now)
    accepted_house = models.BooleanField(default=None, null=True)
