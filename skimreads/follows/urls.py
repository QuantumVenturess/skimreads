from django.conf.urls import patterns, url

urlpatterns = patterns('follows.views', 
    # Follow tags
    url(r'^tags/(?P<slug>[-\w]+)/$', 'follow_tag'),
)