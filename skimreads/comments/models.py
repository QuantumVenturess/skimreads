from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from readings.models import Note

class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    note = models.ForeignKey(Note)
    user = models.ForeignKey(User)

    class Meta:
        ordering = ['created']

    def __unicode__(self):
        return self.content

    def admin_note(self):
        url = reverse('admin:readings_note_change', args=(self.note.pk,))
        return '<a href="%s">%s</a>' % (url, self.note)
    admin_note.allow_tags = True
    admin_note.short_description = 'Note'

    def admin_user(self):
        url = reverse('admin:auth_user_change', args=(self.user.pk,))
        return '<a href="%s">%s</a>' % (url, self.user)
    admin_user.allow_tags = True
    admin_user.short_description = 'User'

    def date_time(self):
        date_time = self.created.strftime('%b %d, %y at %I:%M')
        am_pm = self.created.strftime('%p').lower()
        return date_time + am_pm

    def reply_count(self):
        return self.reply_set.all().count()
    reply_count.short_description = 'Replies'