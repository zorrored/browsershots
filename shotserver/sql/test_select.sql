SELECT * FROM os;
SELECT * FROM browser_stats;

SELECT factory.name,
os.manufacturer, os.name, os.distro, os.version, os.major, os.minor
FROM factory, os WHERE factory.os = os.id;

SELECT factory.name, browser.manufacturer, browser.name,
browser_version.major, browser_version.minor, browser_version.engine
FROM factory_browser, factory, browser_version, browser
WHERE factory_browser.factory = factory.id
AND factory_browser.browser_version = browser_version.id
AND browser_version.browser = browser.id;
