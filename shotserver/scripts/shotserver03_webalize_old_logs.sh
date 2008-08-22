#! /bin/sh
DOMAIN=$1
WEBALIZER=/usr/bin/webalizer
DNSCACHE=/var/www/webalizer/dnscache
DNSCHILDREN=10

mkdir -p /var/www/webalizer/$DOMAIN

ls /var/log/apache2/$DOMAIN/access.log.????-??-??.gz | \
xargs -n1 $WEBALIZER \
-p -N $DNSCHILDREN -D $DNSCACHE \
-o /var/www/webalizer/$DOMAIN -n $DOMAIN
