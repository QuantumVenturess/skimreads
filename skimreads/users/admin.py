from django.contrib import admin
from users.models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('created', 'admin_image', 'admin_user', 'reputation', 
        'read_count', 'note_count', 'comment_count', 'reply_count', 
        'vote_count', 'tie_count', 'favorite_count', 'followers_count', 
        'following_count', 'topic_count', 'message_count', 'slug')
    search_fields = ('user',)

admin.site.register(Profile, ProfileAdmin)