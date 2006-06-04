#!/bin/sh
echo "DELETE FROM nonce WHERE NOW()-created > '1:00'" | sudo su - www-data psql shotserver03
