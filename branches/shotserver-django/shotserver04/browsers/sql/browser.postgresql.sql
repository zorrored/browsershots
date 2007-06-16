ALTER TABLE browsers_browser
ADD CONSTRAINT browsers_browser_version_check
CHECK (user_agent ~ version);

ALTER TABLE browsers_browser
ADD CONSTRAINT browsers_browser_major_minor_check
CHECK (version ~ ('^' || major || '\\.0*' || minor));

ALTER TABLE browsers_browser
ADD CONSTRAINT browsers_browser_engine_version_check
CHECK (user_agent ~ engine_version);
