from django.conf.urls import patterns, url

urlpatterns = patterns('users.views', 
    url(r'^(?P<category>comments|favorites|notes|tags|votes)/$', 'category'),
)