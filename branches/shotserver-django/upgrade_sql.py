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
    'browser': 'factory_browser',
    'maker': 'manufacturer',
    'admin': 'owner',
    'operating_system': 'opsys',
    'operating_system_group': 'opsys_group',
    'uploads_per_hour': 'per_hour',
    'uploads_per_day': 'per_day',
    'logged': 'created',
    'uploaded': 'created',
    'submitted': 'created',
    'submitted_by': 'creator',
    'bits_per_pixel': 'bpp',
    'javascript': 'js',
    }


def guess_new_table(old_table, models):
    if old_table.startswith('factory_'):
        old_table = old_table[len('factory_'):]
    if old_table.startswith('opsys'):
        old_table = 'operatingsystem' + old_table[len('opsys'):]
    old_table = old_table.replace('_', '')
    if old_table in old_table_mapping:
        old_table = old_table_mapping[old_table]
    if old_table in ('feature', 'person', 'prioritydomain'):
        return None
    for model in models:
        if model.endswith('_' + old_table):
            return model
    raise ValueError(old_table)


def guess_mapping(old_table, new_table, old_columns, new_columns):
    mapping = []
    for new_column in new_columns:
        old_column = None
        if new_column == 'id' and old_table in old_columns:
            old_column = old_table
        elif new_column in new_column_mapping and \
                 new_column_mapping[new_column] in old_columns:
            old_column = new_column_mapping[new_column]
        elif new_column in old_columns:
            old_column = new_column
        if old_column:
            mapping.append((old_column, new_column))
    return mapping


def load_columns(model):
    return [field.name for field in models._meta.fields]


def load_module(appname):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'shotserver04.settings'
    module = __import__('shotserver04.%s.models' % appname,
                        globals(), locals(), [''])
    models = {}
    for name, model in module.__dict__.iteritems():
        if not repr(model).startswith("<class '%s.models.'" % appname):
            continue
        table_name = appname + '_' + name.lower()
        models[table_name] = load_model_columns(model)
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


def change_pair(mapping, old_column, new_column):
    for index in range(len(mapping) - 1, 0, -1):
        if mapping[index][0] == old_column:
            mapping[index] == (old_column, new_column)


def remove_pair(mapping, old_column):
    for index in range(len(mapping) - 1, 0, -1):
        if mapping[index][0] == old_column:
            del mapping[index]


def convert(old_table, new_table, old_columns, mapping):
    print >> sys.stderr, new_table, "(was %s)" % old_table
    include = []
    for old_column, new_column in mapping:
        index = old_columns.index(old_column)
        print >> sys.stderr, '   ', new_column, "(was %s at index %d)" % (
            old_column, index)
        include.append(index)
    for index, column in enumerate(old_columns):
        if index not in include:
            print >> sys.stderr, "        ignoring %s at index %d" % (
                column, index)


def debug_model(model, columns):
    print model
    for column in columns:
        print '   ', column


def _main():
    models = load_models()
    # for model, columns in models:
    #     debug_model(model, columns)
    while True:
        line = sys.stdin.readline()
        if line == '':
            break # EOF
        match = copy_match(line)
        if match:
            old_table = match.group(1)
            old_columns = split_column_names(match.group(2))
            new_table = guess_new_table(old_table, models)
            if not new_table:
                print >> sys.stderr, "ignoring table", old_table
                continue
            new_columns = models[new_table]
            mapping = guess_mapping(old_table, new_table,
                                    old_columns, new_columns)
            convert(old_table, new_table, old_columns, mapping)


if __name__ == '__main__':
    _main()
