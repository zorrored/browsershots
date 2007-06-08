from datetime import datetime
from django import template

register = template.Library()


@register.filter
def human_seconds(seconds):
    if seconds < 180:
        return "%d s" % seconds
    minutes = seconds / 60
    if minutes < 180:
        return "%d min" % minutes
    hours = minutes / 60
    if hours < 72:
        return "%d h" % hours
    days = hours / 24
    return "%d d" % days


@register.filter
def human_timesince(then):
    delta = datetime.now() - then
    return human_seconds(delta.days * 24 * 3600 + delta.seconds)
