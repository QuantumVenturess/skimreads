from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify
from readings.utils import set_reading_image, remove_images

import re

class Reading(models.Model):
    title = models.CharField(max_length=80, unique=True)
    link = models.TextField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(User)
    views = models.IntegerField(blank=True, default=0)
    slug = models.SlugField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.title

    def admin_link(self):
        return '<a href="%s" target="_blank">Link</a>' % self.link
    admin_link.allow_tags = True
    admin_link.short_description = 'Link'

    def admin_image(self):
        return '<a href="%s" target="_blank">Link</a>' % self.image
    admin_image.allow_tags = True
    admin_image.short_description = 'Image'

    def admin_user(self):
        url = reverse('admin:auth_user_change', args=(self.user.pk,))
        return '<a href="%s">%s</a>' % (url, self.user)
    admin_user.allow_tags = True
    admin_user.short_description = 'User'

    def activity_count(self):
        """Return number of notes, comments, replies, and votes of reading."""
        a = self.note_count() + self.comment_count()
        b = self.reply_count() + self.vote_count()
        return a + b

    def bullet_notes(self):
        return self.notes()[0:3]

    def bullets(self):
        """Use this for Facebook meta property tag."""
        return ', '.join([n.content for n in self.bullet_notes()])

    def comments(self):
        """Return all comments for each note belonging to reading."""
        from comments.models import Comment
        return Comment.objects.filter(note__reading=self)

    def comment_count(self):
        """Return number of comments for reading."""
        return sum([note.comment_count() for note in self.note_set.all()])

    def date(self):
        return self.created.strftime('%b %d, %y')

    def max_tags(self):
        """Return true if reading has 5 or more ties."""
        if self.tie_set.all().count() >= 5:
            return True

    def month_day_year(self):
        return datetime.strptime(self.created.strftime('%m %d %y'), 
            '%m %d %y')

    def note_count(self):
        """Return the number of notes for reading."""
        return self.note_set.all().count()

    def notes(self):
        """Return the 3 most recent notes."""
        return sorted(self.note_set.all(), 
            key=lambda n: n.vote_value(), reverse=True)

    def pic(self):
        """Return URL for reading's image."""
        if self.image:
            return '%s%s/%s_orig.jpg' % (
                settings.MEDIA_AWS_READ, self.pk, self.pk)
        else:
            return '%simg/readings/default_reading_pic.png' % settings.STATIC_URL

    def reply_count(self):
        """Return number of replies for reading."""
        return sum([note.reply_count() for note in self.note_set.all()])

    def save(self, *args, **kwargs):
        # Newly created object, so set slug
        if not self.id:
            self.slug = slugify(self.title)
        super(Reading, self).save(*args, **kwargs)

    def tags(self):
        """Return all tags for reading."""
        from tags.models import Tag
        ties = [tie.tag.pk for tie in self.tie_set.all()]
        return Tag.objects.filter(pk__in=ties).order_by('name')

    def top_note(self):
        """Return most voted note."""
        notes = self.notes()
        if notes:
            return notes[0]

    def vote_note_count(self):
        """Count the number of votes for each note for reading."""
        return sum([note.vote_count() for note in self.note_set.all()])

    def vote_count(self):
        """Count the number of votes made on reading."""
        return self.vote_set.all().count()

    def vote_value(self):
        """Return the total value of all votes for reading."""
        return sum([vote.value for vote in self.vote_set.all()])

    def weight(self):
        return int(self.views)

def post_save_reading_image(sender, instance, **kwargs):
    """
    Call function to retrieve image, crop, resize, and upload.
    """
    url = instance.image
    if url:
        pattern = re.compile(r'%s_orig\.jpg$' % instance.pk)
        if not re.search(pattern, url):
            set_reading_image(instance, url)

post_save.connect(post_save_reading_image, sender=Reading)

class Note(models.Model):
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    reading = models.ForeignKey(Reading)
    user = models.ForeignKey(User)

    class Meta:
        ordering = ['created']

    def __unicode__(self):
        return unicode('%s' % self.content)

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

    def comment_count(self):
        """Return number of comments."""
        return self.comment_set.all().count()

    def date(self):
        return self.created.strftime('%b %d, %y %I:%M %p')

    def date_time(self):
        date_time = self.created.strftime('%b %d, %y at %I:%M')
        am_pm = self.created.strftime('%p').lower()
        return date_time + am_pm

    def reply_count(self):
        """Return the number of replies for each comment for note."""
        return sum(
            [comment.reply_count() for comment in self.comment_set.all()])

    def vote_count(self):
        """Count the number of votes made on note."""
        return self.vote_set.all().count()

    def vote_value(self):
        """Return the total value of all votes for note."""
        return sum([vote.value for vote in self.vote_set.all()])