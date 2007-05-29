from django import template
from django.template.defaultfilters import stringfilter


def sqlwrap(value):
    return value.replace('","', '", "')


register = template.Library()
register.filter(stringfilter(sqlwrap))
