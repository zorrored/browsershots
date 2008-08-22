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


__revision__ = '$Rev$'


import sys
from optparse import OptionParser


sys.path.append('/usr/lib/mailman/')
from Mailman import MailList, Utils, Errors, mm_cfg


def list_pending(listname, m, options):
    messages = m.GetHeldMessageIds()
    if messages:
        print listname
    for message in messages:
        record = m.GetRecord(message)
        print ' ', message, record[1], record[2]


def discard_sender(listname, m, options):
    messages = m.GetHeldMessageIds()
    for message in messages:
        record = m.GetRecord(message)
        sender = record[1]
        if sender.count(options.discard_sender):
            print listname, message, record[1]
            m.HandleRequest(message, mm_cfg.DISCARD)
    m.Save()


def discard_subject(listname, m, options):
    messages = m.GetHeldMessageIds()
    for message in messages:
        record = m.GetRecord(message)
        subject = record[2]
        if subject.count(options.discard_subject):
            print listname, message, record[2]
            m.HandleRequest(message, mm_cfg.DISCARD)
    m.Save()


def _main():
    version = '%prog ' + __revision__.strip('$').replace('Rev: ', 'r')
    parser = OptionParser(version=version)
    parser.set_usage('%prog [options]')
    parser.add_option('--list-messages',
                      action='store_true', default=False,
                      help="""list pending messages for all mailing lists
                              (default action if unspecified)""")
    parser.add_option('--discard-sender',
                      type='string', action='store', metavar='<substring>',
                      help="""discard pending messages where the sender
                              address contains <substring>""")
    parser.add_option('--discard-subject',
                      type='string', action='store', metavar='<substring>',
                      help="""discard pending messages where the subject
                              contains <substring>""")
    (options, args) = parser.parse_args()

    if (options.discard_sender is None and
        options.discard_subject is None):
        options.list_messages = True

    listnames = Utils.list_names()
    listnames.sort()
    for listname in listnames:
        try:
            m = MailList.MailList(listname, lock=True)
        except Errors.MMUnknownListError:
            print >> sys.stderr, 'Unknown list: %s' % listname
            continue
        try:
            if options.discard_sender:
                discard_sender(listname, m, options)
            if options.discard_subject:
                discard_subject(listname, m, options)
            if options.list_messages:
                list_pending(listname, m, options)
        finally:
            m.Unlock()

if __name__ == '__main__':
    _main()
