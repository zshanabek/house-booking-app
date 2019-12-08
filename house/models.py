from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from account.models import User


class HouseType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class House(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='users')
    rooms = models.IntegerField()
    floor = models.IntegerField()
    address = models.CharField(max_length=255)
    longitude = models.FloatField()
    latitude = models.FloatField()
    city = models.CharField(max_length=255)
    house_type = models.ForeignKey(
        HouseType, on_delete=models.CASCADE, related_name='house_types')
    price = models.IntegerField()
    status = models.IntegerField()

    @property
    def photos(self):
        return self.photo_set.all()

    @property
    def houseaccoms(self):
        return self.accommodationhouse.all()


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


class Accommodation(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class AccommodationHouse(models.Model):
    house = models.ForeignKey(
        House, on_delete=models.CASCADE, related_name='houseaccoms')
    accom = models.ForeignKey(
        Accommodation, on_delete=models.CASCADE, related_name='accommodations')


class Review(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    house = models.ForeignKey(
        House, on_delete=models.CASCADE)
    body = models.CharField(max_length=1000)


class Favourite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    house = models.ForeignKey(
        House, on_delete=models.CASCADE)
