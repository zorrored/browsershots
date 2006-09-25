#! /usr/bin/python


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
