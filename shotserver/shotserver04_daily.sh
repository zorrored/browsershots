#!/bin/sh
date
echo "Counting yesterday's screenshots..."
sudo -u johann shotserver04_uploads_by_factory.py
date
echo "Dumping database for backup..."
sudo -u postgres pg_dump shotserver04 \
| bzip2 > /backup/shotserver04.`date +%Y-%m-%d`.sql.bz2
date
echo "Deleting old entries from database..."
sudo -u johann psql shotserver04 \
< /home/johann/checkout/shotserver/shotserver04_cleanup.sql
date
