from django.conf.urls import patterns, url

urlpatterns = patterns('tags.views', 
    # tag list
    url(r'^tag-list/$', 'tag_list'),
    # tag list new reading
    url(r'^tag-list-new-reading/$', 'tag_list_new_reading'),
    url(r'^(?P<slug>[-\w]+)/$', 'detail'),
    url(r'^(?P<slug>[-\w]+)/followers/$', 'followers'),
    url(r'^(?P<slug>[-\w]+)/new/$', 'new'),
    url(r'^(?P<slug>[-\w]+)/delete/$', 'delete'),
)