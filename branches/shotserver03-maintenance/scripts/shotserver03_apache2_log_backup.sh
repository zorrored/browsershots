#!/bin/sh
LOGS=/var/log/apache2/
BACKUP=/backup/`hostname`$LOGS
shotserver03_log_dates.py $LOGS*.log.?.gz $LOGS*/*.log.?.gz
rsync -tr --exclude "*.log" --exclude "*.log.?" $LOGS $BACKUP
