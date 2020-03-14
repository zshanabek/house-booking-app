from .models import Reservation
from django.contrib.admin import ModelAdmin, site


class ReservationAdmin(ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'


site.register(Reservation, ReservationAdmin)
