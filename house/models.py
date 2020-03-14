from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from account.models import User
from django.utils import timezone
from datetime import datetime
from core.models import TrackableDate


class Accommodation(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Удобство"
        verbose_name_plural = "Удобства"


class Rule(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Правило"
        verbose_name_plural = "Правила"


class HouseType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Вид жилья"
        verbose_name_plural = "Виды жилья"


class NearBuilding(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Ближайшая организация"
        verbose_name_plural = "Ближайшие организации"


class House(TrackableDate):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    address = models.CharField(max_length=255)
    longitude = models.FloatField()
    latitude = models.FloatField()
    rating = models.FloatField(default=0.0)
    status = models.BooleanField(default=True)
    price = models.PositiveIntegerField()
    beds = models.PositiveIntegerField(default=0)
    guests = models.PositiveIntegerField()
    rooms = models.PositiveIntegerField()
    floor = models.IntegerField()
    verified = models.BooleanField(default=False)
    discount7days = models.PositiveIntegerField(
        default=0, validators=[MaxValueValidator(100)])
    discount30days = models.PositiveIntegerField(
        default=0, validators=[MaxValueValidator(100)])
    city = models.ForeignKey('cities_light.City', on_delete=models.CASCADE)
    region = models.ForeignKey(
        'cities_light.Region', on_delete=models.CASCADE, null=True)
    country = models.ForeignKey(
        'cities_light.Country', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    house_type = models.ForeignKey(HouseType, on_delete=models.CASCADE)
    rules = models.ManyToManyField(Rule)
    accommodations = models.ManyToManyField(Accommodation)
    near_buildings = models.ManyToManyField(NearBuilding)

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

    def __str__(self):
        return "{} {}".format(self.id, self.name)

    def to_json(self):
        return {'id': self.id, 'name': self.name, 'created_at': str(self.created_at), 'updated_at': str(self.updated_at)}

    @property
    def available(self):
        now = datetime.now()
        reservations = self.reservation_set.filter(
            check_in__gte=now, check_in__lte=now)
        return reservations.exists()


def nameFile(instance, filename):
    return '/'.join(['images', filename])


class Photo(models.Model):
    house = models.ForeignKey(
        House, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(
        upload_to=nameFile, max_length=254, blank=True, null=True)

    def __str__(self):
        return "{} | {}".format(self.house, self.image)

    class Meta:
        verbose_name = "Фотография"
        verbose_name_plural = "Фотографии объявлений"


class Review(TrackableDate):
    body = models.CharField(max_length=1000)
    stars = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    house = models.ForeignKey(
        House, on_delete=models.CASCADE, related_name='reviews')

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return '%s' % (self.body)


class Favourite(TrackableDate):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Избранный"
        verbose_name_plural = "Избранные"


class BlockedDateInterval(models.Model):
    check_in = models.DateField()
    check_out = models.DateField()
    house = models.ForeignKey(
        House, on_delete=models.CASCADE, related_name='blocked_dates')

    def __str__(self):
        return "{} - {}".format(self.check_in.strftime("%Y/%m/%d"), self.check_out.strftime("%Y/%m/%d"))

    class Meta:
        verbose_name = "Несвободная дата"
        verbose_name_plural = "Несвободные даты"
