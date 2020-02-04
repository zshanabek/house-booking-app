from django.db import models
from account.models import User
from house.models import House
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from core.models import TrackableDate
import datetime

class Reservation(TrackableDate):
    DEFAULT = 0
    CANCELED = 1
    EXPIRED = 2
    STATUS_CHOICES = (
        (DEFAULT, 'Default'),
        (CANCELED, 'Canceled'),
        (EXPIRED, 'Expired')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    days = models.IntegerField()
    guests = models.IntegerField()
    status = models.IntegerField(default=0, choices=STATUS_CHOICES)
    message = models.CharField(max_length=1000)
    is_paid = models.BooleanField(default=False)
    accepted_house = models.BooleanField(default=None, null=True)

    @property
    def income(self):
        return self.house.price * self.days

    def save(self, *args, **kwargs):
        delta = self.check_out - self.check_in
        self.days = delta.days
        super(Reservation, self).save(*args, **kwargs)

    