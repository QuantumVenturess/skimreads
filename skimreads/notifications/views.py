from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from notifications.models import Notification

@login_required
def forward(request, pk):
    """Redirect current user to their destination."""
    notification = get_object_or_404(Notification, pk=pk)
    # If notification was for a comment
    if notification.comment:
        return HttpResponseRedirect(reverse('readings.views.detail_show', 
            kwargs={ 'slug': notification.comment.note.reading.slug, 
                     'show': 'comments',
                     'pk': notification.comment.pk }))
    # If notification was for a note
    elif notification.note:
        return HttpResponseRedirect(reverse('readings.views.detail_show', 
            kwargs={ 'slug': notification.note.reading.slug, 
                     'show': 'notes',
                     'pk': notification.note.pk }))
    # If notification was for a reply
    elif notification.reply:
        return HttpResponseRedirect(reverse('readings.views.detail_show', 
            kwargs={ 'slug': notification.reply.comment.note.reading.slug, 
                     'show': 'replies',
                     'pk': notification.reply.pk }))
    # If notification is for a tag tie
    elif notification.tie:
        return HttpResponseRedirect(reverse('readings.views.detail_show',
            kwargs={ 'slug': notification.tie.reading.slug,
                     'show': 'ties',
                     'pk': notification.tie.pk }))
    # If notification is for a vote
    elif notification.vote:
        if notification.vote.note:
            slug = notification.vote.note.reading.slug
        elif notification.vote.reading:
            slug = notification.vote.reading.slug
        return HttpResponseRedirect(reverse('readings.views.detail_show',
            kwargs={ 'slug': slug,
                     'show': 'votes',
                     'pk': notification.vote.pk }))

@login_required
def list(request):
    """Show all notifications for current user."""
    notifications = request.user.notification_set.all().order_by(
        '-created')[0:50]
    dates = sorted(set([n.date() for n in notifications]), 
        key=lambda n: datetime.strptime(n, '%b %d, %y'), reverse=True)
    days = []
    # Group notifications by date
    for day in dates:
        notis = [n for n in notifications if n.date() == day]
        days.append((day, notis))
    # Mark all unviewed notifications as viewed
    unviewed = request.user.notification_set.filter(viewed=False)
    if unviewed:
        for notification in unviewed:
            notification.viewed = True
            notification.save()
    d = {
            'days': days,
            'title': 'Notifications',
    }
    return render_to_response('notifications/list.html', d, 
        context_instance=RequestContext(request))