#! /bin/sh

BACKUP=/backup/`hostname`/var/lib/svn/browsershots
svn_backup.py $FULL /var/lib/svn/browsershots $BACKUP

BACKUP=/backup/`hostname`/var/lib/svn/etc
svn_backup.py $FULL /var/lib/svn/etc $BACKUP
