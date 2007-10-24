#!/bin/sh
if [ -z "$1" ]; then echo usage: clone_user.sh user1 user2; exit 1; fi
if [ -z "$2" ]; then echo usage: clone_user.sh user1 user2; exit 1; fi
if [ ! -d "/home/$1" ]; then echo /home/$1 does not exist; exit 1; fi
if [ -d "/home/$2" ]; then echo /home/$2 already exists; exit 1; fi
echo copying home directory from $1 to $2
cp -a /home/$1 /home/$2
find /home/$2 -name "*.pyc" | xargs -r rm
find /home/$2 -name "screenlog.*" | xargs -r rm
find /home/$2 -name "pg????.ppm" | xargs -r rm
rm -f /home/$2/.mozilla/firefox/*/history.dat
rm -f /home/$2/.mozilla/firefox/*/secmod.db
rm -f /home/$2/.mozilla/firefox/*/lock
rm -rf /home/$2/.opera/images
rm -rf /home/$2/.kde/socket-*
rm -f /home/$2/.kde/cache-*
rm -f /home/$2/.kde/tmp-*
rm -f /home/$2/.DCOPserver*
rm -f /home/$2/.vnc/*.log
rm -f /home/$2/.vnc/*.pid
sed -i s/$1/$2/ /home/$2/.opera/opera6.ini
sed -i s/$1/$2/ /home/$2/.opera/mail/*.ini
sed -i s/$1/$2/ /home/$2/.emacs-places
chown -R $2:$2 /home/$2
