from django.conf.urls import url

from . import views

app_name = 'core'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^shorten$', views.shorten, name='shorten'),
    url(r'^(?P<token>[a-zA-Z0-9]+)', views.expand, name='expand'),
    url(r'^!(?P<token>[a-zA-Z0-9]+)', views.stats, name='stats'),
]
