#! /bin/sh
echo "DROP DATABASE shotserver03;" | sudo su - postgres psql template1
echo "CREATE DATABASE shotserver03;" | sudo su - postgres psql template1
echo "GRANT ALL PRIVILEGES ON DATABASE shotserver03 TO PUBLIC;" | sudo su - postgres psql shotserver03
