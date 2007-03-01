#!/bin/sh
#######################################################
# WARNING: THIS WILL DROP ALL TABLES IN YOUR DATABASE #
#######################################################
# Run this script as the user www-data (or your database user).

# Drop all tables (note reverse app ordering).
python manage.py sqlclear screenshots requests browsers factories | psql shotserver04

# Create all tables from Django models.
python manage.py syncdb factories browsers requests screenshots

# Load some database content from demo.sql for testing.
psql shotserver04 < demo.sql
