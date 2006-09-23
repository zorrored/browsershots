#! /bin/sh
su - www-data /usr/bin/shotserver03_rm_old_png.py
su - www-data /usr/bin/shotserver03_db_cleanup.sh
