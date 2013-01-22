from comments.forms import CommentForm
from comments.models import Comment
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import loader, RequestContext, Template
from follows.utils import follow_user
from notifications.utils import notify
from readings.models import Note
from replies.forms import ReplyForm
from skimreads.utils import add_csrf
from users.utils import add_rep, del_rep

import json

@login_required
def new(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.note = note
            comment.user = request.user
            comment.save()
            # add rep
            add_rep(request, c=comment)
            # create notification
            notify(comment=comment)
            d = {
                    'comment': comment,
                    'comment_form': CommentForm(),
                    'note': note,
                    'reply_form': ReplyForm(),
            }
            comment = loader.get_template('comments/comment.html')
            comment_form = loader.get_template('comments/comment_form.html')
            context = RequestContext(request, add_csrf(request, d))
            data = {
                        'comment': comment.render(context),
                        'comment_count': note.comment_count(),
                        'comment_form': comment_form.render(context),
                        'pk': note.pk,
            }
            return HttpResponse(json.dumps(data), mimetype='application/json')
    return HttpResponseRedirect(reverse('readings.views.detail', 
        args=[reading.slug]))

@login_required
def delete(request, pk):
    """Delete a comment."""
    comment = get_object_or_404(Comment, pk=pk)
    note = comment.note
    if request.method == 'POST':
        if request.POST.get('delete') == str(comment.pk):
            if comment.user == request.user or request.user.is_staff:
                data = { 
                            'note_pk': note.pk,
                            'pk': comment.pk 
                }
                # del rep
                del_rep(request, c=comment)
                comment.delete()
                data['comment_count'] = note.comment_count()
                return HttpResponse(json.dumps(data), 
                    mimetype='application/json')
    return HttpResponseRedirect(reverse('readings.views.detail', 
        args=[comment.reading.slug]))