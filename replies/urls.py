from django.conf.urls import patterns, url

urlpatterns = patterns('replies.views', 
    url(r'^(?P<pk>\d+)/new/$', 'new'),
    url(r'^(?P<pk>\d+)/delete/$', 'delete'),
)