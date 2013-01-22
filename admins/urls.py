from django.conf.urls import patterns, url

urlpatterns = patterns('admins.views', 
    # reading detail
    url(r'^readings/new/$', 'new_reading'),
    # note detail
    url(r'^notes/(?P<pk>\d+)/$', 'note'),
    # comment detail
    url(r'^comments/(?P<pk>\d+)/$', 'comment'),
)