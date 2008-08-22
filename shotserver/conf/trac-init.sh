#!/bin/sh
DATABASE=shotserver03_trac010
ENVIRONMENT=/var/lib/trac/shotserver03

echo "CREATE DATABASE $DATABASE" | sudo su - postgres psql template1
sudo su - www-data trac-admin $ENVIRONMENT initenv \
Browsershots postgres:///$DATABASE svn /var/lib/svn/browsershots /usr/share/trac/templates
