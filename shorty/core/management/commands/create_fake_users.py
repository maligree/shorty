import requests
from django.contrib.auth.models import User
from django.core.management import BaseCommand

URL = 'https://randomuser.me/api/'


def build_url(n):
    return '{}?results={}'.format(URL, n)


class Command(BaseCommand):
    help = "Populate the database with N fake (but believable) users."

    def add_arguments(self, parser):
        parser.add_argument('user_count', nargs=1, type=int)

    def handle(self, *args, **options):
        user_count = options['user_count'][0]  # TODO: Why?
        response = requests.get(build_url(user_count))

        for random_user in response.json()['results']:
            # If this was a critical piece, we'd use bulk_create(),
            # but since create_user() does a bit behind the scenes
            # we'll stick to a loop here.
            User.objects.create_user(
                random_user['login']['username'],
                random_user['email'],
                random_user['login']['password'],
                first_name=random_user['name']['first'],
                last_name=random_user['name']['last'],
                date_joined=random_user['registered'])
