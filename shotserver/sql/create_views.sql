CREATE VIEW browser_stats AS
SELECT browser_name, COUNT(*) AS queued FROM request, browser
WHERE request_browser = browser AND screenshot IS NULL
GROUP BY browser_name;
