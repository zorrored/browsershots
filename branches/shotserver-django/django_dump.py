#!/usr/bin/env python
# django_dump.py - Dump table data from Django models
# Copyright (C) 2007 Johann C. Rocholl <johann@rocholl.net>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Dump table data from Django models.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

import os
import sys
from pprint import pprint


def sql(instance):
    from django.db import backend
    field_names = [backend.quote_name(f.column)
                   for f in instance._meta.fields]
    db_values = []
    for f in instance._meta.fields:
        value = repr(f.get_db_prep_save(f.pre_save(instance, True)))
        if value.startswith("u'"):
            value = value[1:]
        db_values.append(value)
    return 'INSERT INTO %s (%s) VALUES (%s);' % (
        backend.quote_name(instance._meta.db_table),
        ','.join(field_names),
        ','.join(db_values),
        )


def dump(options, model):
    from django.db import backend
    if options.install:
        module = sys.modules[model.__module__]
        dirname = os.path.dirname(os.path.normpath(module.__file__))
        filename = os.path.join(dirname, 'sql',
                                model._meta.module_name + '.sql')
        outfile = open(filename, 'w')
    elif options.source:
        dirname = os.path.join(options.source, model.app_label, 'sql')
        filename = os.path.join(dirname, model._meta.module_name + '.sql')
        outfile = open(filename, 'w')
    else:
        outfile = sys.stdout
    for instance in model.objects.all().order_by('id'):
        outfile.write(sql(instance) + '\n')
    pk_sql = """SELECT setval('%s_id_seq', (SELECT max("id") FROM %s));""" % (
        model._meta.db_table, backend.quote_name(model._meta.db_table))
    outfile.write(pk_sql + '\n')


def dump_by_name(options, model_name):
    from django.db import models
    for app in models.get_apps():
        for model in models.get_models(app):
            if model_name in (model.__name__, model._meta.db_table):
                return dump(options, model)


def _main():
    from optparse import OptionParser
    version = '%prog ' + __revision__.strip('$').replace('Rev: ', 'r')
    usage = '%prog [options] <model> ...'
    parser = OptionParser(version=version, usage=usage,
                          description=__doc__.strip())
    parser.add_option('-p', '--project',
                      help="import models from PROJECT")
    parser.add_option('-i', '--install', action='store_true',
                      help="save custom SQL in installed project")
    parser.add_option('-s', '--source',
                      help="save custom SQL in project source")
    (options, args) = parser.parse_args()
    if not args:
        parser.error("no models specified")
    if options.project:
        os.environ['DJANGO_SETTINGS_MODULE'] = options.project + '.settings'
    for model_name in args:
        dump_by_name(options, model_name)


if __name__ == '__main__':
    _main()
