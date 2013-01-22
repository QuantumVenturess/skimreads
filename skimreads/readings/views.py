from bs4 import BeautifulSoup
from collections import defaultdict
from comments.forms import CommentForm
from comments.models import Comment
from datetime import timedelta
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import Context, loader, RequestContext, Template
from follows.utils import follow_user, followed_ids
from readings.forms import (EditReadingForm, NoteForm, ReadingForm, 
    RequiredFormSet)
from readings.models import Note, Reading
from readings.utils import crop_image, delete_reading_image
from replies.forms import ReplyForm
from replies.models import Reply
from skimreads.utils import add_csrf, page
from tags.models import Tie
from users.forms import SignUpForm
from users.models import Profile
from users.utils import add_rep, del_rep
from votes.models import Vote

import datetime
import json
import os
import re
import urllib2

# Readings

def feed(request):
    """Home page, show all readings from users."""
    # delete any friendly forwarding saved urls
    if request.session.get('next'):
        del request.session['next']
    # if user is logged out
    if request.user.is_anonymous():
        # show all readings in random order
        day = datetime.date.today() - timedelta(days=28)
        readings = Reading.objects.all().filter(
            created__gte=day).order_by('?')
    # if user is logged in
    else:
        # show readings from the users feed
        readings = request.user.profile.read_feed()
        # if no readings exist for feed, redirect to discover page
        if not readings:
            return HttpResponseRedirect(reverse('readings.views.discover'))
    d = { 'title': 'Skimreads' }
    if request.user.is_anonymous():
        d['form'] = SignUpForm()
        d['objects'] = readings[0:10]
    else:
        d['objects'] = page(request, readings, 10)
    return render_to_response('readings/feed.html', d, 
        context_instance=RequestContext(request))

@login_required
def discover(request):
    """Show all reads."""
    readings = Reading.objects.all().order_by('-created')
    d = {
            'discover': True,
            'objects': page(request, readings, 10),
            'title': 'Discover',
    }
    return render_to_response('readings/feed.html', d, 
        context_instance=RequestContext(request))

@login_required
def discover_exclude(request):
    """Discover new reads page."""
    ids = followed_ids(request)
    ids.append(request.user.pk)
    readings = Reading.objects.all().exclude(user__pk__in=ids).order_by(
        '-created')
    d = {
            'objects': page(request, readings, 10),
            'title': 'Discover',
    }
    return render_to_response('readings/feed.html', d, 
        context_instance=RequestContext(request))


@login_required(login_url='/join')
def list_user(request, slug):
    """Readings for a single user."""
    profile = get_object_or_404(Profile, slug=slug)
    user = User.objects.get(pk=profile.user_id)
    readings = Reading.objects.filter(user=user).order_by('-created')
    d = {
            'current_pk': user.pk,
            'objects': page(request, readings, 10),
            'profile_user': user,
            'title': '%s Reads' % user.first_name,
    }
    return render_to_response('readings/feed.html', add_csrf(request, d), 
        context_instance=RequestContext(request))

@login_required(login_url='/login/')
def new(request):
    """Add new reading."""
    NoteFormset = formset_factory(NoteForm, extra=3, formset=RequiredFormSet)
    if request.method == 'POST':
        link = request.POST.get('link')
        form = ReadingForm(request.POST)
        formset = NoteFormset(request.POST)
        # if reading with link already exists, add notes to it
        try:
            reading = Reading.objects.get(link=link)
            if formset.is_valid():
                # create notes and add it to the existing reading
                for note_form in formset:
                    note = note_form.save(commit=False)
                    note.reading = reading
                    note.user = request.user
                    if note.content.strip():
                        note.save()
                        # create first vote for note
                        request.user.vote_set.create(note=note, value=1)
                messages.success(request, 
                    'This reading exists, your notes have been added ot it')
                return HttpResponseRedirect(reverse('readings.views.detail', 
                    args=[reading.slug]))
        # if reading with link does not exist, create the reading
        except ObjectDoesNotExist:
            if form.is_valid() and formset.is_valid():
                reading = form.save(commit=False)
                reading.user = request.user
                reading.save()
                # add rep
                add_rep(request, rd=reading)
                # create notes for this reading
                for note_form in formset:
                    note = note_form.save(commit=False)
                    note.reading = reading
                    note.user = request.user
                    if note.content.strip():
                        note.save()
                        # create first vote for note
                        request.user.vote_set.create(note=note, value=1)
                messages.success(request, 'Reading created')
                return HttpResponseRedirect(reverse('readings.views.detail', 
                    args=[reading.slug]))
    else:
        form = ReadingForm()
        formset = NoteFormset()
    d = {
            'title': 'New Reading',
            'form': form,
            'formset': formset,
    }
    return render_to_response('readings/new.html', add_csrf(request, d), 
        context_instance=RequestContext(request))

