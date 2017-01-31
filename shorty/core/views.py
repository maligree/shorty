from core.forms import LinkForm
from core.lib import get_unique_shortener_token, get_random_user_from_db
from core.models import Link
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render


def index(request):
    # Just a "landing" endpoint. Hand off to /shorten.
    return redirect('/shorten')


def shorten(request):
    # A warning like this one would nicely fit inside some middleware.
    warn_not_initialized = User.objects.count() == 0

    if request.method == 'GET':
        link_form = LinkForm()
        return render(request, 'core/index.html', {
            'warn_not_initialized': warn_not_initialized,
            'link_form': link_form,
        })

    elif request.method == 'POST':
        link_form = LinkForm(request.POST)

        if link_form.is_valid():
            url = link_form.cleaned_data['url']

            try:
                link = Link.objects.filter(url=url).get()

            except Link.DoesNotExist:
                link = Link()
                link.url = url
                link.token = get_unique_shortener_token()
                link.user = get_random_user_from_db()
                link.save()

            return render(request, 'core/result.html', {
                'original_url': link.url,
                'shortened_url': '{}/{}'.format(settings.BASE_HOST, link.token)
            })

        else:
            # Sorry, errors happened.
            return render(request, 'core/index.html', {
                'warn_not_initialized': warn_not_initialized,
                'link_form': link_form,
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
