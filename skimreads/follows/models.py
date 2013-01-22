from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from tags.models import Tag

class Follow(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    # User.followed_set.all() = where the User is being followed
    # User.follower_set.all() = where the User is the follower
    followed = models.ForeignKey(User, related_name='followed_set')
    follower = models.ForeignKey(User, related_name='follower_set')

    class Meta:
        unique_together = ('followed', 'follower')

    def __unicode__(self):
        return '%s following %s' % (self.follower, self.followed)

    def admin_followed(self):
        url = reverse('admin:auth_user_change', args=(self.followed.pk,))
        return '<a href="%s">%s</a>' % (url, self.followed)
    admin_followed.allow_tags = True
    admin_followed.short_description = 'Followed'

    def admin_follower(self):
        url = reverse('admin:auth_user_change', args=(self.follower.pk,))
        return '<a href="%s">%s</a>' % (url, self.follower)
    admin_follower.allow_tags = True
    admin_follower.short_description = 'Follower'

class TagFollow(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    tag = models.ForeignKey(Tag)
    user = models.ForeignKey(User)

    class Meta:
        unique_together = ('tag', 'user')

    def __unicode__(self):
        return '%s following %s' % (self.user, self.tag)

    def admin_tag(self):
        url = reverse('admin:tags_tag_change', args=(self.tag.pk,))
        return '<a href="%s">%s</a>' % (url, self.tag)
    admin_tag.allow_tags = True
    admin_tag.short_description = 'Tag'

    def admin_user(self):
        url = reverse('admin:auth_user_change', args=(self.user.pk,))
        return '<a href="%s">%s</a>' % (url, self.user)
    admin_user.allow_tags = True
    admin_user.short_description = 'User'