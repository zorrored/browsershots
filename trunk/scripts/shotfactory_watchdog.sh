#!/bin/sh
# Restart screenshot factories when they die, or after reboot.
#
# Add me to /etc/crontab like this (make sure I'm on the PATH):
# * *   * * *   shotfactory1   shotfactory_watchdog.sh <password>
# * *   * * *   shotfactory2   shotfactory_watchdog.sh <password>
# * *   * * *   shotfactory3   shotfactory_watchdog.sh <password>
#
# The load limit for each factory will be set to the factory index
# (the number at the end of the username). So shotfactory1 will take a
# break if the load average is above 1, shotfactory2 will continue to
# work until the load average is above 2, shotfactory3 until load 3.
PASSWORD=$1
USER=`whoami`
INDEX=`whoami | sed s/shotfactory//`

# Check if screen is already running.
ps -u $USER | grep screen > /dev/null && exit 0

# Send email to administrator, including previous output.
echo shotfactory_watchdog.sh:
echo Restarting shotfactory for $USER.
echo
echo Previous output in screenlog.0:
echo ...
tail -n30 /home/$USER/checkout/shotfactory/screenlog.0

# VNC server requires $USER environment variable.
export USER

# Change directory.
cd /home/$USER/checkout/shotfactory

# Start screen (detached, with logging).
# Set the display (-d) and load limit (-l) to the factory index.
screen -d -m -L python shotfactory.py -p $PASSWORD -d :$INDEX -l $INDEX
