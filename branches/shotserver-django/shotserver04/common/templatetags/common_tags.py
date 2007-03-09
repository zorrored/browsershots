import datetime
from django import template

register = template.Library()

@register.simple_tag
def age(timestamp):
    if not timestamp:
        return ''
    delta = datetime.datetime.now() - timestamp
    seconds = delta.seconds + 24*60*60*delta.days
    if abs(seconds) < 100:
        return '%d seconds' % seconds
    minutes = seconds / 60
    if abs(minutes) < 100:
        return '%d minutes' % minutes
    hours = minutes / 60
    if hours < 100:
        return '%d hours' % hours
    days = hours / 24
    if days < 99:
        return '%d days' % days
    weeks = days / 7
    return '%d weeks' % weeks
