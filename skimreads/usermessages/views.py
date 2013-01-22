from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import Context, loader, RequestContext
from skimreads.utils import add_csrf
from usermessages.forms import NewMessageForm, ReplyMessageForm
from usermessages.models import UserMessage
from users.models import Profile

import json
import re

@login_required
def new(request):
    """Create new message."""
    if request.method == 'POST':
        form = NewMessageForm(request.POST)
        content = request.POST.get('content')
        name = request.POST.get('to')
        # if a name and content was submitted
        if content and name:
            pattern = re.compile(r'^[-A-Za-z]{2,} [-A-Za-z]{2,}$')
            # if submitted recipient name matches correct format
            if re.search(pattern, name):
                first_name, last_name = name.split()
                username = '%s %s' % (first_name.lower().capitalize(), 
                    last_name.lower().capitalize())
                # check to see if user with that name exists
                try:
                    user = User.objects.get(username=username)
                    # create a message where current user is the snder
                    # and user is the recipient
                    message = form.save(commit=False)
                    message.recipient = user
                    message.sender = request.user
                    message.save()
                    # if replying to a message via detail page
                    if request.POST.get('reply') == '1':
                        d = {
                            'form': ReplyMessageForm(),
                            'message': message,
                            'profile_user': message.recipient,
                        }
                        message = loader.get_template(
                            'usermessages/message.html')
                        reply_message_form = loader.get_template(
                            'usermessages/reply_message_form.html')
                        context = RequestContext(request, add_csrf(request, d))
                        data = {
                            'message': message.render(context),
                            'reply_message_form': reply_message_form.render(
                                context),
                        }
                        return HttpResponse(json.dumps(data), 
                            mimetype='application/json')
                    # if creating a new message
                    else:
                        return HttpResponseRedirect(
                            reverse('usermessages.views.detail', 
                                args=[message.recipient.profile.slug]))
                # if user does not exist with that name
                except ObjectDoesNotExist:
                    messages.error(request, 'No user found')
            else:
                messages.error(request, 'What kind of name is that?')
        else:
            messages.error(request, 'Leave nothing blank')
    else:
        form = NewMessageForm()
    d = {
        'form': form,
        'title': 'New Message',
    }
    return render_to_response('usermessages/new.html', add_csrf(request, d), 
        context_instance=RequestContext(request))

@login_required
def user_list(request):
    """Return a list of users to send a message to."""
    query = request.GET.get('q', '')
    # if query has 2 or more characters
    if len(query) >= 2:
        names = query.split(' ')
        # if query has a first and last name
        if len(names) == 2:
            first, last = names
            # if first and last name have 2 or more letters
            if len(first) >= 2 and len(last) >= 2:
                results = User.objects.filter(Q(
                    first_name__icontains=first, 
                    last_name__icontains=last) | Q(first_name__icontains=last, 
                    last_name__icontains=first)).exclude(pk=request.user.pk)
            # if first name has 2 or more letters
            elif len(first) >= 2:
                results = User.objects.filter(Q(
                    first_name__icontains=first) | Q(
                    last_name__icontains=first)).exclude(pk=request.user.pk)
            # if last name has 2 or more letters
            elif len(last) >= 2:
                results = User.objects.filter(Q(
                    first_name__icontains=last) | Q(
                    last_name__icontains=last)).exclude(pk=request.user.pk)
            # if first and last name have less than 2 letters
            else:
                results = []
        # if query only has one name
        else:
            results = User.objects.filter(Q(
                username__icontains=query)).exclude(pk=request.user.pk)
    # if query has less than 2 letters
    else:
        results = []
    d = {
        'results': results,
    }
    t = loader.get_template('usermessages/results.html')
    context = Context(d)
    data = {
        'results': t.render(context),
    }
    return HttpResponse(json.dumps(data), mimetype='application/json')

@login_required
def list(request):
    """Show all messages for current user."""
    usermessages = request.user.profile.recent_messages()
    d = {
        'form': NewMessageForm(),
        'usermessages': usermessages,
        'title': 'Messages',
    }
    return render_to_response('usermessages/list.html', d, 
        context_instance=RequestContext(request))

@login_required
def detail(request, slug):
    """Show messages between current user and user."""
    profile = get_object_or_404(Profile, slug=slug)
    msgs = UserMessage.objects.filter(
        Q(recipient=profile.user, sender=request.user) | Q(
            recipient=request.user, sender=profile.user)).order_by('created')
    received_messages = request.user.received_messages.filter(sender=profile.user)
    # mark all messages as viewed
    if received_messages:
        for msg in received_messages:
            msg.viewed = True
            msg.save()
    # group messages by date
    if msgs:
        dates = sorted(set([msg.date() for msg in msgs]), 
            key=lambda m: datetime.strptime(m, '%b %d, %y'))
        days = []
        for day in dates:
            usermsgs = [m for m in msgs if m.date() == day]
            days.append((day, usermsgs))
        d = {
            'days': days,
            'form': ReplyMessageForm(),
            'profile_user': profile.user,
            'title': '%s Messages' % profile.user.username,
        }
        return render_to_response('usermessages/detail.html', 
            add_csrf(request, d), context_instance=RequestContext(request))
    else:
        messages.warning(request, 'You have no messages from that user')
        return HttpResponseRedirect(reverse('usermessages.views.list'))