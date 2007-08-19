#!/bin/sh
# This script must be run as the root database owner, usually postgres.
echo "VACUUM ANALYZE;" | psql shotserver03
echo "VACUUM ANALYZE;" | psql shotserver03_trac010
