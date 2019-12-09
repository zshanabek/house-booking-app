from django.contrib import admin
from house import models as house_models


admin.site.register(house_models.House)
admin.site.register(house_models.Room)
admin.site.register(house_models.HouseRoom)
admin.site.register(house_models.Photo)
admin.site.register(house_models.Accommodation)
admin.site.register(house_models.AccommodationHouse)
admin.site.register(house_models.HouseType)
admin.site.register(house_models.NearBuilding)
admin.site.register(house_models.NearBuildingHouse)
admin.site.register(house_models.City)
admin.site.register(house_models.Rule)
