from django.contrib.auth.models import User
from django.db import models


class Link(models.Model):
    url = models.URLField(max_length=255, unique=True)
    token = models.CharField(max_length=32, unique=True)
    views = models.IntegerField(default=0)

    user = models.ForeignKey(User,
                             related_name='links',
                             on_delete=models.CASCADE)

    def __str__(self):
        return u'<Link #{} token={} url={:.40}>'.format(self.id,
                                                        self.token,
                                                        self.url)
