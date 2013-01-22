from django.contrib import admin
from replies.models import Reply

class ReplyAdmin(admin.ModelAdmin):
    list_display = ('created', 'content', 'admin_comment', 'admin_user')
    list_filter = ('user',)
    search_fields = ('content',)

admin.site.register(Reply, ReplyAdmin)