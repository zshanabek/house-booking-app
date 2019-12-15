from django.db import models
from account.models import User
from house.models import House


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.IntegerField()
    status = models.IntegerField()
    created_at = models.DateField()
    accepted_house = models.BooleanField()
