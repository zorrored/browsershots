SELECT * FROM person;
SELECT * FROM os;

SELECT factory_name, os_name, os_manufacturer,
os_distro, os_codename, os_major, os_minor, person_name AS admin_name
FROM factory NATURAL JOIN os_version NATURAL JOIN os NATURAL JOIN person
ORDER BY factory_name;

SELECT factory_name, browser_manufacturer, browser_name, browser_major, browser_minor, terminal, mobile, engine_name
FROM factory_browser NATURAL JOIN factory NATURAL JOIN browser_version NATURAL JOIN browser NATURAL JOIN engine
ORDER BY factory_name;

SELECT * FROM request;
SELECT * FROM browser_stats;

SELECT website_url, factory_name, browser_name
FROM lock NATURAL JOIN request NATURAL JOIN website NATURAL JOIN factory, browser
WHERE browser = request_browser;
