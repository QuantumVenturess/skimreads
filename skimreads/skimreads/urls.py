from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Test page
    url(r'^test/$', 'admins.views.test'),
    # Admin site
    url(r'^admin/', include(admin.site.urls)),
    # Admins interface
    url(r'^admins/', include('admins.urls')),
    # Comments
    url(r'^comments/', include('comments.urls')),
    # Favorites
    url(r'^favorites/', include('favorites.urls')),
    # Follows
    url(r'^follows/', include('follows.urls')),
    # Media files
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', 
        { 'document_root': settings.MEDIA_ROOT }),
    # Notes
    url(r'^notes/', include('notes.urls')),
    # Notifications
    url(r'^notifications/', include('notifications.urls')),
    # OAuth
    url(r'^oauth/', include('oauth.urls')),
    # Pages
    url(r'^about/$', 'pages.views.about'),
    # Readings
    url(r'^$', 'readings.views.feed', name='root_path'),
    url(r'^discover/$', 'readings.views.discover'),
    url(r'^readings/', include('readings.urls')),
    # Replies
    url(r'^replies/', include('replies.urls')),
    # Search
    url(r'^search/', include('search.urls')),
    # Sessions
    url(r'^login/$', 'sessions.views.new'),
    url(r'^logout/$', 'sessions.views.destroy'),
    # Tags
    url(r'^tags/', include('tags.urls')),
    # User messages
    url(r'^messages/', include('usermessages.urls')),
    # Users
    url(r'^join/$', 'users.views.new'),
    # Votes
    url(r'votes/', include('votes.urls')),

    # URLS with slugs
    # Follows
    url(r'^(?P<slug>[-\w]+)/follow/$', 'follows.views.follow'),
    url(r'^(?P<slug>[-\w]+)/(?P<action>followers|following|topics)/$', 
        'follows.views.show_follows'),
    # Readings
    url(r'^(?P<slug>[-\w]+)/$', 'readings.views.list_user'),
    # Users
    url(r'^(?P<slug>[-\w]+)/edit/$', 'users.views.edit'),
    url(r'^(?P<slug>[-\w]+)/', include('users.urls')),
)

if not settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', { 
            'document_root': settings.STATIC_ROOT })
    )