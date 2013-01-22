from collections import defaultdict
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify
from follows.models import Follow
from itertools import chain, groupby
from readings.models import Reading
from readings.utils import reading_sort

# User email unique (no need for Django >= 1.5)
User._meta.get_field('email')._unique = True

class Profile(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(blank=True, null=True, 
        upload_to=settings.IMAGE_URL)
    reputation = models.IntegerField(default=0)
    user = models.ForeignKey(User, unique=True)
    slug = models.SlugField(blank=True, null=True, unique=True)

#    def save(self, *args, **kwargs):
#        self.slug = slugify(User.objects.get(pk=self.user.pk).username)
#        super(Profile, self).save(*args, **kwargs)

    def __unicode__(self):
        return unicode(self.user)

    def admin_image(self):
        return '<a href="%s" target="_blank">Image</a>' % self.orig()
    admin_image.allow_tags = True
    admin_image.short_description = 'Image'

    def admin_user(self):
        url = reverse('admin:auth_user_change', args=(self.user.pk,))
        return '<a href="%s">%s</a>' % (url, self.user)
    admin_user.allow_tags = True
    admin_user.short_description = 'User'

    def comment_count(self):
        """Return the number of comments for a user."""
        return self.user.comment_set.all().count()

    def comment_reply_count(self):
        return self.comment_count() + self.reply_count()

    def facebook_auth(self):
        """Check to see if user has a facebook oauth."""
        try:
            oauth = self.user.oauth_set.get(provider='facebook')
            return True
        except ObjectDoesNotExist:
            return False

    def favorite_count(self):
        """Count the number of faved readings."""
        return self.user.favorite_set.all().count()

    def followers(self):
        """Return all users who are followers of self.user."""
        ids = [follow.follower.pk for follow in self.user.followed_set.all()]
        users = User.objects.filter(pk__in=ids).order_by('username')
        return users

    def following(self):
        """ Return all users who self.user is following."""
        ids = [follow.followed.pk for follow in self.user.follower_set.all()]
        users = User.objects.filter(pk__in=ids).order_by('username')
        return users

    def followers_count(self):
        return self.user.followed_set.all().count()

    def following_count(self):
        return self.user.follower_set.all().count()

    def note_count(self):
        return self.user.note_set.all().count()

    def is_following(self, user):
        """Check to see if current user is being followed by user."""
        follow = self.user.follower_set.filter(followed=user)
        if follow:
            return True

    def med(self):
        oauth = self.user.oauth_set.all()
        if self.image:
            return '%s%s/%s_med.jpg' % (
                settings.MEDIA_AWS, self.user.pk, self.user.pk)
        elif oauth:
            return 'http://graph.facebook.com/%s/picture?type=large' % (
                oauth[0].facebook_id)
        else:
            return '%s%sdefault_med.jpg' % (settings.STATIC_URL, 
                settings.IMAGE_URL)

    def message_count(self):
        """Return the total number of received messages."""
        return self.user.received_messages.all().count()

    def notice_count(self):
        """Count the number of unviewed notifications."""
        return self.user.notification_set.filter(viewed=False).count()

    def orig(self):
        oauth = self.user.oauth_set.all()
        if self.image:
            return '%s%s/%s_orig.jpg' % (
                settings.MEDIA_AWS, self.user.pk, self.user.pk)
        elif oauth:
            return 'http://graph.facebook.com/%s/picture?type=large' % (
                oauth[0].facebook_id)
        else:
            return '%s%sdefault_orig.jpg' % (settings.STATIC_URL, 
                settings.IMAGE_URL)

    def read_count(self):
        """Return the number of readings for a user."""
        return self.user.reading_set.all().count()

    def read_feed(self):
        """Return readings for followed topics and users."""
        # Use chain to concatenate querysets
        li = self.topic_follow_feed() + list(self.user_follow_feed())
        return sorted(li, key=reading_sort(), reverse=True)

    def recent_messages(self):
        """Return a list of the most recent messages."""
        messages = []
        user_messages = defaultdict(list)
        for msg in self.user.received_messages.all():
            user_messages[msg.sender].append(msg)
        for user, msgs in user_messages.iteritems():
            most_recent = sorted(msgs, key=lambda m: m.created, reverse=True)[0]
            messages.append(most_recent)
        return sorted(messages, key=lambda m: m.created, reverse=True)

    def recent_messages_group_by(self):
        """Return a list of the most recent messages."""
        received_messages = self.user.received_messages.all()
        messages = []
        for user, msgs in groupby(received_messages, lambda m: m.sender):
            most_recent = sorted(msgs, key=lambda m: m.created, reverse=True)[0]
            messages.append(most_recent)
        return sorted(messages, key=lambda m: m.created, reverse=True)

    def reply_count(self):
        return self.user.reply_set.all().count()

    def small(self):
        oauth = self.user.oauth_set.all()
        if self.image:
            return '%s%s/%s_small.jpg' % (
                settings.MEDIA_AWS, self.user.pk, self.user.pk)
        elif oauth:
            return 'http://graph.facebook.com/%s/picture' % (
                oauth[0].facebook_id)
        else:
            return '%s%sdefault_small.jpg' % (settings.STATIC_URL, 
                settings.IMAGE_URL)

    def title_count(self):
        """Count notifications and unread messages."""
        return self.notice_count() + self.unread_message_count()

    def topics(self):
        """Return list of tags user is following."""
        tags = [tagfollow.tag for tagfollow in self.user.tagfollow_set.all()]
        return sorted(tags, key=lambda t: t.name)

    def topic_count(self):
        """Count how many tags user is following."""
        return len(self.topics())

    def topic_follow_feed(self):
        """Return a list of readings from followed topics."""
        readings = []
        for tag in self.topics():
            for reading in tag.readings():
                readings.append(reading)
        return readings

    def tie_count(self):
        """Count how many ties a current user made."""
        return self.user.tie_set.all().count()

    def unread_message_count(self):
        """Count the number of unread messages."""
        return self.user.received_messages.filter(viewed=False).count()

    def user_follow_feed(self):
        """Return a list of readings from followed users."""
        ids = [follow.followed.pk for follow in self.user.follower_set.all()]
        return Reading.objects.filter(user__pk__in=ids)

    def vote_count(self):
        """Count how many votes the current user has."""
        return self.user.vote_set.all().count()

def create_profile(sender, instance, **kwargs):
    try:
        profile = Profile.objects.get(user=instance)
        profile.slug = slugify(instance.username)
        profile.save()
    except ObjectDoesNotExist:
        Profile.objects.create(user=instance, slug=slugify(instance.username))

post_save.connect(create_profile, sender=User)

User.profile = property(lambda u: u.profile_set.all()[0])