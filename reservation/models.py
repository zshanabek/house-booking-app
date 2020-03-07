from django.db import models
from account.models import User
from house.models import House
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from core.models import TrackableDate
from django.db.models import Q
import datetime


class ReservationManager(models.Manager):

    def check_reservation(self, **kwargs):
        check_in = kwargs.get("check_in")
        check_out = kwargs.get("check_out")
        house = kwargs.get("house")
        user = kwargs.get("user")
        reservs = self.filter(Q(check_in__lte=check_out) & Q(
            check_out__gte=check_in) & Q(house=house) & ((Q(status=3) | Q(status=1)) | (Q(user=user) & Q(status=0))))
        return reservs


class Reservation(TrackableDate):
    REQUEST = 0
    APPROVED = 1
    REJECTED = 2
    PAID = 3
    CANCELED = 4
    EXPIRED = 5
    STATUS_CHOICES = (
        (REQUEST, 'Request'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
        (PAID, 'Paid'),
        (CANCELED, 'Canceled'),
        (EXPIRED, 'Expired'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    house = models.ForeignKey(
        House, on_delete=models.CASCADE, related_name='reservations')
    check_in = models.DateField()
    check_out = models.DateField()
    days = models.IntegerField()
    guests = models.IntegerField()
    status = models.IntegerField(default=0, choices=STATUS_CHOICES)
    message = models.CharField(max_length=1000, null=True, blank=True)

    objects = ReservationManager()
    @property
    def income(self):
        return self.house.price * self.days

    def save(self, *args, **kwargs):
        delta = self.check_out - self.check_in
        self.days = delta.days
        super(Reservation, self).save(*args, **kwargs)

    def __str__(self):
        return f"id: {self.id}; House: {self.house.id}-{self.house.name}; User: {self.user.email}; House owner: {self.house.user.email}; check in: {self.check_in}; check out: {self.check_out};"
