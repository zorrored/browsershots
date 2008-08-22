#!/bin/sh
echo 'DROP DATABASE shotserver03' | sudo su - postgres psql template1
echo 'DROP USER "www-data"' | sudo su - postgres psql template1
echo 'CREATE USER "www-data"' | sudo su - postgres psql template1
echo 'CREATE DATABASE shotserver03' | sudo su - postgres psql template1
echo 'GRANT ALL PRIVILEGES ON DATABASE shotserver03 TO "www-data"' | sudo su - postgres psql shotserver03
cat sql/create_tables.sql | sudo su - www-data psql shotserver03
