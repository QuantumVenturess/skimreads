from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from PIL import Image
from users.models import Profile

import boto
import os
import PIL
import shutil

def absolute_image_path(profile):
    """Return the absolute path of an image."""
    n = profile.image.name.split('/')
    return os.path.abspath(os.path.join(os.path.dirname(__file__), 
        '..', 'media', n[0], n[1], n[2])).replace('\\', '/')

def add_rep(request, rd=None, n=None, c=None, rp=None, t=None, v=None, 
    fv=None, fw=None, tf=None):
    """Increment reputation points for user(s).
    rd = Reading, n = Note, c = Comment, rp = Reply, 
    t = Tie, v = Vote, fv = Favorite, fw = Follow, tf = TagFollow."""
    # if reading
    if rd:
        prd = rd.user.profile
        # add 1 point to reading.user
        prd.reputation += 1
        prd.save()
    # if note
    elif n:
        pn = n.user.profile
        # add 1 point to note.user
        pn.reputation += 1
        pn.save()
        # add 1 point to note.reading.user
        # if the note.user != note.reading.user
        if n.user.pk != n.reading.user.pk:
            prd = n.reading.user.profile
            prd.reputation += 1
            prd.save()
    # if comment
    elif c:
        pc = c.user.profile
        # add 1 point to comment.user
        pc.reputation +=1
        pc.save()
        # add 1 point to comment.note.user
        # if the comment.user != comment.note.user
        if c.user.pk != c.note.user.pk:
            pn = c.note.user.profile
            pn.reputation += 1
            pn.save()
        # add 1 point to comment.note.reading.user
        # if comment.user != comment.note.reading.user
        if c.user.pk != c.note.reading.user.pk:
            prd = c.note.reading.user.profile
            prd.reputation += 1
            prd.save()
    # if reply
    elif rp:
        prp = rp.user.profile
        # add 1 point to reply.user
        prp.reputation += 1
        prp.save()
        # add 1 point to reply.comment.user
        # if reply.user != reply.comment.user
        if rp.user.pk != rp.comment.user.pk:
            pc = rp.comment.user.profile
            pc.reputation += 1
            pc.save()
        # add 1 point to reply.comment.note.user
        # if reply.user != reply.comment.note.user
        if rp.user.pk != rp.comment.note.user.pk:
            pn = rp.comment.note.user.profile
            pn.reputation += 1
            pn.save()
        # add 1 point to reply.comment.note.reading.user
        # if reply.user != reply.comment.note.reading.user
        if rp.user.pk != rp.comment.note.reading.user.pk:
            prd = rp.comment.note.reading.user.profile
            prd.reputation += 1
            prd.save()
    # if tie
    elif t:
        pt = t.user.profile
        # add 1 point to tie.user
        pt.reputation += 1
        pt.save()
        # add 1 point to tie.tag.user
        # if tie.user != tie.tag.user
        if t.user.pk != t.tag.user.pk:
            ptg = t.tag.user.profile
            ptg.reputation += 1
            ptg.save()
        # add 1 point to tie.reading.user
        # if tie.user != tie.reading.user
        if t.user.pk != t.reading.user.pk:
            prd = t.reading.user.profile
            prd.reputation += 1
            prd.save()
    # if vote
    elif v:
        pv = v.user.profile
        # add 1 point to vote.user
        pv.reputation += 1
        pv.save()
        # add 1 point to vote.note.user
        # if vote.user != vote.note.user
        if v.user.pk != v.note.user.pk:
            pn = v.note.user.profile
            # if upvoted
            if v.value == 1:
                pn.reputation += 1
                pn.save()
        # add 1 point to vote.note.reading.user
        # if vote.user != vote.note.reading.user
        if v.user.pk != v.note.reading.user.pk:
            prd = v.note.reading.user.profile
            # if upvoted
            if v.value == 1:
                prd.reputation += 1
                prd.save()
    # if favorite
    elif fv:
        pfv = fv.reading.user.profile
        # add 1 point to favorite.reading.user
        # if favorite.user != favorite.reading.user
        if fv.user.pk != fv.reading.user.pk:
            pfv.reputation += 1
            pfv.save()
    # if follow
    elif fw:
        pfw = fw.followed.profile
        # add 1 point to follow.followed user
        # if follow.follower != follow.follwed
        if fw.follower.pk != fw.followed.pk:
            pfw.reputation += 1
            pfw.save()
    # if tagfollow
    elif tf:
        ptf = tf.tag.user.profile
        # add 1 point to tagfollow.tag.user
        # if tagfollow.user != tagfollow.tag.user
        if tf.user.pk != tf.tag.user.pk:
            ptf.reputation += 1
            ptf.save()

