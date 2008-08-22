# browsershots.org ShotServer 0.3-beta1
# Copyright (C) 2007 Johann C. Rocholl <johann@browsershots.org>
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
Sign up to create a user account.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

import commands
from shotserver03.interface import xhtml


class UnexpectedInput(Exception):
    """Form input had unexpected fields."""
    pass


def title():
    """Page title."""
    return "Create a new user account"


def input_row(fields, key, example, caption=None):
    """
    Write one row in the input form table.
    """
    if caption is None:
        caption = key.capitalize()
    xhtml.write_open_tag('tr')
    xhtml.write_tag('td', caption)
    type_ = 'text'
    if key in ('password', 'repeat'):
        type_ = 'password'
    value = ''
    if key in fields:
        value = fields[key]
    xhtml.write_tag('td', xhtml.tag(
        'input', type_=type_, class_=type_, name_=key, value=value))
    error = key + '_error'
    if error in fields and fields[error]:
        xhtml.write_tag('td', fields[error], class_="error")
    elif key == 'password':
        js = ';'.join((
            "document.getElementById('pwgen').style.display='block'",
            "document.getElementById('click').style.display='none'"))
        link = xhtml.tag('a', "Click here!", onclick=js, id_="click")
        xhtml.write_tag('td', link, class_="gray")
    else:
        xhtml.write_tag('td', example, class_="gray")
    xhtml.write_close_tag_line('tr')


def submit_row(caption=None):
    """
    Write the last row in the input form table,
    with the submit button.
    """
    if caption is None:
        caption = 'Submit'
    xhtml.write_open_tag('tr')
    xhtml.write_tag('td', '')
    xhtml.write_tag('td', xhtml.tag(
        'input', type_="submit", class_="submit", name_="submit",
        value_=caption))
    xhtml.write_close_tag_line('tr')


def write_passwords(columns=8, rows=10):
    """
    Write some random passwords from pwgen.
    """
    count = columns * rows
    command = 'pwgen --numerals --ambiguous --capitalize 8 %d' % count
    passwords = commands.getoutput(command).split()
    if len(passwords) != count:
        return
    xhtml.write_open_tag_line('div', id_="pwgen", style="display:none")
    xhtml.write_tag_line('p',
        "You can use one of these secure random passwords:",
        class_="gray")
    xhtml.write_open_tag_line('table', class_="gray", width="100%")
    for y in range(rows):
        xhtml.write_open_tag('tr')
        for x in range(columns):
            xhtml.write_tag('td', passwords.pop(0))
        xhtml.write_close_tag_line('tr')
    xhtml.write_close_tag_line('table')
    xhtml.write_close_tag_line('div')
    return passwords


def read_form(form):
    """Read input form data."""
    fields = {}
    known_keys = """fullname email username
        fullname_error email_error username_error
        password_error repeat_error""".split()
    for key in known_keys:
        fields[key] = ''
    for key in form.keys():
        if key not in known_keys:
            raise UnexpectedInput(key)
        value = form[key]
        value = value.replace('<', '&lt;')
        value = value.replace('>', '&gt;')
        fields[key] = value
    return fields


def body():
    """
    Write the front page.
    """
    fields = read_form(req.info.form)
    xhtml.write_tag_line('p',
        "Sign up if you want to run a ShotFactory or edit the wiki.")
    xhtml.write_open_tag_line('form', action="newuser", method="post")
    xhtml.write_open_tag_line('table')
    input_row(fields, 'fullname', 'Joe Schmoe', caption='Full name')
    input_row(fields, 'email', 'joe@example.com')
    input_row(fields, 'username', 'joe')
    input_row(fields, 'password', '')
    input_row(fields, 'repeat', '')
    submit_row(caption='Sign me up!')
    xhtml.write_close_tag_line('table')
    xhtml.write_close_tag_line('form')
    write_passwords()
