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
from django.template.defaultfilters import slugify
from follows.utils import follow_user, followed_ids
from oauth.facebook import facebook_graph_add_reading
from readings.forms import EditReadingForm, NoteForm, ReadingForm
from readings.models import Note, Reading
from readings.utils import crop_image, delete_reading_image
from replies.forms import ReplyForm
from replies.models import Reply
from sessions.decorators import bookmarklet_login_required
from skimreads.utils import add_csrf, page
from tags.models import Tag, Tie
from tags.utils import auto_tag, banned_words, only_letters
from usermessages.forms import NewMessageForm
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
    NoteFormset = formset_factory(NoteForm, extra=3)
    if request.method == 'POST':
        link = request.POST.get('link')
        form = ReadingForm(request.POST)
        formset = NoteFormset(request.POST)
        # if reading with link already exists, add notes to it
        try:
            reading = Reading.objects.get(link=link)
            if formset.is_valid():
                # add tag
                name = request.POST.get('tag_name')
                # if user added a tag
                if name:
                    name = name.lower()
                    pattern = only_letters()
                    # If name contains only letters
                    if re.search(pattern, name):
                        # If name does not contain any banned words
                        blacklist = banned_words()
                        if not re.search(blacklist, name):
                            try:
                                # If tag exists, get tag
                                tag = Tag.objects.get(name=name)
                            except ObjectDoesNotExist:
                                # If tag does not exist, create tag
                                tag = Tag(name=name, user=request.user)
                                tag.slug = slugify(tag.name)
                                tag.save()
                            try:
                                # Check to see if tie exists
                                tie = reading.tie_set.get(tag=tag)
                            except ObjectDoesNotExist:
                                # If tie does not exist, create it
                                tie = request.user.tie_set.create(
                                    reading=reading, tag=tag)
                                # add rep
                                add_rep(request, t=tie)
                                # create notification
                                notify(tie=tie)
                    # if user did not add a tag, auto tag
                    else:
                        auto_tag(request, reading)
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
                    'This reading exists, your content has been added to it')
                return HttpResponseRedirect(reverse('readings.views.detail', 
                    args=[reading.slug]))
        # if reading with link does not exist, create the reading
        except ObjectDoesNotExist:
            if form.is_valid() and formset.is_valid():
                reading = form.save(commit=False)
                reading.user = request.user
                reading.save()
                # create vote for reading
                reading.vote_set.create(user=reading.user, value=1)
                # add tag
                name = request.POST.get('tag_name')
                # if user added tag
                if name:
                    name = name.lower()
                    pattern = only_letters()
                    # If name contains only letters
                    if re.search(pattern, name):
                        # If name does not contain any banned words
                        blacklist = banned_words()
                        if not re.search(blacklist, name):
                            try:
                                # If tag exists, get tag
                                tag = Tag.objects.get(name=name)
                            except ObjectDoesNotExist:
                                # If tag does not exist, create tag
                                tag = Tag(name=name, user=request.user)
                                tag.slug = slugify(tag.name)
                                tag.save()
                            tie = request.user.tie_set.create(reading=reading, 
                                tag=tag)
                            # add rep
                            add_rep(request, t=tie)
                # if user did not add a tag, auto tag
                else:
                    auto_tag(request, reading)
                # facebook open graph add reading
                facebook_graph_add_reading(request.user, reading)
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
    di = { 'static': settings.STATIC_URL }
    t = loader.get_template('javascript/bookmarklet.js')
    context = RequestContext(request, di)
    d = {
        'bookmarklet': re.sub(r'\s', '%20', str(t.render(context))),
        'form': form,
        'formset': formset,
        'title': 'New Reading',
    }
    return render_to_response('readings/new.html', add_csrf(request, d), 
        context_instance=RequestContext(request))

@bookmarklet_login_required()
def new_bookmarklet(request):
    """Create new reading from bookmarklet."""
    if request.method == 'POST':
        content = request.POST.get('content', '')
        image = request.POST.get('image', '')
        link = request.POST.get('link', '')
        titl = request.POST.get('title', '')
        # if there is a link and title, create reading
        if link and titl:
            try:
                reading = Reading.objects.get(link=link)
            except ObjectDoesNotExist:
                titles = Reading.objects.filter(title=titl)
                if titles:
                    titl = '%s-%s' % (titl, str(titles.count()))
                reading = Reading(image=image, link=link, title=titl, 
                    user=request.user)
                reading.save()
                # create vote for reading
                reading.vote_set.create(user=reading.user, value=1)
            # add tag
            name = request.POST.get('tag_name')
            # if user added tag
            if name:
                name = name.lower()
                pattern = only_letters()
                # If name contains only letters
                if re.search(pattern, name):
                    # If name does not contain any banned words
                    blacklist = banned_words()
                    if not re.search(blacklist, name):
                        try:
                            # If tag exists, get tag
                            tag = Tag.objects.get(name=name)
                        except ObjectDoesNotExist:
                            # If tag does not exist, create tag
                            tag = Tag(name=name, user=request.user)
                            tag.slug = slugify(tag.name)
                            tag.save()
                        tie = request.user.tie_set.create(reading=reading, 
                            tag=tag)
                        # add rep
                        add_rep(request, t=tie)
            # if user did not add a tag, auto tag
            else:
                auto_tag(request, reading)
            # facebook open graph add reading
            facebook_graph_add_reading(request.user, reading)
            # add rep
            add_rep(request, rd=reading)
            # if there is content, create note
            if content.strip():
                note = Note(content=content, reading=reading, 
                    user=reading.user)
                note.save()
                # create first vote for note
                request.user.vote_set.create(note=note, value=1)
            data = { 'success': 1 }
            return HttpResponse(json.dumps(data), 
                mimetype='application/json')
    content = request.GET.get('note', '').lstrip(' ')
    link = request.GET.get('link', '')
    title = request.GET.get('title', '')[:80]
    if len(title.split('|')) >= 2:
        first, second = title.split('|')
        if len(first) >= len(second):
            html_title = first
        else:
            html_title = second
    else:
        html_title = title
    d = {
        'content': content,
        'link': link,
        'titl': html_title,
        'title': 'Add Reading',
    }
    return render_to_response('readings/new_bookmarklet.html', 
        add_csrf(request, d), context_instance=RequestContext(request))
    
