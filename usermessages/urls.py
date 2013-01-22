from django.conf.urls import patterns, url

urlpatterns = patterns('usermessages.views', 
    # new
    url(r'^new/$', 'new'),
    # user list
    url(r'^user-list/$', 'user_list'),
    # list
    url(r'^$', 'list'),
    # detail
    url(r'^(?P<slug>[-\w]+)/$', 'detail'),
)