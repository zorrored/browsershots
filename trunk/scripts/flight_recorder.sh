#!/bin/sh
# Copy or symlink this file to /usr/local/bin/
# and add the following line to /etc/crontab:
# * *     * * *   root    flight_recorder.sh
DATE=`date +%H%M`
LOGDIR=/var/log/flight
mkdir -p $LOGDIR
COLUMNS=160 top -cbn1 > $LOGDIR/top-$DATE.log
