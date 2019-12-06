from django.db import models
from reservation.models import Reservation

# Create your models here.

class Payment(models.Model):
    created_at = models.DateField()
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    amount = models.IntegerField()
