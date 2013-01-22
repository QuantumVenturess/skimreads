from django.conf import settings
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