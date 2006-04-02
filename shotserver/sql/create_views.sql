CREATE VIEW browser_stats AS
SELECT browser.name, COUNT(*) AS queued
FROM request JOIN browser USING (browser)
WHERE screenshot IS NULL
GROUP BY browser.name;
