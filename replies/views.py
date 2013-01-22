from comments.models import Comment
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import loader, RequestContext
from notifications.utils import notify
from replies.forms import ReplyForm
from replies.models import Reply
from skimreads.utils import add_csrf
from users.utils import add_rep, del_rep

import json

@login_required
def new(request, pk):
    """Create new reply."""
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.comment = comment
            reply.user = request.user
            reply.save()
            # add rep
            add_rep(request, rp=reply)
            # create notification
            notify(reply=reply)
            d = {
                    'comment': comment,
                    'reply': reply,
                    'reply_form': ReplyForm(),
            }
            reply = loader.get_template('replies/reply.html')
            reply_form = loader.get_template('replies/reply_form.html')
            context = RequestContext(request, add_csrf(request, d))
            data = {
                        'reply': reply.render(context),
                        'reply_count': comment.reply_count(),
                        'reply_form': reply_form.render(context),
                        'pk': comment.pk,
            }
            return HttpResponse(json.dumps(data), mimetype='application/json')
    return HttpResponseRedirect(reverse('readings.views.detail', 
        args=[comment.note.reading.slug]))

@login_required
def delete(request, pk):
    """Delete reply."""
    reply = get_object_or_404(Reply, pk=pk)
    comment = reply.comment
    if request.method == 'POST':
        if request.POST.get('delete') == str(reply.pk):
            if reply.user == request.user or request.user.is_staff:
                data = { 
                            'comment_pk': comment.pk,
                            'pk': reply.pk 
                }
                # del rep
                del_rep(request, rp=reply)
                reply.delete()
                data['reply_count'] = comment.reply_count()
                return HttpResponse(json.dumps(data), 
                    mimetype='application/json')
    return HttpResponseRedirect(reverse('readings.views.detail', 
        args=[comment.note.reading.slug]))