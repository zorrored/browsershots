CREATE VIEW browser_stats AS
SELECT browser.name, COUNT(*) AS queued FROM job, browser
WHERE job.screenshot IS NULL and job.browser = browser.id
GROUP BY browser.name;
