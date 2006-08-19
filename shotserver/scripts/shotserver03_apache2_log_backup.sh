#!/bin/sh
LOGS=/var/log/apache2/
BACKUP=/backup/`hostname`$LOGS
rsync -trv --exclude "*.log" --exclude "*.log.?" $LOGS $BACKUP
