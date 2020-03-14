from house import models as house_models
from django.contrib.admin import ModelAdmin, site


class HouseAdmin(ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'


class FavouriteAdmin(ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'


site.register(house_models.House, HouseAdmin)
site.register(house_models.Photo)
site.register(house_models.Accommodation)
site.register(house_models.HouseType)
site.register(house_models.NearBuilding)
site.register(house_models.Rule)
site.register(house_models.Favourite, FavouriteAdmin)
site.register(house_models.BlockedDateInterval)
