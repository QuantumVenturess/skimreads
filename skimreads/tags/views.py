from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import Context, loader, RequestContext, Template
from django.template.defaultfilters import slugify
from notifications.utils import notify
from readings.models import Reading
from skimreads.utils import add_csrf, page
from tags.models import Tag, Tie
from tags.utils import banned_words, only_letters
from users.utils import add_rep, del_rep

import json
import re

@login_required
def tag_list(request):
    """Return a list of tags in a html template."""
    name = request.GET.get('term', '')
    if name:
        tags = Tag.objects.filter(name__icontains=name).order_by('name')[0:5]
    else:
        tags = []
    t = loader.get_template('tags/tag_list.html')
    context = RequestContext(request, { 'tags': tags })
    data = { 'tag_list': t.render(context) }
    return HttpResponse(json.dumps(data), mimetype='application/json')

@login_required
def tag_list_new_reading(request):
    """Return tags in a json list."""
    name = request.GET.get('term', '')
    if name:
        tags = Tag.objects.filter(name__icontains=name).values('name')[0:5]
        tags = sorted([t['name'] for t in tags])
    else:
        tags = []
    return HttpResponse(json.dumps(tags), mimetype='application/json')

def detail(request, slug):
    """Show all readings for a single tag."""
    tag = get_object_or_404(Tag, slug=slug)
    readings = tag.readings()
    d = {
            'objects': page(request, readings, 10),
            'tag': tag,
            'title': '%s Reads' % tag.name.capitalize(),
    }
    return render_to_response('readings/feed.html', add_csrf(request, d), 
        context_instance=RequestContext(request))

def followers(request, slug):
    """Show all followers for tag."""
    tag = get_object_or_404(Tag, slug=slug)
    users = sorted([tf.user for tf in tag.tagfollow_set.all()])
    d = {
        'tag': tag,
        'title': '%s Followers' % tag.name.capitalize(),
        'users': users,
    }
    return render_to_response('tags/followers.html', add_csrf(request, d), 
        context_instance=RequestContext(request))

@login_required
def new(request, slug):
    """Create new tie for reading."""
    reading = get_object_or_404(Reading, slug=slug)
    if request.method == 'POST':
        # If reading has 5 tags, do not add or create
        if len(reading.tie_set.all()) >= 5:
            messages.warning(request, 'Each read can only have 5 tags')
        else:
            try:
                # If user already added a tag
                user = reading.tie_set.get(user=request.user)
                messages.error(request, 'You can only add 1 tag per read')
            except ObjectDoesNotExist:
                name = request.POST.get('tag_name')
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
                            d = {
                                    'reading': reading,
                            }
                            tags = loader.get_template('tags/tags.html')
                            context = RequestContext(request, d)
                            data = {
                                        'ties': tags.render(context),
                            }
                            return HttpResponse(json.dumps(data), 
                                mimetype='application/json')
    return HttpResponseRedirect(reverse('readings.views.detail', 
        args=[reading.slug]))

@login_required
def delete(request, slug):
    """Delete current user's tie tag for reading."""
    reading = get_object_or_404(Reading, slug=slug)
    if request.method == 'POST':
        try:
            tie = reading.tie_set.get(user=request.user)
            if request.POST.get('delete') == str(tie.pk):
                # del rep
                del_rep(request, t=tie)
                tie.delete()
                d = {
                        'reading': reading,
                }
                tag_form = loader.get_template('tags/tag_form.html')
                context = RequestContext(request, add_csrf(request, d))
                data = {
                            'tag_form': tag_form.render(context),
                            'tie_id': request.POST.get('delete'),
                }
                return HttpResponse(json.dumps(data), mimetype='application/json')
        except ObjectDoesNotExist:
            messages.error(request, 'You have not added a tag to this read')
    return HttpResponseRedirect(reverse('readings.views.detail', 
        args=[reading.slug]))