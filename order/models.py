from django.db import models
from reservation.models import Reservation
from core.models import TrackableDate

class Order(TrackableDate):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return f"{self.amount}"
