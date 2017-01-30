import string

from django.conf import settings

from random import randint
from random import choice


from core.models import User


def get_random_user_from_db():
    # Count first, then LIMIT + OFFSET so we
    # don't actually pull the whole table into memory.
    user_count = User.objects.count()
    random_pos = randint(0, user_count - 1)
    random_user = User.objects.all()[random_pos:random_pos+1].get()
    return random_user


def build_shortener_token(url):
    min_len, max_len = settings.SHORT_URL_LENGTH_BOUNDS
    pool = string.ascii_uppercase + string.digits
    return ''.join(choice(pool) for _ in range(randint(min_len, max_len)))
