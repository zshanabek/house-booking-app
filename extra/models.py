from django.db import models
from account.models import User
from core.models import TrackableDate


class Feedback(TrackableDate):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.user.id}; {self.user.full_name()}; {self.message}"
