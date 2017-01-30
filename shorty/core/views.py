from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import F
from django.shortcuts import render, redirect, get_object_or_404

from core.models import Link
from core.lib import build_shortener_token
from core.lib import get_random_user_from_db


def index(request):
    # Let's display a warning when DB is not initialized.
    warn_not_initialized = User.objects.count() == 0


    return render(request, 'core/index.html', {
        'warn_not_initialized': warn_not_initialized
    })


def shorten(request):
    # Using raw .POST data: too simple for forms.
    url = request.POST['url']

    try:
        link = Link.objects.filter(url=url).get()

    except Link.DoesNotExist:
        link = Link()
        link.url = url
        link.token = build_shortener_token(url)
        link.user = get_random_user_from_db()
        link.save()

    return render(request, 'core/result.html', {
        'original_url': link.url,
        'shortened_url': '{}/{}'.format(settings.BASE_HOST, link.token)
    })


def expand(request, token):

    # We use an F-expr to do the increment:
    # let the DB do the work, not Python.
    link = get_object_or_404(Link, token=token)
    link.views = F('views') + 1
    link.save()

    return redirect(link.url)


def stats(request, token):
    link = get_object_or_404(Link, token=token)
    return render(request, 'core/stats.html', {
        'link': link
    })
