from django.contrib import admin
from tags.models import Tag, Tie

class TagAdmin(admin.ModelAdmin):
    list_display = ['created', 'name', 'admin_user']
    search_fields = ['name']

class TieAdmin(admin.ModelAdmin):
    list_display = ['created', 'admin_reading', 'admin_tag', 'admin_user']
    list_filter = ['tag']

admin.site.register(Tag, TagAdmin)
admin.site.register(Tie, TieAdmin)