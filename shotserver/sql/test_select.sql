SELECT * FROM person;

SELECT name, major, minor, manufacturer, terminal
FROM browser JOIN browser_version USING (browser)
ORDER BY name;

SELECT DISTINCT name, distro, codename, major, minor, manufacturer, mobile
FROM platform JOIN platform_version USING (platform)
ORDER BY name;

SELECT factory.name, architecture.name, platform.name,
platform_version.distro, platform_version.codename, platform_version.major, platform_version.minor,
person.name
FROM factory
JOIN architecture USING (architecture)
JOIN platform_version USING (platform_version)
JOIN platform USING (platform)
JOIN person ON factory.creator = person.person
ORDER BY factory.name;

SELECT factory.name, browser.manufacturer, browser.name,
browser_version.major, browser_version.minor, browser.terminal, platform_version.mobile
FROM factory_browser
JOIN factory USING (factory)
JOIN platform_version USING (platform_version)
JOIN platform USING (platform)
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
JOIN platform_version USING (platform_version)
JOIN platform USING (platform)
JOIN browser_version USING (browser_version)
JOIN browser USING (browser)
WHERE platform.name = 'Linux';

SELECT DISTINCT browser.name
FROM factory_browser
JOIN factory USING (factory)
JOIN platform_version USING (platform_version)
JOIN platform USING (platform)
JOIN browser_version USING (browser_version)
JOIN browser USING (browser)
WHERE platform.name = 'Mac OS';

SELECT DISTINCT browser.name
FROM factory_browser
JOIN factory USING (factory)
JOIN platform_version USING (platform_version)
JOIN platform USING (platform)
JOIN browser_version USING (browser_version)
JOIN browser USING (browser)
WHERE platform.name = 'Windows';

SELECT DISTINCT browser.name
FROM factory_browser
JOIN factory USING (factory)
JOIN platform_version USING (platform_version)
JOIN platform USING (platform)
JOIN browser_version USING (browser_version)
JOIN browser USING (browser)
WHERE browser.terminal;

SELECT DISTINCT browser.name
FROM factory_browser
JOIN factory USING (factory)
JOIN platform_version USING (platform_version)
JOIN platform USING (platform)
JOIN browser_version USING (browser_version)
JOIN browser USING (browser)
WHERE platform_version.mobile;

SELECT factory.name, architecture.name, platform.name,
platform_version.distro, platform_version.codename, platform_version.major, platform_version.minor, platform_version.mobile
FROM factory
JOIN architecture USING (architecture)
JOIN platform_version USING (platform_version)
JOIN platform USING (platform);
