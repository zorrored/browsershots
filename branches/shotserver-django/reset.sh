#!/bin/sh

#######################################################
# WARNING: THIS WILL DROP ALL TABLES IN YOUR DATABASE #
#######################################################

# Run this script as the user www-data (or your database user) after
# changing the database models. If you want to keep your data, use
# pg_dump before you run this script, then reload from the dump file.

APPS="factories browsers websites requests screenshots"

# Drop all tables, with cascade.
python shotserver04/manage.py sqlclear $APPS | \
grep -v CONSTRAINT | sed 's/";/" CASCADE;/' | \
psql shotserver04

# Create all tables from Django models.
python shotserver04/manage.py syncdb $APPS

# Load factories from sql directory
psql shotserver04 < sql/factories_architecture.sql
psql shotserver04 < sql/factories_operatingsystemgroup.sql
psql shotserver04 < sql/factories_operatingsystem.sql
psql shotserver04 < sql/factories_factory.sql
psql shotserver04 < sql/factories_screensize.sql
psql shotserver04 < sql/factories_colordepth.sql

# Load browsers from sql directory
psql shotserver04 < sql/browsers_engine.sql
psql shotserver04 < sql/browsers_browsergroup.sql
psql shotserver04 < sql/browsers_browser.sql

# Load websites from sql directory
psql shotserver04 < sql/websites_website.sql

# Load requests from sql directory
psql shotserver04 < sql/requests_requestgroup.sql
psql shotserver04 < sql/requests_request.sql
