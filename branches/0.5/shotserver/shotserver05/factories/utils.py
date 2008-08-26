import random
import base64
from datetime import datetime, timedelta


def last_poll_timeout():
    return datetime.now() - timedelta(minutes=10)


def random_secret_key(length=None):
    if length is None:
        from shotserver05.factories.models import Factory
        length = Factory._meta.get_field('secret_key').max_length
    assert length % 4 == 0
    random_chars = []
    for index in range(length / 4 * 3):
        if index % 23 == 0:
            random.seed()
        random_chars.append(chr(random.randint(0, 255)))
    return base64.b64encode(''.join(random_chars))


def jobs_for_factory(factory):
    q = Q()
    for browser in factory.browser_set.filter(active=True):
        q |= Q(browser_name=browser.name,
               major=browser.major, minor=browser.minor)
