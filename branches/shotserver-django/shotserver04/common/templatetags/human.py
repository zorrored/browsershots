from datetime import datetime
from django import template
from django.db import connection

register = template.Library()


@register.filter
def human_seconds(seconds):
    if seconds < 180:
        return "%d s" % seconds
    return "%d min" % (seconds / 60)


@register.filter
def human_timesince(then):
    delta = datetime.now() - then
    return human_seconds(delta.days * 24 * 3600 + delta.seconds)
