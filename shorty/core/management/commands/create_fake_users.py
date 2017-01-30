import requests

from django.core.management import BaseCommand
from django.contrib.auth.models import User

from django.db import connection

URL = 'https://randomuser.me/api/'


# todo: progressbar via tqdm

def build_url(n):
    return '{}?results={}'.format(URL, n)

# todo: /Users/maligree/shorty/VENV/lib/python3.6/site-packages/django/db/models/fields/__init__.py:1430: RuntimeWarning: DateTimeField User.date_joined received a naive datetime (2005-11-05 04:07:05) while time zone support is active.


class Command(BaseCommand):
    help = "Populate the database with N fake (but believable) users."

    def add_arguments(self, parser):
        parser.add_argument('user_count', nargs=1, type=int)

    def handle(self, *args, **options):
        user_count = options['user_count'][0]  # TODO: Why?
        response = requests.get(build_url(user_count))

        for random_user in response.json()['results']:
            user = User.objects.create_user(
                random_user['login']['username'],
                random_user['email'],
                random_user['login']['password'],
                first_name=random_user['name']['first'],
                last_name=random_user['name']['last'],
                date_joined=random_user['registered'])


        print(connection.queries)
