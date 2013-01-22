from comments.models import Comment
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models

class Reply(models.Model):
    comment = models.ForeignKey(Comment)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)

    class Meta:
        ordering = ['created']
        verbose_name_plural = 'replies'

    def __unicode__(self):
        return self.content

    def admin_comment(self):
        url = reverse('admin:comments_comment_change', 
            args=(self.comment.pk,))
        return '<a href="%s">%s</a>' % (url, self.comment)
    admin_comment.allow_tags = True
    admin_comment.short_description = 'Comment'

    def admin_user(self):
        url = reverse('admin:auth_user_change', args=(self.user.pk,))
        return '<a href="%s">%s</a>' % (url, self.user)
    admin_user.allow_tags = True
    admin_user.short_description = 'User'

    def date_time(self):
        date_time = self.created.strftime('%b %d, %y at %I:%M')
        am_pm = self.created.strftime('%p').lower()
        return date_time + am_pm