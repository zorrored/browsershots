#!/bin/sh

#######################################################
# WARNING: THIS WILL DROP ALL TABLES IN YOUR DATABASE #
#######################################################

# Run this script as the user www-data (or your database user) after
# changing the database models. If you want to keep your data, use
# pg_dump before you run this script, then reload from the dump file.

APPS="factories browsers requests"

# Drop all tables, with cascade.
python shotserver04/manage.py sqlclear $APPS | \
grep -v CONSTRAINT | sed 's/";/" CASCADE;/' | \
psql shotserver04

# Create all tables from Django models.
python shotserver04/manage.py syncdb $APPS

# Load data from sql directory
psql shotserver04 < sql/factories_architecture.sql
