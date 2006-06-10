INSERT INTO person (name, salt, password, email) VALUES ('Johann C. Rocholl', 'beef', md5('beefsecret'), 'jcrocholl@browsershots.org');

INSERT INTO architecture (name, creator) VALUES ('i386', 1);
INSERT INTO architecture (name, creator) VALUES ('PPC', 1);
INSERT INTO architecture (name, creator) VALUES ('68000', 1);
INSERT INTO architecture (name, creator) VALUES ('Palm', 1);
INSERT INTO architecture (name, creator) VALUES ('AMD64', 1);

INSERT INTO engine (name, creator) VALUES ('Gecko', 1);
INSERT INTO engine (name, creator) VALUES ('KHTML', 1);

INSERT INTO browser_group (name, manufacturer, creator) VALUES ('Firefox', 'Mozilla', 1);
INSERT INTO browser_group (name, manufacturer, creator) VALUES ('Safari', 'Apple', 1);
INSERT INTO browser_group (name, manufacturer, creator) VALUES ('MSIE', 'Microsoft', 1);
INSERT INTO browser_group (name, manufacturer, creator) VALUES ('Konqueror', 'KDE', 1);
INSERT INTO browser_group (name, creator) VALUES ('Galeon', 1);
INSERT INTO browser_group (name, creator) VALUES ('Mozilla', 1);
INSERT INTO browser_group (name, creator) VALUES ('Epiphany', 1);
INSERT INTO browser_group (name, creator) VALUES ('Opera', 1);
INSERT INTO browser_group (name, creator) VALUES ('Camino', 1);
INSERT INTO browser_group (name, terminal, creator) VALUES ('Links', TRUE, 1);
INSERT INTO browser_group (name, terminal, creator) VALUES ('Lynx', TRUE, 1);
INSERT INTO browser_group (name, terminal, creator) VALUES ('W3M', TRUE, 1);
INSERT INTO browser_group (name, creator) VALUES ('NetFront', 1);
INSERT INTO browser_group (name, creator) VALUES ('WebToGo', 1);
INSERT INTO browser_group (name, creator) VALUES ('EudoraWeb', 1);

INSERT INTO browser (browser_group, major, minor, engine, creator) VALUES (1, 1, 5, 1, 1);
INSERT INTO browser (browser_group, major, minor, engine, creator) VALUES (2, 2, 0, 2, 1);
INSERT INTO browser (browser_group, major, minor, creator) VALUES (3, 6, 0, 1);
INSERT INTO browser (browser_group, major, minor, engine, creator) VALUES (4, 3, 3, 2, 1);
INSERT INTO browser (browser_group, major, minor, engine, creator) VALUES (5, 1, 3, 1, 1);
INSERT INTO browser (browser_group, major, minor, engine, creator) VALUES (6, 1, 7, 1, 1);
INSERT INTO browser (browser_group, major, minor, engine, creator) VALUES (7, 1, 4, 1, 1);
INSERT INTO browser (browser_group, major, minor, creator) VALUES (8, 8, 5, 1);
INSERT INTO browser (browser_group, major, minor, engine, creator) VALUES (9, 1, 0, 1, 1);
INSERT INTO browser (browser_group, major, minor, creator) VALUES (10, 1, 0, 1);
INSERT INTO browser (browser_group, major, minor, creator) VALUES (11, 2, 8, 1);
INSERT INTO browser (browser_group, major, minor, creator) VALUES (12, 0, 5, 1);
INSERT INTO browser (browser_group, major, minor, creator) VALUES (13, 3, 3, 1);
INSERT INTO browser (browser_group, major, minor, creator) VALUES (14, 4, 2, 1);
INSERT INTO browser (browser_group, major, minor, creator) VALUES (15, 2, 1, 1);
INSERT INTO browser (browser_group, major, minor, engine, creator) VALUES (1, 1, 0, 1, 1);
INSERT INTO browser (browser_group, major, minor, creator) VALUES (3, 7, 0, 1);
INSERT INTO browser (browser_group, major, minor, creator) VALUES (3, 5, 2, 1);
INSERT INTO browser (browser_group, major, minor, creator) VALUES (3, 5, 5, 1);

INSERT INTO opsys_group (name, creator) VALUES ('Linux', 1);
INSERT INTO opsys_group (name, manufacturer, creator) VALUES ('Mac OS', 'Apple', 1);
INSERT INTO opsys_group (name, manufacturer, creator) VALUES ('Windows', 'Microsoft', 1);
INSERT INTO opsys_group (name, creator) VALUES ('Palm OS', 1);
INSERT INTO opsys_group (name, creator) VALUES ('Symbian', 1);
INSERT INTO opsys_group (name, creator) VALUES ('Solaris', 1);
INSERT INTO opsys_group (name, creator) VALUES ('TOS', 1);

