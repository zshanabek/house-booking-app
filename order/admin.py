from django.contrib.admin import ModelAdmin, site
from .models import Order


class OrderAdmin(ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'


site.register(Order, OrderAdmin)
