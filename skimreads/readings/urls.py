from django.conf.urls import patterns, url

urlpatterns = patterns('readings.views',
    # New reading
    url(r'^new/$', 'new'),
    url(r'^new/bookmarklet/$', 'new_bookmarklet'),
    # Scrape reading link
    url(r'^new/scrape/$', 'scrape'),
    # Detail
    url(r'^(?P<slug>[-\w]+)/$', 'detail'),
    # Detail show comment, note, or reply
    url(r'^(?P<slug>[-\w]+)/(?P<show>[\w]+)/(?P<pk>\d+)/$', 
        'detail_show'),
    # Permalink
    url(r'^(?P<slug>[-\w]+)/permalink/$', 'permalink'),
    # Reading link redirect
    url(r'^(?P<slug>[-\w]+)/link/$', 'link'),
    # Reading edit
    url(r'^(?P<slug>[-\w]+)/edit/$', 'edit'),
    # Reading delete
    url(r'^(?P<slug>[-\w]+)/delete/$', 'delete'),
)

urlpatterns += patterns('admins.views',
    # Admins detail reading
    url(r'^(?P<slug>[-\w]+)/admins/$', 'reading'),
    # vote all
    url(r'^(?P<slug>[-\w]+)/admins/vote-all/$', 'vote_all'),
)