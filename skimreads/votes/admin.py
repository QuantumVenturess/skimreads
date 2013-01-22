from django.contrib import admin
from votes.models import Vote

class VoteAdmin(admin.ModelAdmin):
    list_display = ('created', 'admin_note', 'admin_user', 'value')

admin.site.register(Vote, VoteAdmin)