from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from facepy import GraphAPI
import random

def facebook_app_id():
    return settings.FACEBOOK_APP_ID

def facebook_app_secret():
    return settings.FACEBOOK_APP_SECRET

def facebook_redirect_uri():
    return settings.FACEBOOK_REDIRECT_URI

def facebook_scope():
    return settings.FACEBOOK_SCOPE

def facebook_url():
    response_type = 'token'
    state = ''.join([str(random.randrange(0, 10)) for i in range(0, 10)])
    url = [
        'https://www.facebook.com/dialog/oauth?',
        'client_id=%s&' % facebook_app_id(),
        'redirect_uri=%s&' % facebook_redirect_uri(),
        'scope=%s&' % facebook_scope(),
        'state=%s' % state,
    ]
    return ''.join(url)

def facebook_graph_add_reading(user, reading):
    if not settings.DEV:
        try:
            oauth = user.oauth_set.get(provider='facebook')
            graph_data = (
                'http://skimreads.com/readings/%s/permalink/' % reading.slug)
            graph = GraphAPI(oauth.access_token)
            graph.post(
                path = 'me/skimreads:add',
                reading = graph_data
            )
        except ObjectDoesNotExist:
            pass