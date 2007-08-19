#!/bin/sh
# This script must be run as the database owner, usually www-data.
echo "DELETE FROM nonce WHERE created < NOW()-'24:00'::interval" | psql shotserver03
echo "DELETE FROM request WHERE request IN (SELECT request FROM request JOIN request_group USING (request_group) WHERE created < NOW()-'24:00'::interval AND locked IS NULL)" | psql shotserver03
echo "DELETE FROM request_group WHERE created < NOW()-'24:00'::interval AND NOT EXISTS (SELECT request FROM request WHERE request.request_group = request_group.request_group)" | psql shotserver03
echo "DELETE FROM website WHERE created < NOW()-'24:00'::interval AND NOT EXISTS (SELECT request_group FROM request_group WHERE website = website.website)" | psql shotserver03
