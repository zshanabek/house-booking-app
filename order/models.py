from django.db import models
from reservation.models import Reservation
from core.models import TrackableDate


class Order(TrackableDate):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    amount = models.IntegerField()
    is_paid = models.BooleanField(default=False)
    payment_id = models.PositiveIntegerField(unique=True, null=True)

    def __str__(self):
        return f"id: {self.id}; amount: {self.amount}; is_paid: {self.is_paid}; payment_id: {self.payment_id}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
