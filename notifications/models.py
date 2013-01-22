from comments.models import Comment
from django.contrib.auth.models import User
from django.db import models
from follows.models import Follow
from readings.models import Note
from replies.models import Reply
from tags.models import Tie
from votes.models import Vote

class Notification(models.Model):
    comment = models.ForeignKey(Comment, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    follow = models.ForeignKey(Follow, blank=True, null=True)
    note = models.ForeignKey(Note, blank=True, null=True)
    reply = models.ForeignKey(Reply, blank=True, null=True)
    tie = models.ForeignKey(Tie, blank=True, null=True)
    viewed = models.BooleanField(default=False)
    vote = models.ForeignKey(Vote, blank=True, null=True)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return '%s %s' % (self.user.username, self.date_time())

    def date(self):
        return self.created.strftime('%b %d, %y')

    def date_time(self):
        date_time = self.created.strftime('%b %d, %y at %I:%M')
        am_pm = self.created.strftime('%p').lower()
        return date_time + am_pm

    def follower(self):
        return self.follow.follower

    def time(self):
        time = self.created.strftime('%I:%M').lstrip('0')
        am_pm = self.created.strftime('%p').lower()
        return time + am_pm