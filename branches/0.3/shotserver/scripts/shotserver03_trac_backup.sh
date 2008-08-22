#!/bin/sh
DB=shotserver03_trac010
BACKUP=/backup/`hostname`/var/lib/postgresql/$DB
DATE=`date +%Y-%m-%d`
su - www-data pg_dump $DB | bzip2 > $BACKUP.$DATE.sql.bz2
