CREATE VIEW browser_stats AS
SELECT browser.name, COUNT(*) AS queued
FROM request
JOIN request_browser USING (request)
JOIN browser USING (browser)
WHERE screenshot IS NULL
GROUP BY browser.name;
