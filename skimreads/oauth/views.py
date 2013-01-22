from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from oauth.facebook import *
from oauth.models import Oauth

import json
import random
import re
import urllib2

def facebook(request):
    return HttpResponseRedirect(facebook_url())

def facebook_auth(request):
    """Facebook login/sign up."""
    code = request.GET.get('code')
    error = request.GET.get('error')
    # If the user cancels app permission
    if error:
        messages.error(request, 'Unable to authenticate, please try again')
        # if user is not logged in
        if request.user.is_anonymous():
            return HttpResponseRedirect(reverse('users.views.new'))
        # if user is logged in
        else:
            return HttpResponseRedirect(reverse('user.views.edit', 
                args=[request.user.profile.slug]))
    # If user grants app permissions
    elif code:
        url = [
            'https://graph.facebook.com/oauth/access_token?',
            'client_id=%s&' % facebook_app_id(),
            'redirect_uri=%s&' % facebook_redirect_uri(),
            'client_secret=%s&' % facebook_app_secret(),
            'code=%s' % code
        ]
        exchange = ''.join(url)
        response = urllib2.urlopen(exchange).read()
        access_token = response.split('=')[1].split('&')[0]
        graph = 'https://graph.facebook.com/me?access_token=%s' % access_token
        api_call = urllib2.urlopen(graph).read()
        data = json.loads(api_call)
        email = data['email']
        facebook_id = data['id']
        first_name = data['first_name']
        last_name = data['last_name']
        username = ' '.join([first_name, last_name])
        # If user is not logged in
        if request.user.is_anonymous():
            # Check to see if oauth with facebook id exists
            try:
                oauth = Oauth.objects.get(facebook_id=facebook_id)
                # Update access token
                oauth.access_token = access_token
                oauth.save()
                user = oauth.user
            # If oauth does not exist with that facebook id, create one
            except ObjectDoesNotExist:
                # Check to see if user with email exists
                try:
                    user = User.objects.get(email=email)
                # If user with email does not exist
                except ObjectDoesNotExist:
                    # Random password
                    letters = list(access_token)
                    random.shuffle(letters)
                    password = ''.join(letters[0:20])
                    user = User.objects.create(email=email, 
                        first_name=first_name, last_name=last_name, 
                        password=password, username=username)
                # Create oauth for user
                user.oauth_set.create(access_token=access_token, 
                    facebook_id=facebook_id, provider='facebook')
            # Login user
            auth.login(request, auth.authenticate(email=user.email))
            # friendly forwarding
            if request.session.get('next'):
                next = request.session['next']
                del request.session['next']
                return HttpResponseRedirect(next)
        # If user is logged in
        else:
            # Check to see if oauth with facebook id exists
            try:
                oauth = request.user.oauth_set.get(facebook_id=facebook_id)
                # if so update access token
                oauth.access_token = access_token
                oauth.save()
            # If oauth does not exist with that facebook id, create one
            except ObjectDoesNotExist:
                request.user.oauth_set.create(access_token=access_token, 
                    facebook_id=facebook_id, provider='facebook')
    # If the user came straight to this URL
    if request.user.is_anonymous():
        return HttpResponseRedirect(reverse('users.views.new'))
    return HttpResponseRedirect(reverse('root_path'))