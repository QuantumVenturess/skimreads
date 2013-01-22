from django.conf.urls import patterns, url

urlpatterns = patterns('tags.views', 
    # tag list
    url(r'^tag-list/$', 'tag_list'),
    url(r'^(?P<slug>[-\w]+)/$', 'detail'),
    url(r'^(?P<slug>[-\w]+)/followers/$', 'followers'),
    url(r'^(?P<slug>[-\w]+)/new/$', 'new'),
    url(r'^(?P<slug>[-\w]+)/delete/$', 'delete'),
)