INSERT INTO opsys (opsys_group, distro, codename, major, minor, creator) VALUES (1, 'Ubuntu', 'Dapper Drake', 6, 4, 1);
INSERT INTO opsys (opsys_group, distro, codename, major, minor, creator) VALUES (2, 'X', 'Tiger', 10, 4, 1);
INSERT INTO opsys (opsys_group, distro, codename, creator) VALUES (3, 'XP', 'Service Pack 2', 1);
INSERT INTO opsys (opsys_group, codename, major, minor, mobile, creator) VALUES (4, 'Cobalt', 6, 1, TRUE, 1);
INSERT INTO opsys (opsys_group, major, minor, mobile, creator) VALUES (5, 6, 1, TRUE, 1);
INSERT INTO opsys (opsys_group, major, minor, creator) VALUES (6, 5, 8, 1);
INSERT INTO opsys (opsys_group, major, minor, creator) VALUES (7, 2, 6, 1);
INSERT INTO opsys (opsys_group, distro, codename, major, minor, creator) VALUES (1, 'Debian', 'Sarge', 3, 1, 1);

INSERT INTO factory (name, opsys, architecture, creator, owner) VALUES ('tyll', 1, 1, 1, 1);
INSERT INTO factory (name, opsys, architecture, creator, owner) VALUES ('runt', 2, 2, 1, 1);
INSERT INTO factory (name, opsys, architecture, creator, owner) VALUES ('quad', 3, 1, 1, 1);
INSERT INTO factory (name, opsys, architecture, creator, owner) VALUES ('palm', 4, 4, 1, 1);
INSERT INTO factory (name, opsys, architecture, creator, owner) VALUES ('7650', 5, 4, 1, 1);
INSERT INTO factory (name, opsys, architecture, creator, owner) VALUES ('lara', 6, 3, 1, 1);
INSERT INTO factory (name, opsys, architecture, creator, owner) VALUES ('tari', 7, 3, 1, 1);
INSERT INTO factory (name, opsys, architecture, creator, owner) VALUES ('azul', 8, 5, 1, 1);
INSERT INTO factory (name, opsys, architecture, creator, owner) VALUES ('sven', 3, 1, 1, 1);
INSERT INTO factory (name, salt, password, opsys, architecture, creator, owner) VALUES ('argo', '1234', md5('1234secret'), 8, 5, 1, 1);

INSERT INTO factory_browser (factory, browser) VALUES (1, 1);
INSERT INTO factory_browser (factory, browser) VALUES (1, 10);
INSERT INTO factory_browser (factory, browser) VALUES (1, 11);
INSERT INTO factory_browser (factory, browser) VALUES (1, 12);
INSERT INTO factory_browser (factory, browser) VALUES (2, 2);
INSERT INTO factory_browser (factory, browser) VALUES (2, 9);
INSERT INTO factory_browser (factory, browser) VALUES (2, 18);
INSERT INTO factory_browser (factory, browser) VALUES (3, 3);
INSERT INTO factory_browser (factory, browser) VALUES (3, 1);
INSERT INTO factory_browser (factory, browser) VALUES (4, 13);
INSERT INTO factory_browser (factory, browser) VALUES (4, 14);
INSERT INTO factory_browser (factory, browser) VALUES (4, 15);
INSERT INTO factory_browser (factory, browser) VALUES (8, 4);
INSERT INTO factory_browser (factory, browser) VALUES (8, 5);
INSERT INTO factory_browser (factory, browser) VALUES (8, 6);
INSERT INTO factory_browser (factory, browser) VALUES (8, 7);
INSERT INTO factory_browser (factory, browser) VALUES (8, 8);
INSERT INTO factory_browser (factory, browser) VALUES (8, 16);
INSERT INTO factory_browser (factory, browser) VALUES (9, 17);
INSERT INTO factory_browser (factory, browser) VALUES (9, 19);
INSERT INTO factory_browser (factory, browser) VALUES (9, 8);

INSERT INTO factory_screen (factory, width, height) VALUES (1, 1024, 768);
INSERT INTO factory_screen (factory, width, height) VALUES (1, 800, 600);

INSERT INTO factory_feature (factory, name, intval) VALUES (1, 'bpp', 24);
INSERT INTO factory_feature (factory, name, strval) VALUES (1, 'flash', '7.0 r63');

INSERT INTO website (url) VALUES ('http://foo');
INSERT INTO website (url) VALUES ('http://bar');
INSERT INTO website (url) VALUES ('http://baz');

INSERT INTO request_group (website, expire) VALUES (1, NOW() + '0:30');
INSERT INTO request_group (website, expire, width) VALUES (2, NOW() + '1:00', 800);
INSERT INTO request_group (website, expire, width) VALUES (3, NOW() + '4:00', 1024);

INSERT INTO request (request_group, browser_group, major, minor) VALUES (1, 1, 1, 5);
INSERT INTO request (request_group, browser_group, opsys_group) VALUES (1, 1, 1);
INSERT INTO request (request_group, browser_group) VALUES (1, 2);
INSERT INTO request (request_group, browser_group) VALUES (2, 2);
INSERT INTO request (request_group, browser_group) VALUES (3, 2);

INSERT INTO lock (request, factory) VALUES (1, 1);

INSERT INTO screenshot (hashkey, factory, width, height) VALUES (md5('hashkey'), 1, 640, 480);
