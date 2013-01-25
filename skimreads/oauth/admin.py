from django.contrib import admin
from oauth.models import Oauth

class OauthAdmin(admin.ModelAdmin):
    list_display = ('created', 'user', 'provider', 'facebook_id', 
        'access_token',)
    search_fields = ['user']

admin.site.register(Oauth, OauthAdmin)