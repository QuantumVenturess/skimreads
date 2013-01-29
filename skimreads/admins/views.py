from admins.utils import first_ten_users, random_user
from comments.forms import AdminCommentForm, DavidCommentForm
from comments.models import Comment
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.template.defaultfilters import slugify
from notifications.utils import notify
from oauth.facebook import facebook_graph_add_note, facebook_graph_add_reading
from random import randint
from readings.forms import (AdminNoteForm, DavidNoteForm, AdminReadingForm, 
    DavidReadingForm, NoteForm, RequiredFormSet)
from readings.models import Note, Reading
from replies.forms import AdminReplyForm, DavidReplyForm
from sessions.decorators import staff_user
from skimreads.utils import add_csrf
from tags.models import Tag
from tags.utils import auto_tag, banned_words, only_letters
from users.utils import add_rep

import re

@staff_user()
def test(request):
    """Test page."""
    return render_to_response('admins/test.html', 
        context_instance=RequestContext(request))

@staff_user()
def new_reading(request):
    """Create a new reading."""
    NoteFormset = formset_factory(NoteForm, extra=3, formset=RequiredFormSet)
    if request.method == 'POST':
        if request.user.pk == 2:
            form = DavidReadingForm(request.POST)
        else:
            form = AdminReadingForm(request.POST)
        formset = NoteFormset(request.POST)
        if form.is_valid() and formset.is_valid():
            # save reading
            reading = form.save()
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
                        tie = request.user.tie_set.create(reading=reading, 
                            tag=tag)
                        # add rep
                        add_rep(request, t=tie)
            # if user did not add a tag, auto tag
            else:
                auto_tag(request, reading)
            # facebook open graph add reading
            if reading.user.pk == request.user.pk:
                facebook_graph_add_reading(request.user, reading)
            # add rep
            add_rep(request, rd=reading)
            first = True
            # save each note
            for note_form in formset:
                note = note_form.save(commit=False)
                if note.content.strip():
                    note.reading = reading
                    # if this is the first note
                    # set note.user to reading.user
                    if first:
                        note.user = reading.user
                        first = False
                    else:
                        note.user = random_user()
                    # save note
                    note.save()
                    # create first vote for note
                    note.user.vote_set.create(note=note, value=1)
                    # add rep
                    add_rep(request, n=note)
            notes = reading.note_set.all()
            users = first_ten_users()
            # create votes for first ten users
            for user in users:
                # vote each note
                for note in notes:
                    vote = note.vote_set.filter(user=user)
                    if not vote:
                        if randint(0, 4):
                            value = 1
                        else:
                            value = -1
                        # create vote
                        vote = note.vote_set.create(user=user, value=value)
                        # add rep
                        add_rep(request, v=vote)
                # vote reading
                vote = reading.vote_set.filter(user=user)
                if not vote:
                    if randint(0, 4):
                        value = 1
                    else:
                        value = -1
                    # create vote
                    vote = reading.vote_set.create(user=user, value=value)
                    # add rep
                    add_rep(request, v=vote)
            messages.success(request, 'Reading created')
            return HttpResponseRedirect(reverse('admins.views.reading', 
                args=[reading.slug]))
    else:
        if request.user.pk == 2:
            form = DavidReadingForm()
        else:
            form = AdminReadingForm()
        formset = NoteFormset()
    d = {
        'form': form,
        'formset': formset,
        'title': 'New Reading',
    }
    return render_to_response('readings/new.html', add_csrf(request, d), 
        context_instance=RequestContext(request))

@staff_user()
def vote_all(request, slug):
    reading = get_object_or_404(Reading, slug=slug)
    notes = reading.note_set.all()
    users = first_ten_users()
    # create votes for first ten users
    for user in users:
        # vote each note
        for note in notes:
            vote = note.vote_set.filter(user=user)
            if not vote:
                if randint(0, 4):
                    value = 1
                else:
                    value = -1
                # create vote
                vote = note.vote_set.create(user=user, value=value)
                # add rep
                add_rep(request, v=vote)
        # vote reading
        vote = reading.vote_set.filter(user=user)
        if not vote:
            if randint(0, 4):
                value = 1
            else:
                value = -1
            # create vote
            vote = reading.vote_set.create(user=user, value=value)
            # add rep
            add_rep(request, v=vote)
    messages.success(request, 'Votes created')
    return HttpResponseRedirect(reverse('admins.views.reading', 
        args=[reading.slug]))

@staff_user()
def reading(request, slug):
    """Detail reading."""
    reading = get_object_or_404(Reading, slug=slug)
    if request.method == 'POST':
        if request.user.pk == 2:
            form = DavidNoteForm(request.POST)
        else:
            form = AdminNoteForm(request.POST)
        if form.is_valid():
            # save note
            note = form.save(commit=False)
            note.reading = reading
            note.save()
            # facebook open graph add note
            if note.user.pk == request.user.pk:
                facebook_graph_add_note(request.user, reading)
            # add rep
            add_rep(request, n=note)
            # create notification
            notify(note=note)
            note.user.vote_set.create(note=note, value=1)
            messages.success(request, 'Note created')
            return HttpResponseRedirect(reverse('admins.views.reading', 
                args=[reading.slug]))
    else:
        if request.user.pk == 2:
            form = DavidNoteForm()
        else:
            form = AdminNoteForm()
    d = {
        'form': form,
        'reading': reading,
        'title': 'Reading: Add Note',
    }
    return render_to_response('admins/detail_reading.html', 
        add_csrf(request, d), context_instance=RequestContext(request))

@staff_user()
def note(request, pk):
    """Detail note."""
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        if request.user.pk == 2:
            form = DavidCommentForm(request.POST)
        else:
            form = AdminCommentForm(request.POST)
        if form.is_valid():
            # save comment
            comment = form.save(commit=False)
            comment.note = note
            comment.save()
            # add rep
            add_rep(request, c=comment)
            # create notification
            notify(comment=comment)
            messages.success(request, 'Comment created')
            return HttpResponseRedirect(reverse(
                'admins.views.note', args=[note.pk]))
    else:
        if request.user.pk == 2:
            form = DavidCommentForm(request.POST)
        else:
            form = AdminCommentForm()
    d = {
        'form': form,
        'note': note,
        'note_pk': note.pk,
        'title': 'Note: Add Comment',
    }
    return render_to_response('admins/detail_note.html', 
        add_csrf(request, d), context_instance=RequestContext(request))

@staff_user()
def comment(request, pk):
    """Detail comment."""
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        if request.user.pk == 2:
            form = DavidReplyForm(request.POST)
        else:
            form = AdminReplyForm(request.POST)
        if form.is_valid():
            # save reply
            reply = form.save(commit=False)
            reply.comment = comment
            reply.save()
            # add rep
            add_rep(request, rp=reply)
            # create notification
            notify(reply=reply)
            messages.success(request, 'Reply created')
            return HttpResponseRedirect(reverse(
                'admins.views.comment', args=[comment.pk]))
    else:
        if request.user.pk == 2:
            form = DavidReplyForm()
        else:
            form = AdminReplyForm()
    d = {
        'comment': comment,
        'comment_pk': comment.pk,
        'form': form,
        'title': 'Comment: Add Reply',
    }
    return render_to_response('admins/detail_comment.html', 
        add_csrf(request, d), context_instance=RequestContext(request))