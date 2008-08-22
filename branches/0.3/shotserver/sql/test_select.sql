SELECT * FROM person;

SELECT name, major, minor, manufacturer, terminal
FROM browser
JOIN browser_group USING (browser_group)
ORDER BY name;

SELECT DISTINCT name, distro, codename, major, minor, manufacturer, mobile
FROM opsys
JOIN opsys_group USING (opsys_group)
ORDER BY name;

SELECT factory.name, architecture.name, opsys_group.name,
opsys.distro, opsys.codename, opsys.major, opsys.minor,
person.name
FROM factory
JOIN architecture USING (architecture)
JOIN opsys USING (opsys)
JOIN opsys_group USING (opsys_group)
JOIN person ON factory.creator = person.person
ORDER BY factory.name;

SELECT factory.name, browser_group.manufacturer, browser_group.name,
browser.major, browser.minor, browser_group.terminal, opsys.mobile
FROM factory_browser
JOIN factory USING (factory)
JOIN opsys USING (opsys)
JOIN opsys_group USING (opsys_group)
JOIN browser USING (browser)
JOIN browser_group USING (browser_group)
ORDER BY factory.name;

SELECT * FROM request;
SELECT * FROM browser_stats;

SELECT website.url, factory.name, browser_group.name
FROM lock
JOIN request USING (request)
JOIN request_group USING (request_group)
JOIN website USING (website)
JOIN factory USING (factory)
JOIN browser_group USING (browser_group);

SELECT DISTINCT browser_group.name
FROM factory_browser
JOIN factory USING (factory)
JOIN opsys USING (opsys)
JOIN opsys_group USING (opsys_group)
JOIN browser USING (browser)
JOIN browser_group USING (browser_group)
WHERE opsys_group.name = 'Linux';

SELECT DISTINCT browser_group.name
FROM factory_browser
JOIN factory USING (factory)
JOIN opsys USING (opsys)
JOIN opsys_group USING (opsys_group)
JOIN browser USING (browser)
JOIN browser_group USING (browser_group)
WHERE opsys_group.name = 'Mac OS';

SELECT DISTINCT browser_group.name
FROM factory_browser
JOIN factory USING (factory)
JOIN opsys USING (opsys)
JOIN opsys_group USING (opsys_group)
JOIN browser USING (browser)
JOIN browser_group USING (browser_group)
WHERE opsys_group.name = 'Windows';

SELECT DISTINCT browser_group.name
FROM factory_browser
JOIN factory USING (factory)
JOIN opsys USING (opsys)
JOIN opsys_group USING (opsys_group)
JOIN browser USING (browser)
JOIN browser_group USING (browser_group)
WHERE browser_group.terminal;

SELECT DISTINCT browser_group.name
FROM factory_browser
JOIN factory USING (factory)
JOIN opsys USING (opsys)
JOIN opsys_group USING (opsys_group)
JOIN browser USING (browser)
JOIN browser_group USING (browser_group)
WHERE opsys.mobile;

SELECT factory.name, architecture.name, opsys_group.name,
opsys.distro, opsys.codename, opsys.major, opsys.minor, opsys.mobile
FROM factory
JOIN architecture USING (architecture)
JOIN opsys USING (opsys)
JOIN opsys_group USING (opsys_group);
