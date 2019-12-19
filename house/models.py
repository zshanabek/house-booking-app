from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from account.models import User
from django.utils import timezone


class Accommodation(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Rule(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class HouseType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class NearBuilding(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class House(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    rooms = models.IntegerField()
    floor = models.IntegerField()
    address = models.CharField(max_length=255)
    longitude = models.FloatField()
    latitude = models.FloatField()
    price = models.IntegerField()
    status = models.IntegerField()
    rating = models.FloatField(default=0)
    guests = models.IntegerField()
    beds = models.IntegerField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='users')
    house_type = models.ForeignKey(
        HouseType, on_delete=models.CASCADE, related_name='house_types')
    rules = models.ManyToManyField(Rule)
    accommodations = models.ManyToManyField(Accommodation)
    near_buildings = models.ManyToManyField(NearBuilding)

    @property
    def photos(self):
        return self.photo_set.all()


class Room(models.Model):
    name = models.CharField(max_length=255)
    is_room = models.BooleanField()


class HouseRoom(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    description = models.TextField()
    count = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(99)])


def nameFile(instance, filename):
    return '/'.join(['images',  filename])


class Photo(models.Model):
    house = models.ForeignKey(
        House, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(
        upload_to=nameFile, max_length=254, blank=True, null=True)

    def __str__(self):
        return "{} | {}".format(self.house, self.image)


class Review(models.Model):
    body = models.CharField(max_length=1000)
    stars = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.CASCADE)


class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.CASCADE)


class FreeDateInterval(models.Model):
    date_start = models.DateField((""), auto_now=False, auto_now_add=False)
    date_end = models.DateField((""), auto_now=False, auto_now_add=False)
    house = models.ForeignKey(
        House, on_delete=models.CASCADE, related_name='house_free_dates')
