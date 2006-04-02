INSERT INTO person (name, email) VALUES ('Johann C. Rocholl', 'jcrocholl@browsershots.org');

INSERT INTO browser (name, manufacturer, creator) VALUES ('Firefox', 'Mozilla', 1);
INSERT INTO browser (name, manufacturer, creator) VALUES ('Safari', 'Apple', 1);
INSERT INTO browser (name, manufacturer, creator) VALUES ('MSIE', 'Microsoft', 1);
INSERT INTO browser (name, manufacturer, creator) VALUES ('Konqueror', 'KDE', 1);
INSERT INTO browser (name, creator) VALUES ('Galeon', 1);
INSERT INTO browser (name, creator) VALUES ('Mozilla', 1);
INSERT INTO browser (name, creator) VALUES ('Epiphany', 1);
INSERT INTO browser (name, creator) VALUES ('Opera', 1);
INSERT INTO browser (name, creator) VALUES ('Camino', 1);
INSERT INTO browser (name, terminal, creator) VALUES ('Links', TRUE, 1);
INSERT INTO browser (name, terminal, creator) VALUES ('Lynx', TRUE, 1);
INSERT INTO browser (name, terminal, creator) VALUES ('W3M', TRUE, 1);
INSERT INTO browser (name, creator) VALUES ('NetFront', 1);
INSERT INTO browser (name, creator) VALUES ('Blazer', 1);
INSERT INTO browser (name, creator) VALUES ('EudoraWeb', 1);

INSERT INTO engine (name, creator) VALUES ('Gecko', 1);
INSERT INTO engine (name, creator) VALUES ('KHTML', 1);

INSERT INTO browser_version (browser, major, minor, engine, creator) VALUES (1, 1, 5, 1, 1);
INSERT INTO browser_version (browser, major, minor, engine, creator) VALUES (2, 2, 0, 2, 1);
INSERT INTO browser_version (browser, major, minor, engine, creator) VALUES (1, 1, 0, 1, 1);
INSERT INTO browser_version (browser, major, minor, engine, creator) VALUES (4, 3, 3, 2, 1);
INSERT INTO browser_version (browser, major, minor, creator) VALUES (8, 8, 5, 1);
INSERT INTO browser_version (browser, major, minor, engine, creator) VALUES (9, 1, 0, 1, 1);
INSERT INTO browser_version (browser, major, minor, creator) VALUES (11, 2, 8, 1);
INSERT INTO browser_version (browser, major, minor, creator) VALUES (12, 0, 5, 1);
INSERT INTO browser_version (browser, major, minor, creator) VALUES (13, 1, 0, 1);
INSERT INTO browser_version (browser, major, minor, creator) VALUES (3, 6, 0, 1);
INSERT INTO browser_version (browser, major, minor, creator) VALUES (3, 7, 0, 1);

INSERT INTO os (name, creator) VALUES ('Linux', 1);
INSERT INTO os (name, manufacturer, creator) VALUES ('Mac OS', 'Apple', 1);
INSERT INTO os (name, manufacturer, creator) VALUES ('Windows', 'Microsoft', 1);
INSERT INTO os (name, mobile, creator) VALUES ('Palm OS', TRUE, 1);

INSERT INTO os_version (os, distro, codename, major, minor, creator) VALUES (1, 'Ubuntu', 'Dapper Drake', 6, 4, 1);
INSERT INTO os_version (os, distro, codename, major, minor, creator) VALUES (2, 'X', 'Tiger', 10, 4, 1);
INSERT INTO os_version (os, distro, codename, creator) VALUES (3, 'XP', 'Service Pack 2', 1);
INSERT INTO os_version (os, distro, codename, major, minor, creator) VALUES (1, 'Debian', 'Sarge', 3, 1, 1);
INSERT INTO os_version (os, codename, major, minor, creator) VALUES (4, 'Cobalt', 6, 1, 1);

INSERT INTO factory (name, os_version, creator) VALUES ('tyll', 1, 1);
INSERT INTO factory (name, os_version, creator) VALUES ('runt', 2, 1);
INSERT INTO factory (name, os_version, creator) VALUES ('sven', 3, 1);
INSERT INTO factory (name, os_version, creator) VALUES ('quad', 3, 1);
INSERT INTO factory (name, os_version, creator) VALUES ('azul', 4, 1);
INSERT INTO factory (name, os_version, creator) VALUES ('palm', 5, 1);

INSERT INTO factory_browser (factory, browser_version) VALUES (1, 1);
INSERT INTO factory_browser (factory, browser_version) VALUES (2, 2);
INSERT INTO factory_browser (factory, browser_version) VALUES (5, 3);
INSERT INTO factory_browser (factory, browser_version) VALUES (5, 4);
INSERT INTO factory_browser (factory, browser_version) VALUES (5, 5);
INSERT INTO factory_browser (factory, browser_version) VALUES (3, 11);
INSERT INTO factory_browser (factory, browser_version) VALUES (4, 10);

INSERT INTO factory_screen (factory, width, height) VALUES (1, 1024, 768);
INSERT INTO factory_screen (factory, width, height) VALUES (1, 800, 600);

INSERT INTO website (url) VALUES ('http://foo');
INSERT INTO website (url) VALUES ('http://bar');
INSERT INTO website (url) VALUES ('http://baz');

INSERT INTO request (website, browser, major, minor) VALUES (1, 1, 1, 5);
INSERT INTO request (website, browser, os) VALUES (2, 1, 1);
INSERT INTO request (website, browser) VALUES (1, 2);
INSERT INTO request (website, browser) VALUES (2, 2);
INSERT INTO request (website, browser) VALUES (3, 2);

INSERT INTO lock (request, factory) VALUES (1, 1);
INSERT INTO lock (request, factory) VALUES (3, 2);
