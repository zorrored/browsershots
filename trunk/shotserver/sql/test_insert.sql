INSERT INTO person (person_name, person_email) VALUES ('Johann C. Rocholl', 'jcrocholl@browsershots.org');

INSERT INTO browser (browser_name, browser_manufacturer) VALUES ('Firefox', 'Mozilla');
INSERT INTO browser (browser_name, browser_manufacturer) VALUES ('Safari', 'Apple');
INSERT INTO browser (browser_name, browser_manufacturer) VALUES ('Internet Explorer', 'Microsoft');
INSERT INTO browser (browser_name, browser_manufacturer) VALUES ('Konqueror', 'KDE');
INSERT INTO browser (browser_name) VALUES ('Galeon');
INSERT INTO browser (browser_name) VALUES ('Mozilla');
INSERT INTO browser (browser_name) VALUES ('Epiphany');
INSERT INTO browser (browser_name) VALUES ('Opera');
INSERT INTO browser (browser_name) VALUES ('Camino');
INSERT INTO browser (browser_name, terminal) VALUES ('Links', TRUE);
INSERT INTO browser (browser_name, terminal) VALUES ('Lynx', TRUE);
INSERT INTO browser (browser_name, terminal) VALUES ('W3M', TRUE);
INSERT INTO browser (browser_name) VALUES ('NetFront');
INSERT INTO browser (browser_name) VALUES ('Blazer');
INSERT INTO browser (browser_name) VALUES ('EudoraWeb');

INSERT INTO engine (engine_name) VALUES ('Gecko');
INSERT INTO engine (engine_name) VALUES ('KHTML');

INSERT INTO browser_version (browser, browser_major, browser_minor, engine) VALUES (1, 1, 5, 1);
INSERT INTO browser_version (browser, browser_major, browser_minor, engine) VALUES (2, 2, 0, 2);
INSERT INTO browser_version (browser, browser_major, browser_minor, engine) VALUES (1, 1, 0, 1);
INSERT INTO browser_version (browser, browser_major, browser_minor, engine) VALUES (4, 3, 2, 2);
INSERT INTO browser_version (browser, browser_major, browser_minor) VALUES (8, 8, 5);
INSERT INTO browser_version (browser, browser_major, browser_minor, engine) VALUES (1, 1, 0, 1);
INSERT INTO browser_version (browser, browser_major, browser_minor, engine) VALUES (9, 1, 0, 1);
INSERT INTO browser_version (browser, browser_major, browser_minor) VALUES (11, 2, 8);
INSERT INTO browser_version (browser, browser_major, browser_minor) VALUES (12, 0, 5);
INSERT INTO browser_version (browser, browser_major, browser_minor) VALUES (13, 1, 0);

INSERT INTO os (os_name) VALUES ('Linux');
INSERT INTO os (os_name, os_manufacturer) VALUES ('Mac OS', 'Apple');
INSERT INTO os (os_name, os_manufacturer) VALUES ('Windows', 'Microsoft');
INSERT INTO os (os_name, os_manufacturer) VALUES ('Palm OS', 'Palm');

INSERT INTO os_version (os, os_distro, os_codename, os_major, os_minor) VALUES (1, 'Ubuntu', 'Dapper Drake', 6, 4);
INSERT INTO os_version (os, os_distro, os_codename, os_major, os_minor) VALUES (2, 'X', 'Tiger', 10, 4);
INSERT INTO os_version (os, os_distro, os_codename) VALUES (3, 'XP', 'Service Pack 2');
INSERT INTO os_version (os, os_distro, os_codename, os_major, os_minor) VALUES (1, 'Debian', 'Sarge', 3, 1);
INSERT INTO os_version (os, os_codename, os_major, os_minor, mobile) VALUES (4, 'Cobalt', 6, 1, TRUE);

INSERT INTO factory (factory_name, os_version, factory_admin) VALUES ('tyll', 1, 1);
INSERT INTO factory (factory_name, os_version, factory_admin) VALUES ('runt', 2, 1);
INSERT INTO factory (factory_name, os_version, factory_admin) VALUES ('sven', 3, 1);
INSERT INTO factory (factory_name, os_version, factory_admin) VALUES ('quad', 3, 1);
INSERT INTO factory (factory_name, os_version, factory_admin) VALUES ('azul', 4, 1);
INSERT INTO factory (factory_name, os_version, factory_admin) VALUES ('palm', 5, 1);

INSERT INTO factory_browser (factory, browser_version) VALUES (1, 1);
INSERT INTO factory_browser (factory, browser_version) VALUES (2, 2);
INSERT INTO factory_browser (factory, browser_version) VALUES (5, 3);
INSERT INTO factory_browser (factory, browser_version) VALUES (5, 4);
INSERT INTO factory_browser (factory, browser_version) VALUES (5, 5);

INSERT INTO factory_screen (factory, screen_width, screen_height) VALUES (1, 1024, 768);
INSERT INTO factory_screen (factory, screen_width, screen_height) VALUES (1, 800, 600);

INSERT INTO website (website_url) VALUES ('http://foo');
INSERT INTO website (website_url) VALUES ('http://bar');
INSERT INTO website (website_url) VALUES ('http://baz');

INSERT INTO request (website, request_browser, request_major, request_minor) VALUES (1, 1, 1, 5);
INSERT INTO request (website, request_browser, request_os) VALUES (2, 1, 1);
INSERT INTO request (website, request_browser) VALUES (1, 2);
INSERT INTO request (website, request_browser) VALUES (2, 2);
INSERT INTO request (website, request_browser) VALUES (3, 2);

INSERT INTO lock (request, factory) VALUES (1, 1);
INSERT INTO lock (request, factory) VALUES (3, 2);
