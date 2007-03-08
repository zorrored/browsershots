#!/usr/bin/python

import sys
import os
import re
import glob

copy_match = re.compile(r'COPY (\S+) \((.+)\) FROM stdin;').match

old_table_mapping = {
    'screen': 'screensize',
    'bpp': 'bitsperpixel',
    }

new_column_mapping = {
    'browser_id': 'factory_browser',
    'maker': 'manufacturer',
    'admin_id': 'owner',
    'operating_system_id': 'opsys',
    'operating_system_group_id': 'opsys_group',
    'uploads_per_hour': 'per_hour',
    'uploads_per_day': 'per_day',
    'logged': 'created',
    'uploaded': 'created',
    'submitted': 'created',
    'submitter_id': 'creator',
    'bits_per_pixel': 'bpp',
    'javascript': 'js',
    'hashkey': 'nonce',
    'version': 'major.minor',
    }

old_string_remove_null = (
    'manufacturer',
    'distro',
    'codename',
    'js',
    'java',
    'flash',
    'command',
    'engine_version',
    )

table_limits = {
    'request_group': 100,
    'request': 1000,
    'screenshot': 100,
    'nonce': 100,
    }


def guess_new_table(old_table, models):
    if old_table.startswith('factory_'):
        old_table = old_table[len('factory_'):]
    if old_table.startswith('opsys'):
        old_table = 'operatingsystem' + old_table[len('opsys'):]
    old_table = old_table.replace('_', '')
    if old_table in old_table_mapping:
        old_table = old_table_mapping[old_table]
    if old_table in ('feature', 'person', 'prioritydomain', 'failure'):
        return None
    for model in models:
        if model.endswith('_' + old_table):
            return model
    raise ValueError(old_table)


def guess_mapping(old_table, new_table, old_columns, new_columns):
    mapping = []
    for new_column in new_columns:
        old_column = None
        if new_column == 'id' and old_table in old_columns and \
               old_table != 'nonce':
            old_column = old_table
        elif new_column in new_column_mapping and \
                 new_column_mapping[new_column] in old_columns:
            old_column = new_column_mapping[new_column]
        elif old_table == 'opsys' and new_column == 'version':
            old_column = 'major.minor'
        elif new_column in old_columns:
            old_column = new_column
        elif new_column.endswith('_id') and \
                 new_column[:-3] in old_columns:
            old_column = new_column[:-3]
        if old_column:
            mapping.append((old_column, new_column))
    return mapping


def load_columns(model):
    return [field.attname for field in model._meta.fields]


def load_module(appname):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'shotserver04.settings'
    module_name = 'shotserver04.%s.models' % appname
    module = __import__(module_name, globals(), locals(), [''])
    models = {}
    for name, model in module.__dict__.iteritems():
        if not repr(model).startswith("<class '%s." % module_name):
            continue
        table_name = appname + '_' + name.lower()
        models[table_name] = load_columns(model)
    return models


def load_models():
    models = {}
    from shotserver04 import settings
    for app in settings.INSTALLED_APPS:
        if app.startswith('shotserver04.'):
            appname = app.split('.')[1]
            models.update(load_module(appname))
    return models


def split_column_names(text):
    result = text.split(', ')
    for index in range(len(result)):
        if result[index][0] == '"' == result[index][-1]:
            result[index] = result[index][1:-1]
    return result


def convert(old_table, new_table, old_columns, mapping):
    print >> sys.stderr, new_table, "(was %s)" % old_table
    include = []
    new_columns = []
    for old_column, new_column in mapping:
        if old_column == 'major.minor':
            index = (old_columns.index('major'),
                     old_columns.index('minor'))
        else:
            index = old_columns.index(old_column)
        print >> sys.stderr, '   ', new_column, "(was %s at index %s)" % (
            old_column, index)
        include.append(index)
        new_columns.append(new_column)
    if old_table == 'engine':
        new_columns.append('maker')
    for index, column in enumerate(old_columns):
        if index not in include:
            print >> sys.stderr, "        ignoring %s at index %s" % (
                column, index)
    rows = []
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        line = line.rstrip('\n')
        if line == r'\.':
            break
        old_values = line.split('\t')
        assert len(old_values) == len(old_columns)
        new_values = []
        for index in include:
            if isinstance(index, tuple):
                new_value = []
                for i in index:
                    if old_values[i] != r'\N':
                        new_value.append(old_values[i])
                new_value = '.'.join(new_value)
            else:
                old_column = old_columns[index]
                new_value = old_values[index]
                if old_column == 'owner':
                    new_value = '1'
                if old_table == 'factory_browser' and old_column == 'disabled':
                    if new_value == r'\N':
                        new_value = 'f'
                    else:
                        new_value = 't'
                if new_value == r'\N' and \
                       old_column in old_string_remove_null:
                    new_value = ''
            new_values.append(new_value)
        if old_table == 'engine':
            new_values.append('')
        sort_value = new_values[0]
        if sort_value.isdigit():
            sort_value = int(sort_value)
        rows.append((sort_value, '\t'.join(new_values)))
    rows.sort()
    if old_table in table_limits and len(rows) > table_limits[old_table]:
        rows = rows[-table_limits[old_table]:]
    rows.insert(0, (0,
        "COPY %s (%s) FROM stdin;" % (new_table, ', '.join(new_columns))))
    rows.append((0, r'\.'))
    rows.append((0, ''))
    if 'id' in new_columns:
        rows.append((0, ' '.join((
            "SELECT '%s' AS table_name, " % new_table,
            "setval('%s_id_seq'," % new_table,
            "(SELECT max(id) FROM %s)) as pkey_max;" % new_table,
            ))))
    # Write SQL to file
    outfilename = 'sql/%s.sql' % new_table
    outfile = open(outfilename, 'w')
    for sort_value, row in rows:
        outfile.write(row)
        outfile.write('\n')
    outfile.close()


def debug_model(model, columns):
    print model
    for column in columns:
        print '   ', column


def _main(tables):
    models = load_models()
    # for model, columns in models:
    #     debug_model(model, columns)
    converted = 0
    while True:
        line = sys.stdin.readline()
        if line == '':
            break # EOF
        match = copy_match(line)
        if match:
            old_table = match.group(1)
            if tables and old_table not in tables:
                continue
            old_columns = split_column_names(match.group(2))
            new_table = guess_new_table(old_table, models)
            if not new_table:
                print >> sys.stderr, "ignoring table", old_table
                continue
            new_columns = models[new_table]
            mapping = guess_mapping(old_table, new_table,
                                    old_columns, new_columns)
            convert(old_table, new_table, old_columns, mapping)
            if old_table in tables:
                converted += 1
                if converted == len(tables):
                    return


if __name__ == '__main__':
    _main(sys.argv[1:])