@login_required
def scrape(request):
    """Scrape url for all images."""
    url = urllib2.urlopen(request.GET.get('url'))
    html = url.read()
    soup = BeautifulSoup(html)
    imgs = soup.find_all('img', src=re.compile('^http'))
    imgs = [i['src'] for i in imgs]
    html_title = soup.find('title').string[:80]
    t = loader.get_template('readings/images.html')
    c = Context({ 'imgs': imgs })
    data = {
                'imgs': t.render(c),
                'html_title': html_title,
    }
    return HttpResponse(json.dumps(data), mimetype='application/json')

def detail(request, slug):
    """Reading detail."""
    reading = get_object_or_404(Reading, slug=slug)
    comment_form = CommentForm()
    note_form = NoteForm()
    reply_form = ReplyForm()
    if request.user.is_anonymous():
        next = reverse('readings.views.detail', args=[slug])
        request.session['next'] = next
        user_tag = None
    else:
        next = ''
        request.session.get('next', '')
        user_tag = reading.tie_set.filter(user=request.user)
    d = {
            'comment_form': comment_form,
            'next': next,
            'note_form': note_form,
            'reading': reading,
            'reply_form': reply_form,
            'title': reading.title,
            'user_tag': user_tag,
    }
    return render_to_response('readings/detail.html', add_csrf(request, d), 
        context_instance=RequestContext(request))

@login_required
def detail_show(request, slug, show, pk):
    """Reading detail."""
    if show == 'comments':
        comment = get_object_or_404(Comment, pk=pk)
        a = {
                'comment_show': comment.note.pk,
                'comment_focus': comment.pk,
        }
    elif show == 'notes':
        note = get_object_or_404(Note, pk=pk)
        a = {
                'note_focus': note.pk,
        }
    elif show == 'replies':
        reply = get_object_or_404(Reply, pk=pk)
        a = {
                'comment_show': reply.comment.note.pk,
                'reply_focus': reply.pk,
                'reply_show': reply.comment.pk,
        }
    elif show == 'ties':
        tie = get_object_or_404(Tie, pk=pk)
        a = {
                'tie_focus': tie.pk,
        }
    elif show == 'votes':
        vote = get_object_or_404(Vote, pk=pk)
        note = vote.note
        if vote.value == 1:
            value = 1
        else:
            value = -1
        a = {
                'note_pk': note.pk,
                'value': value,
        }
    reading = get_object_or_404(Reading, slug=slug)
    comment_form = CommentForm()
    note_form = NoteForm()
    reply_form = ReplyForm()
    if request.user.is_anonymous():
        user_tag = None
    else:
        user_tag = reading.tie_set.filter(user=request.user)
    b = {
            'comment_form': comment_form,
            'note_form': note_form,
            'reading': reading,
            'reply_form': reply_form,
            'title': reading.title,
            'user_tag': user_tag,
    }
    d = dict(a.items() + b.items())
    return render_to_response('readings/detail.html', add_csrf(request, d), 
        context_instance=RequestContext(request))

def link(request, slug):
    """After clicking reading link, increment view and redirect to link."""
    reading = get_object_or_404(Reading, slug=slug)
    reading.views += 1
    reading.save()
    return HttpResponseRedirect(reading.link)

@login_required
def edit(request, slug):
    reading = get_object_or_404(Reading, slug=slug)
    if request.user.pk != reading.user.pk and not request.user.is_staff:
        return HttpResponseRedirect(reverse('readings.views.list_user', 
            args=[request.user.profile.slug]))
    if request.method == 'POST':
        form = EditReadingForm(request.POST, instance=reading)
        if form.is_valid():
            reading = form.save()
            messages.success(request, 'Reading updated')
            return HttpResponseRedirect(reverse('readings.views.detail', 
                args=[reading.slug]))
    else:
        form = EditReadingForm(instance=reading)
    d = {
            'form': form,
            'reading': reading,
            'title': 'Edit Reading',
    }
    return render_to_response('readings/new.html', add_csrf(request, d), 
        context_instance=RequestContext(request))

@login_required
def delete(request, slug):
    """Delete a reading."""
    reading = get_object_or_404(Reading, slug=slug)
    # if current user did not create reading and is not admin
    if request.user.pk != reading.user.pk and not request.user.is_staff:
        # redirect
        return HttpResponseRedirect(reverse('readings.views.list_user', 
            args=[request.user.profile.slug]))
    # Delete reading
    if request.method == 'POST' and request.POST.get('delete'):
        if reading.user.pk == request.user.pk or request.user.is_staff:
            delete_reading_image(reading)
            # del rep
            del_rep(request, rd=reading)
            reading.delete()
            messages.success(request, 'Read deleted')
        else:
            messages.error(request, 'You can only delete your reads')
    return HttpResponseRedirect(reverse('readings.views.list_user', 
        args=[request.user.profile.slug]))