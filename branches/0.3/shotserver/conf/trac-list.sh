#!/bin/sh
ENVIRONMENT=/var/lib/trac/shotserver03

sudo su - www-data trac-admin $ENVIRONMENT permission list
sudo su - www-data trac-admin $ENVIRONMENT component list
sudo su - www-data trac-admin $ENVIRONMENT severity list
sudo su - www-data trac-admin $ENVIRONMENT priority list
sudo su - www-data trac-admin $ENVIRONMENT version list
sudo su - www-data trac-admin $ENVIRONMENT milestone list
