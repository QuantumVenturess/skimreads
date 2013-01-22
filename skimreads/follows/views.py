from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import loader, RequestContext
from django.utils import timezone
from notifications.utils import notify
from skimreads.utils import add_csrf, page
from tags.models import Tag
from users.utils import add_rep, del_rep, user_exists

import json

@login_required
def follow(request, slug):
    """Follow or unfollow a user."""
    user = user_exists(slug)
    change_count = 1
    # if request method is POST and
    # the follow/unfollow user is not the current user
    if request.method == 'POST' and user.pk != request.user.pk:
        # if request POST has follow in it
        if request.POST.get('follow'):
            # follow user
            follow = user.followed_set.create(follower=request.user)
            # add rep
            add_rep(request, fw=follow)
            # create notification
            notify(follow=follow)
        # if request POST has unfollow in it
        elif request.POST.get('unfollow'):
            # unfollow user
            follow = user.followed_set.filter(follower=request.user)[0]
            # del rep
            del_rep(request, fw=follow)
            follow.delete()
        # if current user is on another user's page
        if user.pk == int(request.POST.get('current_pk', 0)):
            followers_count = str(user.profile.followers_count())
            following_count = str(user.profile.following_count())
        # if current user is on their own page
        elif request.user.pk == int(request.POST.get('current_pk', 0)):
            followers_count = str(request.user.profile.followers_count())
            following_count = str(request.user.profile.following_count())
        # if current user is not on anyone's page
        else:
            followers_count = 0
            following_count = 0
            change_count = 0
        d = {
                'current_pk': request.POST.get('current_pk'),
                'profile_user': user,
        }
        t = loader.get_template('follows/follow_form.html')
        c = RequestContext(request, add_csrf(request, d))
        data = { 
                    'change_count': change_count,
                    'follow_form': t.render(c),
                    'followers_count': followers_count,
                    'following_count': following_count,
                    'user_id': str(user.pk),
        }
        return HttpResponse(json.dumps(data), mimetype='application/json')
    else:
        return HttpResponseRedirect(reverse('readings.views.list_user', 
            args=[profile.slug]))

@login_required
def follow_tag(request, slug):
    """Follow or unfollow a tag."""
    tag = get_object_or_404(Tag, slug=slug)
    if request.method == 'POST':
        # If current user is already following tag
        if request.user in tag.followers():
            # delete tag follow
            tagfollow = tag.tagfollow_set.get(user=request.user)
            # del rep
            del_rep(request, tf=tagfollow)
            tagfollow.delete()
        # If current user is not following tag
        else:
            # create tag follow
            tagfollow = request.user.tagfollow_set.create(tag=tag)
            # add rep
            add_rep(request, tf=tagfollow)
        d = {
            'tag': tag,
        }
        t = loader.get_template('follows/tagfollow_form.html')
        context = RequestContext(request, add_csrf(request, d))
        data = { 
            'tagfollowers_count': tag.followers_count(),
            'tag_pk': tag.pk,
            'tagfollow_form': t.render(context),
            'topic_count': request.user.profile.topic_count(),
        }
        return HttpResponse(json.dumps(data), mimetype='application/json')
    return HttpResponseRedirect(reverse('tags.views.detail', 
        args=[tag.slug]))

@login_required
def show_follows(request, slug, action):
    """Show all followers for user."""
    user = user_exists(slug)
    if action == 'followers':
        a = { 
            'users': user.profile.followers(),
        }
    elif action == 'following':
        a = { 
            'users': user.profile.following(),
        }
    elif action == 'topics':
        a = {
            'topics': user.profile.topics(),
        }
    d = {
            'current_pk': user.pk,
            'profile_user': user,
            'title': "%s's %s" % (user.first_name, action.capitalize()),
    }
    d.update(a)
    return render_to_response('follows/follows.html', d, 
        context_instance=RequestContext(request))