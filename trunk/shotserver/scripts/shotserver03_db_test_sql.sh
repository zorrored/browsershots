#!/bin/sh
cat sql/create_tables.sql | sudo su - www-data psql shotserver03 2>&1 | grep -v NOTICE
cat sql/create_views.sql | sudo su - www-data psql shotserver03 2>&1 | grep -v NOTICE
cat sql/test_insert.sql | sudo su - www-data psql shotserver03 2>&1 | grep -v NOTICE | grep -v INSERT
# cat sql/test_select.sql | sudo su - www-data psql shotserver03
