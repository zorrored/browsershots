from django.utils.translation import ugettext as _
from django.http import HttpResponseRedirect
from django.utils.text import capfirst


def redirect(url, result=None, id=None, fragment=None):
    if hasattr(url, 'get_absolute_url'):
        url = url.get_absolute_url()
    if result is not None:
        url += '?result=' + result
        if hasattr(id, 'id'):
            url += '_%d' % id.id
        elif id is not None:
            url += '_' + unicode(id)
    if fragment is not None:
        url += '#' + fragment
    return HttpResponseRedirect(url)


def filter(items, func):
    if isinstance(func, int):
        id = func
        func = lambda item: item.id == id
    elif isinstance(func, basestring):
        text = func
        func = lambda item: unicode(item) == text
    for item in items:
        if func(item):
            return item


def message(result, id=None):
    parts = result.split('_')
    action = parts.pop(0)
    if id is None:
        id = parts.pop(-1)
    else:
        parts.pop(-1)
        id = unicode(id)
    item = _(' '.join(parts))
    if action == 'added':
        return _("Added %(item)s %(id)s.") % locals()
    elif action == 'removed':
        return _("Removed %(item)s %(id)s.") % locals()
    elif action == 'updated':
        return _("Updated %(item)s %(id)s.") % locals()
    return "%s %s %s." % (capfirst(action), item, id)