@login_required
def scrape(request):
    """Scrape url for all images."""
    url = request.GET.get('url')
    req = urllib2.Request(url, headers={ 'User-Agent': 'Magic Browser' })
    con = urllib2.urlopen(req)
    html = con.read()
    soup = BeautifulSoup(html)
    imgs = soup.find_all('img')
    imgs = [i.get('src') for i in imgs if i.get('src')]
    title = soup.find('title').string[:80]
    if len(title.split('|')) >= 2:
        first, second = title.split('|')
        if len(first) >= len(second):
            html_title = first
        else:
            html_title = second
    else:
        html_title = title
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
    # get next and previous reading
    readings = Reading.objects.all().values('pk').order_by('pk')
    first_pk = readings[0]['pk']
    last_pk = readings.reverse()[0]['pk']
    next_count = reading.pk + 1
    next_read = None
    prev_count = reading.pk - 1
    prev_read = None
    # if reading is the most recent reading
    if reading.pk == last_pk:
        next_read = Reading.objects.get(pk=first_pk)
    # if reading is not the most recent reading
    else:
        while not next_read and next_count <= last_pk:
            try:
                next_read = Reading.objects.get(pk=next_count)
            except ObjectDoesNotExist:
                next_count += 1
    # if reading is the oldest reading
    if reading.pk == first_pk:
        prev_read = Reading.objects.get(pk=last_pk)
    # if reading is not the oldest reading
    else:
        while not prev_read and prev_count >= first_pk:
            try:
                prev_read = Reading.objects.get(pk=prev_count)
            except ObjectDoesNotExist:
                prev_count -= 1
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
            'form': NewMessageForm(),
            'next': next,
            'next_read': next_read,
            'note_form': note_form,
            'prev_read': prev_read,
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
        if vote.value == 1:
            value = 1
        else:
            value = -1
        if vote.note:
            a = { 'note_pk': vote.note.pk }
        elif vote.reading:
            a = { 'reading_pk': vote.reading.pk }
        a['value'] = value
    reading = get_object_or_404(Reading, slug=slug)
    # get next and previous reading
    readings = Reading.objects.all().values('pk').order_by('pk')
    first_pk = readings[0]['pk']
    last_pk = readings.reverse()[0]['pk']
    next_count = reading.pk + 1
    next_read = None
    prev_count = reading.pk - 1
    prev_read = None
    # if reading is the most recent reading
    if reading.pk == last_pk:
        next_read = Reading.objects.get(pk=first_pk)
    # if reading is not the most recent reading
    else:
        while not next_read and next_count <= last_pk:
            try:
                next_read = Reading.objects.get(pk=next_count)
            except ObjectDoesNotExist:
                next_count += 1
    # if reading is the oldest reading
    if reading.pk == first_pk:
        prev_read = Reading.objects.get(pk=last_pk)
    # if reading is not the oldest reading
    else:
        while not prev_read and prev_count >= first_pk:
            try:
                prev_read = Reading.objects.get(pk=prev_count)
            except ObjectDoesNotExist:
                prev_count -= 1
    comment_form = CommentForm()
    note_form = NoteForm()
    reply_form = ReplyForm()
    if request.user.is_anonymous():
        user_tag = None
    else:
        user_tag = reading.tie_set.filter(user=request.user)
    b = {
            'comment_form': comment_form,
            'form': NewMessageForm(),
            'next_read': next_read,
            'note_form': note_form,
            'prev_read': prev_read,
            'reading': reading,
            'reply_form': reply_form,
            'title': reading.title,
            'user_tag': user_tag,
    }
    d = dict(a.items() + b.items())
    return render_to_response('readings/detail.html', add_csrf(request, d), 
        context_instance=RequestContext(request))

def permalink(request, slug):
    """Permanent link."""
    reading = get_object_or_404(Reading, slug=slug)
    d = {
        'reading': reading,
    }
    return render_to_response('readings/permalink.html', d, 
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
        # only save the image
        reading.image = request.POST.get('image')
        reading.save()
        messages.success(request, 'Reading updated')
        return HttpResponseRedirect(reverse('readings.views.detail', 
            args=[reading.slug]))
    d = {
            'form': EditReadingForm(instance=reading),
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