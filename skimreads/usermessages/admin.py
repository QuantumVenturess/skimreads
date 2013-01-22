from django.contrib import admin
from usermessages.models import UserMessage

class UserMessageAdmin(admin.ModelAdmin):
    list_display = ('created', 'content', 'admin_recipient', 'admin_sender', 
        'viewed')
    search_fields = ('content',)

admin.site.register(UserMessage, UserMessageAdmin)