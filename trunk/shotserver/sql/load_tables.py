#!/usr/bin/env python

import os
import sys
import commands

PSQL = '/usr/bin/psql'

TABLES = """
auth user
django session site
revenue userdonation userpayment userrevenue
start newsitem
sponsors sponsor
factories factory screensize colordepth screenshotcount
browsers browser
invoices billingaddress
paypal paypallog
websites domain website
priority domainpriority
priority userpriority
screenshots screenshot problemreport
requests requestgroup request
messages factoryerror
""".splitlines()


for line in TABLES:
    models = line.split()
    if not models:
        continue
    app = models.pop(0)
    for model in models:
        table = '%s_%s' % (app, model)
        filename = table + '.modified.sql'
        if not os.path.exists(filename):
            filename = table + '.sql'
        command = PSQL + ' shotserver04'
        command += ' < ' + filename
        print command
        status, output = commands.getstatusoutput(command)
        for out in output.splitlines():
            if ' | ' in out or '-+-' in out:
                continue
            if out.strip() in ('(1 row)', 'DELETE 1'):
                continue
            print output
            sys.exit(1)
        if status:
            print 'error code', status
            sys.exit(status)
