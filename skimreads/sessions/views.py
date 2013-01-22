from django.contrib import auth, messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from sessions.decorators import already_logged_in
from skimreads.utils import add_csrf

@already_logged_in()
def new(request):
    """Login page."""
    if request.method == 'POST':
        email = request.POST.get('email', '').lower()
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            # login url from login required
            if request.POST.get('next'):
                return HttpResponseRedirect(request.POST['next'])
            # friendly forwarding
            elif request.session.get('next'):
                next = request.session['next']
                del request.session['next']
                return HttpResponseRedirect(next)
            else:
                return HttpResponseRedirect(reverse('root_path'))
        else:
            messages.error(request, 
                'The email or password you have entered is invalid')
    next = request.GET.get('next', '')
    d = {
            'title': 'Login',
            'email': request.POST.get('email', ''),
            'next': next,
    }
    return render_to_response('sessions/new.html', add_csrf(request, d), 
        context_instance=RequestContext(request))

@login_required
def destroy(request):
    """Logout."""
    auth.logout(request)
    return HttpResponseRedirect(reverse('sessions.views.new'))