EXPLAIN ANALYZE SELECT request,
       browser_group.name, major, minor,
       width, bpp, js, java, flash, media
FROM request
JOIN request_group USING (request_group)
JOIN browser_group USING (browser_group)
LEFT JOIN opsys_group USING (opsys_group)
WHERE (opsys_group IS NULL OR opsys_group.name = 'Linux') AND
(
(browser_group.name = 'Firefox' AND (major IS NULL OR major = 1) AND (minor IS NULL OR minor = 5)) OR
(browser_group.name = 'Konqueror' AND (major IS NULL OR major = 3) AND (minor IS NULL OR minor = 5))
) AND
(width IS NULL OR width = 640 OR width = 800 OR width = 1024 OR width = 1280 OR width = 1600) AND
(media IS NULL) AND
(bpp IS NULL OR bpp = 8 OR bpp = 16 OR bpp = 24) AND
(flash IS NULL OR 'yes' = flash) AND
(java IS NULL) AND
(js IS NULL OR 'yes' = js)
AND screenshot IS NULL
AND (locked IS NULL OR NOW() - locked > '0:01:00')
ORDER BY request_group.created ASC
LIMIT 1
