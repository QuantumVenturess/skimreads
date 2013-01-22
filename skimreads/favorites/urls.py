from django.conf.urls import patterns, url

urlpatterns = patterns('favorites.views', 
    url(r'^(?P<slug>[-\w]+)/fave/$', 'fave'),
)