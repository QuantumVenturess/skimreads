from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from readings.models import Reading

class Favorite(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    reading = models.ForeignKey(Reading)
    user = models.ForeignKey(User)

    class Meta:
        unique_together = ('reading', 'user')

    def __unicode__(self):
        return '%s - %s' % (self.user, self.reading)

    def admin_reading(self):
        url = reverse('admin:readings_reading_change', args=(
            self.reading.pk,))
        return '<a href="%s">%s</a>' % (url, self.reading)
    admin_reading.allow_tags = True
    admin_reading.short_description = 'Reading'

    def admin_user(self):
        url = reverse('admin:auth_user_change', args=(self.user.pk,))
        return '<a href="%s">%s</a>' % (url, self.user)
    admin_user.allow_tags = True
    admin_user.short_description = 'User'