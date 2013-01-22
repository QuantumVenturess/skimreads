from django.conf.urls import patterns, url

urlpatterns = patterns('votes.views', 
    url(r'(?P<pk>\d+)/vote/$', 'new'),
)