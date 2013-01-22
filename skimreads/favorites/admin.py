from django.contrib import admin
from favorites.models import Favorite

class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['created', 'admin_reading', 'admin_user']
    list_filter = ['user']

admin.site.register(Favorite, FavoriteAdmin)