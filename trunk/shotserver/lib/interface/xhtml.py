# browsershots.org
# Copyright (C) 2006 Johann C. Rocholl <johann@browsershots.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston,
# MA 02111-1307, USA.

"""
XHTML formatting and output.

>>> print open_tag('a', href = '/'),
<a href="/">

>>> print close_tag('a'),
</a>
"""

__revision__ = '$Rev: 882 $'
__date__     = '$Date: 2005-12-31 15:20:50 +0100 (Sa, 31 Dez 2005) $'
__author__   = '$Author: johann $'

open_tags = []
class ClosingTagMismatch(Exception):
    """
    Last opened tag does not match closing tag name.
    """
    pass

def attribute_string(**attributes):
    """
    Make a XHTML attribute string for an opening tag.

    >>> print attribute_string(),

    >>> print attribute_string(_id="foo", _class="bar", href="/"),
     class="bar" id="foo" href="/"
    """
    result = []
    keys = attributes.keys()
    keys.sort()
    for key in keys:
        value = attributes[key]
        result.append('%s="%s"' % (key.strip('_'), value))
    if result:
        result.insert(0, '')
    return ' '.join(result)

def open_tag(name, **attributes):
    """
    Make an opening tag.
    """
    global open_tags
    open_tags.append(name)
    attr = attribute_string(**attributes)
    return '<%s%s>' % (name, attr)

def close_tag(name = None):
    """
    Make a closing tag.
    """
    global open_tags
    innermost = open_tags.pop(-1)
    if name is not None and name != innermost:
        open_tags.append(innermost)
        raise ClosingTagMismatch("%s != %s" % (name, innermost))
    return '</%s>' % innermost

def tag(name, data = None, **attributes):
    """
    >>> print tag('p', 'Test'),
    <p>Test</p>

    >>> print tag('a', 'Test', href = '/', _class = 'local'),
    <a class="local" href="/">Test</a>
    """
    attr = attribute_string(**attributes)
    if data is None:
        return '<%s%s />' % (name, attr)
    else:
        return '<%s%s>%s</%s>' % (name, attr, data, name)

def tag_line(name, data = None, **attributes):
    """
    >>> print tag_line('br'),
    <br />
    """
    return tag(name, data, **attributes) + '\n'

def multiline_tag(name, data = None, **attributes):
    """
    >>> print multiline_tag('ul', tag_line('li', 'test'), _class="test"),
    <ul class="test">
    <li>test</li>
    </ul>
    """
    return tag_line(name, '\n' + data, **attributes)

def text_to_xhtml(text):
    """
    Convert possibly many lines of text to XHTML.

    >>> print text_to_xhtml('example\\na < b'),
    example<br />
    a &lt; b
    """
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('\n', '<br />\n')
    return text

write_open_tag = lambda *args, **attr: req.write(open_tag(*args, **attr))
write_open_tag_line = lambda *args, **attr: req.write(open_tag(*args, **attr) + '\n')
write_close_tag = lambda *args: req.write(close_tag(*args))
write_close_tag_line = lambda *args: req.write(close_tag(*args) + '\n')
write_tag_line = lambda *args, **attr: req.write(tag_line(*args, **attr))
write_tag = lambda *args, **attr: req.write(tag(*args, **attr))

def _test():
    """
    Run doctest on this module.
    """
    import doctest
    import xhtml
    return doctest.testmod(xhtml)

if __name__ == '__main__':
    _test()
