#!/bin/sh
ARCHIVES=/var/lib/mailman/archives/private/
BACKUP=/backup/`hostname`$ARCHIVES
rsync -trL $ARCHIVES $BACKUP
