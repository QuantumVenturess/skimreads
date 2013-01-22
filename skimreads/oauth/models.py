from django.contrib.auth.models import User
from django.db import models

class Oauth(models.Model):
    access_token = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    facebook_id = models.BigIntegerField(blank=True, null=True)
    provider = models.CharField(max_length=255)
    user = models.ForeignKey(User)

    class Meta:
        unique_together = ('facebook_id', 'user')

    def __unicode__(self):
        return '%s - %s' % (self.provider, self.user.username)