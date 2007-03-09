ALTER TABLE websites_website
ADD CONSTRAINT websites_website_url_check
CHECK (url ~ '^https?://[a-z0-9_\.\-]*/');
