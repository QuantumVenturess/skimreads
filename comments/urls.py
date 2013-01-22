from django.conf.urls import patterns, url

urlpatterns = patterns('comments.views',
    url(r'^new/(?P<pk>\d+)/$', 'new'),
    url(r'^(?P<pk>\d+)/delete/$', 'delete'),
)