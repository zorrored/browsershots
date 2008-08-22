#! /usr/bin/python
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


from shotserver03 import database as db


def get_last_ticket():
    cur.execute("""\
SELECT id FROM ticket
ORDER BY id DESC
LIMIT 1
""")
    row = cur.fetchone()
    return row[0]


def delete_ticket_changes(ticket):
    cur.execute("""\
DELETE FROM ticket_change
WHERE ticket = %s
""", (ticket, ))


def delete_ticket(ticket):
    cur.execute("""\
DELETE FROM ticket
WHERE id = %s
""", (ticket, ))


def rewind_counter(ticket):
    cur.execute("""\
SELECT setval('ticket_id_seq', %s)
""", (ticket-1, ))


def debug(sql, args):
    print sql, args


db.connect('shotserver03_trac010')
try:
    ticket = get_last_ticket()
    print "deleting ticket", ticket
    # cur.execute = debug
    delete_ticket_changes(ticket)
    delete_ticket(ticket)
    rewind_counter(ticket)
finally:
    db.disconnect()
