import string
from random import choice, randint

from core.models import User
from django.conf import settings


def get_random_user_from_db():
    """
    Returns a random User object from the database.


    To prevent pulling the whole table into memory, we simply
    count first, then query with LIMIT + OFFSET.
    """

    user_count = User.objects.count()
    random_pos = randint(0, user_count - 1)
    random_user = User.objects.all()[random_pos:random_pos+1].get()
    return random_user


def build_shortener_token(url):
    """
    Generate a [a-zA-Z0-9] token to represent the shortened URL.

    The length of the token is random, based on the bounds specified
    in SHORT_URL_LENGTH_BOUNDS in the app settings.
    """

    min_len, max_len = settings.SHORT_URL_LENGTH_BOUNDS
    pool = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return ''.join(choice(pool) for _ in range(randint(min_len, max_len)))
