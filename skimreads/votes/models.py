from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from readings.models import Note

class Vote(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    note = models.ForeignKey(Note)
    user = models.ForeignKey(User)
    value = models.IntegerField()

    class Meta:
        unique_together = ('note', 'user')

    def __unicode__(self):
        return '%s: %s' % (self.note, str(self.value))

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