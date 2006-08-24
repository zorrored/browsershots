#!/bin/sh
echo "DELETE FROM nonce WHERE created < NOW()-'24:00'::interval" | su - www-data psql shotserver03
