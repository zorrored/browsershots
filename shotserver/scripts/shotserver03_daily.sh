#! /bin/sh
/usr/bin/shotserver03_db_backup.sh
su - www-data /usr/bin/shotserver03_rm_old_png.py
su - www-data /usr/bin/shotserver03_db_cleanup.sh
su - postgres /usr/bin/shotserver03_db_vacuum.sh
