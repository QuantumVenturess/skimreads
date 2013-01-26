from django.conf.urls import patterns, url

urlpatterns = patterns('votes.views', 
    # vote for note
    url(r'(?P<pk>\d+)/note/vote/$', 'new'),
    # vote for reading
    url(r'(?P<pk>\d+)/reading/vote/$', 'new_reading'),
)