from django.contrib import admin
from notifications.models import Notification

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('created', 'comment', 'follow', 'note', 'reply', 'tie', 
        'vote', 'user', 'viewed')

admin.site.register(Notification, NotificationAdmin)