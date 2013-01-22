from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from readings.models import Reading

class Tag(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=15, unique=True)
    slug = models.SlugField()
    user = models.ForeignKey(User)

    def __unicode__(self):
        return unicode(self.name)

    def admin_user(self):
        url = reverse('admin:auth_user_change', args=(self.user.pk,))
        return '<a href="%s">%s</a>' % (url, self.user)
    admin_user.allow_tags = True
    admin_user.short_description = 'User'

    def followers(self):
        """Return a list of users who are following this tag."""
        ids = [tagfollow.user.pk for tagfollow in self.tagfollow_set.all()]
        users = User.objects.filter(pk__in=ids).order_by('username')
        return users

    def followers_count(self):
        """Return the number of followers for tag."""
        return self.tagfollow_set.all().count()

    def read_count(self):
        """Return the number of readings for tag."""
        return len(self.readings())

    def readings(self):
        """Return all tie readings for tag."""
        ties = Tie.objects.filter(tag=self)
        readings = sorted([tie.reading for tie in ties], 
            key=lambda r: r.month_day_year(), reverse=True)
        return readings

class Tie(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    reading = models.ForeignKey(Reading)
    tag = models.ForeignKey(Tag)
    user = models.ForeignKey(User)

    class Meta:
        ordering = ['tag__name']
        unique_together = ('reading', 'tag')

    def __unicode__(self):
        return unicode(self.tag)

    def admin_reading(self):
        url = reverse('admin:readings_reading_change', args=(
            self.reading.pk,))
        return '<a href="%s">%s</a>' % (url, self.reading)
    admin_reading.allow_tags = True
    admin_reading.short_description = 'Reading'

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