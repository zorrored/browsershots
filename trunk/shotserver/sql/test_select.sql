SELECT * FROM person;

SELECT name, major, minor, manufacturer, terminal
FROM browser
JOIN browser_version USING (browser)
ORDER BY name;

SELECT DISTINCT name, distro, codename, major, minor, manufacturer, mobile
FROM opsys
JOIN opsys_version USING (opsys)
ORDER BY name;

SELECT factory.name, architecture.name, opsys.name,
opsys_version.distro, opsys_version.codename, opsys_version.major, opsys_version.minor,
person.name
FROM factory
JOIN architecture USING (architecture)
JOIN opsys_version USING (opsys_version)
JOIN opsys USING (opsys)
JOIN person ON factory.creator = person.person
ORDER BY factory.name;

SELECT factory.name, browser.manufacturer, browser.name,
browser_version.major, browser_version.minor, browser.terminal, opsys_version.mobile
FROM factory_browser
JOIN factory USING (factory)
JOIN opsys_version USING (opsys_version)
JOIN opsys USING (opsys)
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
JOIN opsys_version USING (opsys_version)
JOIN opsys USING (opsys)
JOIN browser_version USING (browser_version)
JOIN browser USING (browser)
WHERE opsys.name = 'Linux';

SELECT DISTINCT browser.name
FROM factory_browser
JOIN factory USING (factory)
JOIN opsys_version USING (opsys_version)
JOIN opsys USING (opsys)
JOIN browser_version USING (browser_version)
JOIN browser USING (browser)
WHERE opsys.name = 'Mac OS';

SELECT DISTINCT browser.name
FROM factory_browser
JOIN factory USING (factory)
JOIN opsys_version USING (opsys_version)
JOIN opsys USING (opsys)
JOIN browser_version USING (browser_version)
JOIN browser USING (browser)
WHERE opsys.name = 'Windows';

SELECT DISTINCT browser.name
FROM factory_browser
JOIN factory USING (factory)
JOIN opsys_version USING (opsys_version)
JOIN opsys USING (opsys)
JOIN browser_version USING (browser_version)
JOIN browser USING (browser)
WHERE browser.terminal;

SELECT DISTINCT browser.name
FROM factory_browser
JOIN factory USING (factory)
JOIN opsys_version USING (opsys_version)
JOIN opsys USING (opsys)
JOIN browser_version USING (browser_version)
JOIN browser USING (browser)
WHERE opsys_version.mobile;

SELECT factory.name, architecture.name, opsys.name,
opsys_version.distro, opsys_version.codename, opsys_version.major, opsys_version.minor, opsys_version.mobile
FROM factory
JOIN architecture USING (architecture)
JOIN opsys_version USING (opsys_version)
JOIN opsys USING (opsys);
