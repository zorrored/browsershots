#!/usr/bin/env python

import os
import sys
import commands

TABLES = """
auth user
django session site
sponsors sponsor
factories factory screensize colordepth screenshotcount
browsers browser
invoices billingaddress
paypal paypallog
websites domain website
priority domainpriority
priority userpriority
requests requestgroup request
revenue nonprofit userdonation userpayment userrevenue
screenshots screenshot problemreport
messages factoryerror
start newsitem
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
        command = '/opt/local/lib/postgresql83/bin/psql shotserver04'
        command += ' < ' + filename
        print command
        status, output = commands.getstatusoutput(command)
        if status:
            print 'error code', result
            sys.exit(result)
        for out in output.splitlines():
            if ' | ' in out or '-+-' in out:
                continue
            if out.strip() in ('(1 row)', 'DELETE 1'):
                continue
            print output
            sys.exit(1)
