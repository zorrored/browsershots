INSERT INTO browser (name, manufacturer) VALUES ('Firefox', 'Mozilla');
INSERT INTO browser (name, manufacturer) VALUES ('Safari', 'Apple');
INSERT INTO browser (name, manufacturer) VALUES ('Internet Explorer', 'Microsoft');
INSERT INTO browser (name, manufacturer) VALUES ('Konqueror', 'KDE');
INSERT INTO browser (name) VALUES ('Galeon');
INSERT INTO browser (name) VALUES ('Mozilla');
INSERT INTO browser (name) VALUES ('Epiphany');
INSERT INTO browser (name) VALUES ('Opera');

INSERT INTO browser_version (browser, major, minor, engine) VALUES (1, 1, 5, 'Gecko');
INSERT INTO browser_version (browser, major, minor, engine) VALUES (2, 2, 0, 'KHTML');
INSERT INTO browser_version (browser, major, minor, engine) VALUES (1, 1, 0, 'Gecko');
INSERT INTO browser_version (browser, major, minor, engine) VALUES (4, 3, 2, 'KHTML');

INSERT INTO os (name, distro, version, major, minor, manufacturer) VALUES ('Linux', 'Ubuntu', 'Dapper Drake', 6, 4, 'Canonical');
INSERT INTO os (name, distro, version, major, minor, manufacturer) VALUES ('Mac OS', 'X', 'Tiger', 10, 4, 'Apple');
INSERT INTO os (name, distro, version, manufacturer) VALUES ('Windows', 'XP', 'Service Pack 2', 'Microsoft');
INSERT INTO os (name, distro, version, major, minor) VALUES ('Linux', 'Debian', 'Sarge', 3, 1);

INSERT INTO factory (name, os) VALUES ('tyll', 1);
INSERT INTO factory (name, os) VALUES ('runt', 2);
INSERT INTO factory (name, os) VALUES ('sven', 3);
INSERT INTO factory (name, os) VALUES ('quad', 3);
INSERT INTO factory (name, os) VALUES ('azul', 4);

INSERT INTO factory_browser (factory, browser_version) VALUES (1, 1);
INSERT INTO factory_browser (factory, browser_version) VALUES (2, 2);
INSERT INTO factory_browser (factory, browser_version) VALUES (5, 3);
INSERT INTO factory_browser (factory, browser_version) VALUES (5, 4);

INSERT INTO factory_resolution (factory, width, height) VALUES (1, 1024, 768);
INSERT INTO factory_resolution (factory, width, height) VALUES (1, 800, 600);

INSERT INTO website (url) VALUES ('http://foo');
INSERT INTO website (url) VALUES ('http://bar');
INSERT INTO website (url) VALUES ('http://baz');

INSERT INTO job (browser, website) VALUES (1, 1);
INSERT INTO job (browser, website) VALUES (1, 2);
INSERT INTO job (browser, website) VALUES (2, 1);
INSERT INTO job (browser, website) VALUES (2, 2);
INSERT INTO job (browser, website) VALUES (2, 3);
