from collections import defaultdict
from comments.forms import CommentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import loader, RequestContext
from notifications.utils import notify
from readings.forms import NoteForm
from readings.models import Note, Reading
from skimreads.utils import add_csrf
from users.utils import add_rep, del_rep

import json

@login_required
def new(request, slug):
    """Create new note for reading."""
    reading = get_object_or_404(Reading, slug=slug)
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.reading = reading
            note.user = request.user
            note.save()
            # add rep
            add_rep(request, n=note)
            request.user.vote_set.create(note=note, value=1)
            notify(note=note)
            d = {
                    'comment_form': CommentForm(),
                    'note': note,
                    'note_form': NoteForm(),
                    'reading': reading,
            }
            bullet_notes = loader.get_template('notes/bullet_notes.html')
            note = loader.get_template('notes/note.html')
            note_form = loader.get_template('notes/note_form.html')
            context = RequestContext(request, add_csrf(request, d))
            data = {
                        'bullet_notes': bullet_notes.render(context),
                        'note': note.render(context),
                        'note_form': note_form.render(context),
            }
            return HttpResponse(json.dumps(data), mimetype='application/json')
    return HttpResponseRedirect(reverse('readings.views.detail', 
        args=[reading.slug]))

@login_required
def delete(request, pk):
    """Delete note."""
    note = get_object_or_404(Note, pk=pk)
    reading = note.reading
    if request.method == 'POST':
        # if delete value equals note's pk
        if request.POST.get('delete') == str(note.pk):
            # if current user created note or is staff
            if request.user.pk == note.user.pk or request.user.is_staff:
                data = defaultdict(str)
                note_count = reading.note_count()
                if note_count > 1:
                    note_pk = note.pk
                    # del rep
                    del_rep(request, n=note)
                    note.delete()
                    d = {
                            'reading': reading,
                    }
                    bullet_notes = loader.get_template(
                        'notes/bullet_notes.html')
                    context = RequestContext(request, add_csrf(request, d))
                    data = { 
                                'bullet_notes': bullet_notes.render(context),
                                'pk': note_pk,
                    }
                data['note_count'] = note_count
                return HttpResponse(json.dumps(data), 
                    mimetype='application/json')
    return HttpResponseRedirect(reverse('readings.views.detail', 
        args=[reading.slug]))