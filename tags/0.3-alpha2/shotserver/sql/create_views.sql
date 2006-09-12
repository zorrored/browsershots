CREATE VIEW browser_stats AS
SELECT browser_group.name, COUNT(*) AS queued
FROM request
JOIN browser_group USING (browser_group)
WHERE screenshot IS NULL
GROUP BY browser_group.name;
