import string
from random import choice, randint

from core.models import User, Link
from django.conf import settings


def get_random_user_from_db():
    """
    Returns a random User object from the database.


    To prevent pulling the whole table into memory, we simply
    count first, then query with LIMIT + OFFSET.
    """

    user_count = User.objects.count()
    random_pos = randint(0, user_count - 1)
    random_user = User.objects.all()[random_pos:random_pos + 1].get()
    return random_user


def build_shortener_token():
    """
    Generate a [a-zA-Z0-9] token to represent the shortened URL.

    The length of the token is random, based on the bounds specified
    in SHORT_URL_LENGTH_BOUNDS in the app settings.
    """

    min_len, max_len = settings.SHORT_URL_LENGTH_BOUNDS
    pool = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return ''.join(choice(pool) for _ in range(randint(min_len, max_len)))


def get_unique_shortener_token(retry=5):
    """
    Calls build_shortener_token up to `retry` times to guarantee a unique token.

    This isn't ideal, but given the way we generate tokens it's necessary.
    IDEALLY we'd either use a different algorithm tied to the URL passed
    e.g. the base 36 method which is pretty common.

    For really big traffic, we'd need a separate service to keep a pool
    of unique, ready-to-use IDs.
    """

    # Let's do this without any external modules (e.g. retry, retrying)
    while True:
        token = build_shortener_token()
        if Link.objects.filter(token=token).count() == 0:
            break

    return token
