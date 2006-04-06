SELECT * FROM person;

SELECT name, major, minor, manufacturer, terminal
FROM browser JOIN browser_version USING (browser)
ORDER BY name;

SELECT DISTINCT name, distro, codename, major, minor, manufacturer, mobile
FROM os JOIN os_version USING (os)
ORDER BY name;

SELECT factory.name, platform.name, os.name, 
os_version.distro, os_version.codename, os_version.major, os_version.minor,
person.name
FROM factory
JOIN platform USING (platform)
JOIN os_version USING (os_version)
JOIN os USING (os)
JOIN person ON factory.creator = person.person
ORDER BY factory.name;

SELECT factory.name, browser.manufacturer, browser.name,
browser_version.major, browser_version.minor, browser.terminal, os_version.mobile
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

SELECT DISTINCT browser.name
FROM factory_browser
JOIN factory USING (factory)
JOIN os_version USING (os_version)
JOIN os USING (os)
JOIN browser_version USING (browser_version)
JOIN browser USING (browser)
WHERE os.name = 'Linux';

SELECT DISTINCT browser.name
FROM factory_browser
JOIN factory USING (factory)
JOIN os_version USING (os_version)
JOIN os USING (os)
JOIN browser_version USING (browser_version)
JOIN browser USING (browser)
WHERE os.name = 'Mac OS';

SELECT DISTINCT browser.name
FROM factory_browser
JOIN factory USING (factory)
JOIN os_version USING (os_version)
JOIN os USING (os)
JOIN browser_version USING (browser_version)
JOIN browser USING (browser)
WHERE os.name = 'Windows';

SELECT DISTINCT browser.name
FROM factory_browser
JOIN factory USING (factory)
JOIN os_version USING (os_version)
JOIN os USING (os)
JOIN browser_version USING (browser_version)
JOIN browser USING (browser)
WHERE browser.terminal;

SELECT DISTINCT browser.name
FROM factory_browser
JOIN factory USING (factory)
JOIN os_version USING (os_version)
JOIN os USING (os)
JOIN browser_version USING (browser_version)
JOIN browser USING (browser)
WHERE os_version.mobile;

SELECT factory.name, platform.name, os.name,
os_version.distro, os_version.codename, os_version.major, os_version.minor, os_version.mobile
FROM factory
JOIN platform USING (platform)
JOIN os_version USING (os_version)
JOIN os USING (os);
