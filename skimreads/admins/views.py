from admins.utils import first_ten_users, random_user
from comments.forms import AdminCommentForm
from comments.models import Comment
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from notifications.utils import notify
from oauth.facebook import facebook_graph_add_note, facebook_graph_add_reading
from random import randint
from readings.forms import (AdminNoteForm, AdminReadingForm, NoteForm, 
    RequiredFormSet)
from readings.models import Note, Reading
from replies.forms import AdminReplyForm
from sessions.decorators import staff_user
from skimreads.utils import add_csrf
from users.utils import add_rep

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
        form = AdminReadingForm(request.POST)
        formset = NoteFormset(request.POST)
        if form.is_valid() and formset.is_valid():
            # save reading
            reading = form.save()
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
        form = AdminReplyForm()
    d = {
        'comment': comment,
        'comment_pk': comment.pk,
        'form': form,
        'title': 'Comment: Add Reply',
    }
    return render_to_response('admins/detail_comment.html', 
        add_csrf(request, d), context_instance=RequestContext(request))