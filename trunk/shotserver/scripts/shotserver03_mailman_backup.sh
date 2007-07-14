#!/bin/sh
ARCHIVES=/var/lib/mailman/archives/private
BACKUP=/backup/`hostname`$ARCHIVES.`date +%Y-%m-%d`.tar.bz2
tar -cjPf $BACKUP $ARCHIVES
