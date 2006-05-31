#!/bin/sh
ENVIRONMENT=/var/lib/trac/shotserver03

sudo su - www-data trac-admin $ENVIRONMENT permission add johann TRAC_ADMIN

sudo su - www-data trac-admin $ENVIRONMENT component add shotserver johann
sudo su - www-data trac-admin $ENVIRONMENT component add shotfactory johann
sudo su - www-data trac-admin $ENVIRONMENT component remove component1
sudo su - www-data trac-admin $ENVIRONMENT component remove component2

sudo su - www-data trac-admin $ENVIRONMENT severity add blocker
sudo su - www-data trac-admin $ENVIRONMENT severity add critical
sudo su - www-data trac-admin $ENVIRONMENT severity add major
sudo su - www-data trac-admin $ENVIRONMENT severity add normal
sudo su - www-data trac-admin $ENVIRONMENT severity add minor
sudo su - www-data trac-admin $ENVIRONMENT severity add trivial

sudo su - www-data trac-admin $ENVIRONMENT priority remove blocker
sudo su - www-data trac-admin $ENVIRONMENT priority remove critical
sudo su - www-data trac-admin $ENVIRONMENT priority remove major
sudo su - www-data trac-admin $ENVIRONMENT priority remove minor
sudo su - www-data trac-admin $ENVIRONMENT priority remove trivial

sudo su - www-data trac-admin $ENVIRONMENT priority add highest
sudo su - www-data trac-admin $ENVIRONMENT priority add high
sudo su - www-data trac-admin $ENVIRONMENT priority add normal
sudo su - www-data trac-admin $ENVIRONMENT priority add low
sudo su - www-data trac-admin $ENVIRONMENT priority add lowest

sudo su - www-data trac-admin $ENVIRONMENT version add 0.3

sudo su - www-data trac-admin $ENVIRONMENT version remove 1.0
sudo su - www-data trac-admin $ENVIRONMENT version remove 2.0

sudo su - www-data trac-admin $ENVIRONMENT milestone add 0.3-pre1
sudo su - www-data trac-admin $ENVIRONMENT milestone add 0.3.0
sudo su - www-data trac-admin $ENVIRONMENT milestone add 0.3.1

sudo su - www-data trac-admin $ENVIRONMENT milestone remove milestone1
sudo su - www-data trac-admin $ENVIRONMENT milestone remove milestone2
sudo su - www-data trac-admin $ENVIRONMENT milestone remove milestone3
sudo su - www-data trac-admin $ENVIRONMENT milestone remove milestone4
