from django.db import models
from django.contrib.auth.models import User


class Link(models.Model):

    url = models.CharField(max_length=255, unique=True)
    token = models.CharField(max_length=32, unique=True)
    views = models.IntegerField(default=0)

    user = models.ForeignKey(User,
                             related_name='links',
                             on_delete=models.CASCADE)

    def __unicode__(self):
        return u'<Link #{}>'.format(self.id)
