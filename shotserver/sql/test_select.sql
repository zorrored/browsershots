SELECT * FROM person;

SELECT name, major, minor, manufacturer, terminal
FROM browser JOIN browser_version USING (browser)
ORDER BY name;

SELECT DISTINCT name, major, minor, manufacturer, mobile
FROM os JOIN os_version USING (os)
ORDER BY name;

SELECT factory.name,
os.name, os.manufacturer,
os_version.distro, os_version.codename, os_version.major, os_version.minor,
person.name
FROM factory
JOIN person ON factory.creator = person.person
JOIN os_version USING (os_version)
JOIN os USING (os)
WHERE os_version.os_version = factory.os_version
ORDER BY factory.name;

SELECT factory.name, browser.manufacturer, browser.name,
browser_version.major, browser_version.minor, browser.terminal, os.mobile
FROM factory_browser
JOIN factory USING (factory)
JOIN os_version USING (os_version)
JOIN os USING (os)
JOIN browser_version USING (browser_version)
JOIN browser USING (browser)
ORDER BY factory.name;

SELECT * FROM request;
SELECT * FROM browser_stats;

SELECT website.url, factory.name, browser.name
FROM lock
JOIN request USING (request)
JOIN website USING (website)
JOIN factory USING (factory)
JOIN browser USING (browser);
