from django.db import models
from account.models import User
from house.models import House
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from core.models import TrackableDate
import datetime


class ReservationManager(models.Manager):

    def check_reservation(self, **kwargs):
        check_in = kwargs.get("check_in")
        check_out = kwargs.get("check_out")
        house = kwargs.get("house")
        filter_params = dict(check_in__lte=check_out, check_out__gte=check_in)
        reservs = Reservation.objects.filter(
            **filter_params, house=house)
        return self.filter()


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
    message = models.CharField(max_length=1000, null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    accepted_house = models.BooleanField(default=None, null=True)

    objects = ReservationManager()
    @property
    def income(self):
        return self.house.price * self.days

    def save(self, *args, **kwargs):
        delta = self.check_out - self.check_in
        self.days = delta.days
        super(Reservation, self).save(*args, **kwargs)

    def __str__(self):
        return f"House: {self.house.name}; User: {self.user.email}; Owner: {self.house.user.email}; check in: {self.check_in}; check out: {self.check_out}; accepted: {self.accepted_house}; paid: {self.is_paid}"
