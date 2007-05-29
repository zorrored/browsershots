from django import template

register = template.Library()


@register.filter
def sqlwrap(value):
    return value.replace('","', '", "')
