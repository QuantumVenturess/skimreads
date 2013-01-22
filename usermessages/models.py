from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models

class UserMessage(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    recipient = models.ForeignKey(User, related_name='received_messages')
    sender = models.ForeignKey(User, related_name='sent_messages')
    viewed = models.BooleanField(default=False)

    def __unicode__(self):
        return self.content

    def admin_recipient(self):
        url = reverse('admin:auth_user_change', args=(self.recipient.pk,))
        return '<a href="%s">%s</a>' % (url, self.recipient)
    admin_recipient.allow_tags = True
    admin_recipient.short_description = 'Recipient'

    def admin_sender(self):
        url = reverse('admin:auth_user_change', args=(self.sender.pk,))
        return '<a href="%s">%s</a>' % (url, self.sender)
    admin_sender.allow_tags = True
    admin_sender.short_description = 'Sender'

    def date(self):
        return self.created.strftime('%b %d, %y')

    def date_time(self):
        date_time = self.created.strftime('%b %d, %y at %I:%M')
        am_pm = self.created.strftime('%p').lower()
        return date_time + am_pm

    def month_day_year(self):
        return datetime.strptime(self.created.strftime('%m %d %y'), 
            '%m %d %y')

    def time(self):
        time = self.created.strftime('%I:%M').lstrip('0')
        am_pm = self.created.strftime('%p').lower()
        return time + am_pm