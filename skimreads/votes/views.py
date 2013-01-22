from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import loader, RequestContext
from django.utils import timezone
from notifications.models import Notification
from notifications.utils import notify
from readings.models import Note
from skimreads.utils import add_csrf
from users.utils import add_rep, del_rep

import json

@login_required
def new(request, pk):
    """Create a downvote or upvote for note."""
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST' and request.POST.get('action'):
        # If user is downvoting the note
        if request.POST.get('action') == 'downvote':
            value = -1
        # If user is upvoting the note
        elif request.POST.get('action') == 'upvote':
            value = 1
        try:
            # Check to see if user already voted
            vote = note.vote_set.get(user=request.user)
            # If user already upvoted
            if vote.value == 1:
                # If user is upvoting again, remove the vote
                if value == 1:
                    # del rep
                    del_rep(request, v=vote)
                    vote.delete()
                # If user is downvoting, downvote the note
                else:
                    vote.value = value
                    vote.save()
                    # If user changes their vote, update the notifications
                    notifications = Notification.objects.filter(vote=vote)
                    for notification in notifications:
                        notification.created = timezone.now()
                        notification.viewed = False
                        notification.save()
            # If user already downvoted
            elif vote.value == -1:
                # If user is downvoting again, remove the vote
                if value == -1:
                    # del rep
                    del_rep(request, v=vote)
                    vote.delete()
                # If user is upvoting, upvote the note
                else:
                    vote.value = value
                    vote.save()
                    # If user changes their vote, update the notifications
                    notifications = Notification.objects.filter(vote=vote)
                    for notification in notifications:
                        notification.created = timezone.now()
                        notification.viewed = False
                        notification.save()
        except ObjectDoesNotExist:
            # If the user has not yet voted, create a new vote
            vote = request.user.vote_set.create(note=note, value=value)
            # add rep
            add_rep(request, v=vote)
            # create notification
            notify(vote=vote)
        d = {
                'note': note,
                'reading': note.reading,
        }
        bullet_notes = loader.get_template('notes/bullet_notes.html')
        vote_form = loader.get_template('votes/vote_form.html')
        context = RequestContext(request, add_csrf(request, d))
        data = {
                    'bullet_notes': bullet_notes.render(context),
                    'pk': note.pk,
                    'vote_form': vote_form.render(context),
        }
        return HttpResponse(json.dumps(data), mimetype='application/json')
    return HttpResponseRedirect(reverse('readings.views.detail', 
        args=[note.reading.slug]))