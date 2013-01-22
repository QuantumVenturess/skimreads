from django.conf.urls import patterns, url

urlpatterns = patterns('oauth.views', 
    url(r'^facebook/$', 'facebook'),
    url(r'^facebook/authenticate/$', 'facebook_auth'),
)