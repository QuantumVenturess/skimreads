from collections import defaultdict
from comments.forms import CommentForm
from django.conf import settings
from django.contrib import auth, messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import loader, RequestContext
from django.template.defaultfilters import slugify
from readings.forms import NoteForm
from readings.models import Reading
from readings.utils import reading_sorted
from replies.forms import ReplyForm
from sessions.decorators import already_logged_in
from skimreads.utils import add_csrf, page
from users.forms import EditUserForm, ProfileForm, SignUpForm
from users.models import Profile
from users.utils import *

import boto
import json
import os

# Users

@already_logged_in()
def new(request):
    """Create new user."""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            user = auth.authenticate(email=request.POST.get('email').lower())
            auth.login(request, user)
            # If the user is signing up through ajax form
            pk = request.POST.get('reading')
            if pk:
                reading = get_object_or_404(Reading, pk=pk)
                # Create a dictionary of comment & vote forms for each note
                comment_forms = defaultdict(str)
                vote_forms = defaultdict(str)
                notes = reading.note_set.all()
                for note in notes:
                    d = { 
                        'comment_form': CommentForm(),
                        'note': note,
                    }
                    t = loader.get_template('comments/comment_form.html')
                    v = loader.get_template('votes/vote_form.html')
                    context = RequestContext(request, add_csrf(request, d))
                    comment_forms[str(note.pk)] = t.render(context)
                    vote_forms[str(note.pk)] = v.render(context)
                # Create a dictionary of reply forms for each comment
                reply_forms = defaultdict(str)
                comments = reading.comments()
                for comment in comments:
                    d = {
                        'comment': comment,
                        'reply_form': ReplyForm(),
                    }
                    t = loader.get_template('replies/reply_form.html')
                    context = RequestContext(request, add_csrf(request, d))
                    reply_forms[str(comment.pk)] = t.render(context)
                # Create the note & tag form
                d = {
                        'note_form': NoteForm(),
                        'reading': reading,
                        'static': settings.STATIC_URL,
                }
                favorite_form = loader.get_template('favorites/favorite_form.html')
                header = loader.get_template('header.html')
                note_form = loader.get_template('notes/note_form.html')
                tag_form = loader.get_template('tags/tag_form.html')
                context = RequestContext(request, add_csrf(request, d))
                # Ready all the partials to be outputted as JSON
                data = {
                    'comment_forms': comment_forms,
                    'favorite_form': favorite_form.render(context),
                    'header': header.render(context),
                    'note_form': note_form.render(context),
                    'reply_forms': reply_forms,
                    'success': 'yes',
                    'tag_form': tag_form.render(context),
                    'vote_forms': vote_forms,
                }
                return HttpResponse(json.dumps(data), 
                    mimetype='application/json')
            messages.success(request, 
                """Welcome %s, skim some reads and discover 
                something new""" % user.first_name)
            return HttpResponseRedirect(reverse('readings.views.discover'))
        else:
            pk = request.POST.get('reading')
            if pk:
                data = {
                    'success': 'no',
                }
                return HttpResponse(json.dumps(data), 
                    mimetype='application/json')
    else:
        form = SignUpForm()
    d = {
            'title': 'Welcome',
            'form': form,
    }
    return render_to_response('users/new.html', add_csrf(request, d), 
        context_instance=RequestContext(request))

@login_required
def edit(request, slug):
    """Edit user page."""
    user = user_exists(slug)
    # Correct user
    if request.user.pk is not user.pk:
        return HttpResponseRedirect(reverse('readings.views.list_user', 
            args=[request.user.profile.slug]))
    profile = user.profile
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, 
            instance=profile)
        if form.is_valid() and profile_form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password1')
            # If user changed their password
            if password:
                user.set_password(password)
                user.save()
            user = form.save()
            # If an image is uploaded
            profile = profile_form.save()
            # If user changed their username
            if username:
                profile.slug = slugify(username)
                # if user has a profile image and checked clear image
                if profile.image and request.POST.get('clear_image'):
                    profile.image = ''
                    s3_delete_file(user)
                profile.save()
            if request.FILES.get('image'):
                file_path = settings.MEDIA_ROOT + '/' + profile.image.name
                try:
                    f = open(file_path)
                    f.close()
                    name = str(user.pk) + '_orig.jpg'
                    # Get absolute path of image
                    absolute_path = absolute_image_path(profile)
                    # Rename image
                    rename_image(name, absolute_path)
                    # Resize original image if too large
                    resize_orig_image(user)
                    # Create medium and small images
                    create_extra_images(user)
                    # Upload images to Amazon S3
                    s3_upload(user)
                    # Remove any old images
                    #remove_images(user)
                    # Save profile image name
                    #profile.image = name
                    #profile.save()
                    messages.success(request, '%s - %s' %(name, absolute_path))
                except IOError as e:
                    messages.error(request, 'file path does not exist')
            messages.success(request, 'User updated')
            return HttpResponseRedirect(reverse('readings.views.list_user', 
                args=[user.profile.slug]))
    else:
        form = EditUserForm(instance=user)
        profile_form = ProfileForm(instance=profile)
    d = {
            'title': 'Edit %s' % user.first_name,
            'form': form,
            'profile_form': profile_form,
    }
    return render_to_response('users/edit.html', add_csrf(request, d), 
        context_instance=RequestContext(request))

@login_required
def category(request, slug, category):
    """
    Show all readings that user has commented, 
    faved, added a note, tagged, or voted on.
    """
    profile = get_object_or_404(Profile, slug=slug)
    user = profile.user
    if category == 'comments':
        if profile.comment_reply_count() == 0:
            return HttpResponseRedirect(reverse('readings.views.list_user', 
                args=[profile.slug]))
        li = [comment.note.reading for comment in user.comment_set.all()]
        li += [reply.comment.note.reading for reply in user.reply_set.all()]
        li = set(li)
        title = 'Commented'
    if category == 'favorites':
        if profile.favorite_count() == 0:
            return HttpResponseRedirect(reverse('readings.views.list_user', 
                args=[profile.slug]))
        li = set([fave.reading for fave in user.favorite_set.all()])
        title = 'Favorite'
    if category == 'notes':
        if profile.note_count() == 0:
            return HttpResponseRedirect(reverse('readings.views.list_user', 
                args=[profile.slug]))
        li = set([note.reading for note in user.note_set.all()])
        title = 'Noted'
    if category == 'tags':
        if profile.tie_count() == 0:
            return HttpResponseRedirect(reverse('readings.views.list_user', 
                args=[profile.slug]))
        li = set([tie.reading for tie in user.tie_set.all()])
        title = 'Tagged'
    if category == 'votes':
        if profile.vote_count() == 0:
            return HttpResponseRedirect(reverse('readings.views.list_user', 
                args=[profile.slug]))
        li = set([vote.note.reading for vote in user.vote_set.all()])
        title = 'Voted'
    readings = reading_sorted(li)
    d = {
            'current_pk': user.pk,
            'objects': page(request, readings, 10),
            'profile_user': user,
            'title': "%s's %s Readings" % (user.first_name, title),
    }
    return render_to_response('readings/feed.html', add_csrf(request, d), 
        context_instance=RequestContext(request))