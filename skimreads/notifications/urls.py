from django.conf.urls import patterns, url

urlpatterns = patterns('notifications.views', 
    url(r'^(?P<pk>\d+)/forward/$', 'forward'),
    url(r'^$', 'list'),
)