from django.contrib.admin import ModelAdmin, site
from core.models import Message


class MessageAdmin(ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('id', 'body', 'user__email', 'recipient__email')
    list_display = ('id', 'user', 'recipient', 'created_at',
                    'updated_at', 'characters')
    list_display_links = ('id',)
    list_filter = ('user', 'recipient')
    date_hierarchy = 'created_at'


site.register(Message, MessageAdmin)
