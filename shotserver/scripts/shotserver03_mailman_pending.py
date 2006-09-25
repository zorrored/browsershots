#! /usr/bin/python


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
    (options, args) = parser.parse_args()

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
            else:
                list_pending(listname, m, options)
        finally:
            m.Unlock()

if __name__ == '__main__':
    _main()
