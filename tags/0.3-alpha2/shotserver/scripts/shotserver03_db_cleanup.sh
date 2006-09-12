#!/bin/sh
echo "DELETE FROM nonce WHERE created < NOW()-'24:00'::interval" | su - www-data psql shotserver03
echo "DELETE FROM request WHERE request IN (SELECT request FROM request JOIN request_group USING (request_group) WHERE created < NOW()-'24:00'::interval AND locked IS NULL)" | su - www-data psql shotserver03
echo "DELETE FROM request_group WHERE created < NOW()-'24:00'::interval AND NOT EXISTS (SELECT request FROM request WHERE request.request_group = request_group.request_group)" | su - www-data psql shotserver03
