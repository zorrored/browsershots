ALTER TABLE websites_website
ADD CONSTRAINT websites_website_url_check
CHECK (url ~* '^https?://(([a-z0-9_-]+\\.)+[a-z]+|\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}|\\d+)(:\\d+)?/\\S*$');
