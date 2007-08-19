#!/bin/sh
DATABASE=shotserver03_trac010
ENVIRONMENT=/var/lib/trac/shotserver03

echo Are you sure you want to delete the Trac database $DATABASE and the environment $ENVIRONMENT?
read ANSWER
if [ $ANSWER != 'yes' ] ; then exit 1 ; fi

echo "DROP DATABASE $DATABASE" | sudo su - postgres psql template1
sudo rm -rf $ENVIRONMENT