def del_rep(request, rd=None, n=None, c=None, rp=None, t=None, v=None, 
    fv=None, fw=None, tf=None):
    """Increment reputation points for user(s).
    rd = Reading, n = Note, c = Comment, rp = Reply, 
    t = Tie, v = Vote, fv = Favorite, fw = Follow, tf = TagFollow."""
    # if reading
    if rd:
        prd = rd.user.profile
        # minus 1 point to reading.user
        prd.reputation -= 1
        prd.save()
    # if note
    elif n:
        pn = n.user.profile
        # minus 1 point to note.user
        pn.reputation -= 1
        pn.save()
    # if comment
    elif c:
        pc = c.user.profile
        # minus 1 point to comment.user
        pc.reputation -= 1
        pc.save()
    # if reply
    elif rp:
        prp = rp.user.profile
        # minus 1 point to reply.user
        prp.reputation -= 1
        prp.save()
    # if tie
    elif t:
        pt = t.user.profile
        # minus 1 point to tie.user
        pt.reputation -= 1
        pt.save()
    # if vote
    elif v:
        pv = v.user.profile
        # minus 1 point to vote.user
        pv.reputation -= 1
        pv.save()
    # if favorite
    elif fv:
        pfv = fv.reading.user.profile
        # minus 1 point to favorite.user
        # if favorite.user != favorite.reading.user
        if fv.user.pk != fv.reading.user.pk:
            pfv.reputation -= 1
            pfv.save()
    # if follow
    elif fw:
        pfw = fw.followed.profile
        # minus 1 point to follow.followed
        # if follow.follower != follow.follwed
        if fw.follower.pk != fw.followed.pk:
            pfw.reputation -= 1
            pfw.save()
    # if tagfollow
    elif tf:
        ptf = tf.tag.user.profile
        # minus 1 point to tagfollow.user
        # if tagfollow.user != tagfollow.tag.user
        if tf.user.pk != tf.tag.user.pk:
            ptf.reputation -= 1
            ptf.save()

def create_extra_images(user):
    """Create a small version of original image."""
    img = Image.open('%s%s_orig.jpg' % (settings.MEDIA_IMAGE_ROOT, user.pk))
    # Crop image
    width, height = img.size
    if width > height:
        left = int((width - height)/2.0)
        top = 0
        box = (left, top, left + height, top + height)
        img = img.crop(box)
    elif height > width:
        left = 0
        top = int((height - width)/2.0)
        box = (left, top, left + width, top + width)
        img = img.crop(box)
    # Resize image
    med = img.resize((200, 200), PIL.Image.ANTIALIAS)
    small = img.resize((100, 100), PIL.Image.ANTIALIAS)
    med.save('%s%s' % (settings.MEDIA_IMAGE_ROOT, 
        '%s_med.jpg' % str(user.pk)))
    small.save('%s%s' % (settings.MEDIA_IMAGE_ROOT, 
        '%s_small.jpg' % str(user.pk)))

def remove_images(user):
    """Remove all images for user on the web server."""
    file_list = [f for f in os.listdir(
        settings.MEDIA_IMAGE_ROOT) if f.startswith('%s_' % user.pk)]
    for f in file_list:
        os.remove(settings.MEDIA_IMAGE_ROOT + f)

def rename_image(name, absolute_path):
    """Rename uploaded image, save it into the root folder,
    copy renamed image from the root folder into IMAGE_URL,
    remove renamed image in the root folder"""
    # Rename uploaded image, then save it into the root folder
    os.rename(absolute_path, name)
    # Copy renamed image from root folder into IMAGE_URL
    shutil.copy(name, '%s/%s' % (settings.MEDIA_ROOT, settings.IMAGE_URL))
    # Remove renamed image in the root folder
    os.remove(name)

def resize_orig_image(user):
    """If uploaded image is larger than dimensions, resize it."""
    max_height = 768.0
    max_width = 1024.0
    img = Image.open('%s%s_orig.jpg' % (settings.MEDIA_IMAGE_ROOT, user.pk))
    width, height = img.size
    if width > max_width:
        new_height = height * (max_width/width)
        img = img.resize((int(max_width), int(new_height)), PIL.Image.ANTIALIAS)
    elif height > max_height:
        new_width = width * (max_height/height)
        img = img.resize((int(new_width), int(max_height)), PIL.Image.ANTIALIAS)
    img.save('%s%s' % (settings.MEDIA_IMAGE_ROOT, 
        '%s_orig.jpg' % str(user.pk)))

def s3_delete_file(user):
    """Delete a file uploaded to Amazon s3."""
    s3 = boto.connect_s3(settings.AWS_ACCESS_KEY_ID, 
        settings.AWS_SECRET_ACCESS_KEY)
    bucket = s3.get_bucket(settings.BUCKET_NAME)
    for size in ['orig', 'med', 'small']:
        key = bucket.get_key('media/%s%s/%s_%s.jpg' % (settings.IMAGE_URL,
            user.pk, user.pk, size))
        if key:
            key.delete()

def s3_upload(user):
    """Upload profile image to Amazon S3"""
    s3 = boto.connect_s3(settings.AWS_ACCESS_KEY_ID, 
        settings.AWS_SECRET_ACCESS_KEY)
    bucket = s3.get_bucket(settings.BUCKET_NAME)
    for size in ['orig', 'med', 'small']:
        key = bucket.new_key('media/%s%s/%s_%s.jpg' % (settings.IMAGE_URL,
            user.pk, user.pk, size))
        key.set_contents_from_filename(
            '%s/%s%s_%s.jpg' % (settings.MEDIA_ROOT, 
                settings.IMAGE_URL, user.pk, size))
        key.set_acl('public-read')

def user_exists(slug):
    """Check to see if user exists and return user."""
    user = get_object_or_404(Profile, slug=slug).user
    return user