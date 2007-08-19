#!/bin/sh
echo "UPDATE factory SET per_hour = (SELECT COUNT(*) FROM screenshot WHERE screenshot.factory=factory.factory AND screenshot.created>NOW()-'1:00'::interval), per_day = (SELECT COUNT(*) FROM screenshot WHERE screenshot.factory=factory.factory AND screenshot.created>NOW()-'24:00'::interval)" | su - www-data psql shotserver03
