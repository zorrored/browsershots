-- Delete expired nonces.
DELETE FROM nonces_nonce
WHERE created < NOW() - '7d'::interval;

-- Delete old requests that don't have screenshots.
DELETE FROM requests_request
WHERE screenshot_id IS NULL
AND EXISTS (SELECT 1 FROM requests_requestgroup
    WHERE id = requests_request.request_group_id
    AND submitted < NOW() - '7d'::interval);

-- Delete old request groups without requests.
DELETE FROM requests_requestgroup
WHERE submitted < NOW() - '7d'::interval
AND NOT EXISTS (SELECT 1 FROM requests_request
    WHERE request_group_id = requests_requestgroup.id);

-- Delete old websites without request groups.
DELETE FROM websites_website
WHERE submitted < NOW() - '7d'::interval
AND NOT EXISTS (SELECT 1 FROM requests_requestgroup
    WHERE website_id = websites_website.id)
AND NOT EXISTS (SELECT 1 FROM screenshots_screenshot
    WHERE website_id = screenshots_screenshot.id);

-- Delete old domains without websites.
DELETE FROM websites_domain
WHERE submitted < NOW() - '7d'::interval
AND NOT EXISTS (SELECT 1 FROM websites_website
    WHERE domain_id = websites_domain.id)
AND NOT EXISTS (SELECT 1 FROM priority_domainpriority
    WHERE domain_id = websites_domain.id);
