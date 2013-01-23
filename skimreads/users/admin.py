from django.contrib import admin
from django.contrib.admin.models import User
from users.models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('created', 'admin_image', 'admin_user', 'reputation', 
        'read_count', 'note_count', 'comment_count', 'reply_count', 
        'vote_count', 'tie_count', 'favorite_count', 'followers_count', 
        'following_count', 'topic_count', 'message_count', 'slug')
    search_fields = ('user',)

class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'email', 'first_name', 'last_name', 
        'is_staff', 'last_login', 'date_joined')
    list_display_links = ('username',)
    search_fields = ('username',)

admin.site.register(Profile, ProfileAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)