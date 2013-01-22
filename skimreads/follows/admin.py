from django.contrib import admin
from follows.models import Follow, TagFollow

class FollowAdmin(admin.ModelAdmin):
    list_display = ['created', 'admin_followed', 'admin_follower']

class TagFollowAdmin(admin.ModelAdmin):
    list_display = ['created', 'admin_tag', 'admin_user']
    list_filter = ['tag']

admin.site.register(Follow, FollowAdmin)
admin.site.register(TagFollow, TagFollowAdmin)