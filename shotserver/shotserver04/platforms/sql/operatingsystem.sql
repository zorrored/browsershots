INSERT INTO "platforms_operatingsystem" ("id","platform_id","name","version","codename","maker") VALUES (1,1,'Debian','3.1','Sarge','');
INSERT INTO "platforms_operatingsystem" ("id","platform_id","name","version","codename","maker") VALUES (2,1,'Debian','4.0','Etch','');
INSERT INTO "platforms_operatingsystem" ("id","platform_id","name","version","codename","maker") VALUES (3,1,'PLD','2.0','Ac','');
INSERT INTO "platforms_operatingsystem" ("id","platform_id","name","version","codename","maker") VALUES (4,1,'Gentoo','2006.0','','');
INSERT INTO "platforms_operatingsystem" ("id","platform_id","name","version","codename","maker") VALUES (5,1,'Ubuntu','5.10','Breezy Badger','Canonical');
INSERT INTO "platforms_operatingsystem" ("id","platform_id","name","version","codename","maker") VALUES (6,1,'Ubuntu','6.06 LTS','Dapper Drake','Canonical');
INSERT INTO "platforms_operatingsystem" ("id","platform_id","name","version","codename","maker") VALUES (7,1,'Ubuntu','6.10','Edgy Eft','Canonical');
INSERT INTO "platforms_operatingsystem" ("id","platform_id","name","version","codename","maker") VALUES (8,1,'Ubuntu','7.04','Feisty Fawn','Canonical');
INSERT INTO "platforms_operatingsystem" ("id","platform_id","name","version","codename","maker") VALUES (9,2,'Mac OS X','10.3','Jaguar','Apple');
INSERT INTO "platforms_operatingsystem" ("id","platform_id","name","version","codename","maker") VALUES (10,2,'Mac OS X','10.4','Tiger','Apple');
INSERT INTO "platforms_operatingsystem" ("id","platform_id","name","version","codename","maker") VALUES (11,2,'Mac OS X','10.5','Leopard','Apple');
INSERT INTO "platforms_operatingsystem" ("id","platform_id","name","version","codename","maker") VALUES (12,3,'Windows','98','','Microsoft');
INSERT INTO "platforms_operatingsystem" ("id","platform_id","name","version","codename","maker") VALUES (13,3,'Windows','ME','','Microsoft');
INSERT INTO "platforms_operatingsystem" ("id","platform_id","name","version","codename","maker") VALUES (14,3,'Windows','XP','','Microsoft');
INSERT INTO "platforms_operatingsystem" ("id","platform_id","name","version","codename","maker") VALUES (15,3,'Windows','2003','Server','Microsoft');
INSERT INTO "platforms_operatingsystem" ("id","platform_id","name","version","codename","maker") VALUES (16,3,'Windows','Vista','','Microsoft');
INSERT INTO "platforms_operatingsystem" ("id","platform_id","name","version","codename","maker") VALUES (17,3,'Windows','2000','','Microsoft');
INSERT INTO "platforms_operatingsystem" ("id","platform_id","name","version","codename","maker") VALUES (18,1,'Fedora','7','','Red Hat');
INSERT INTO "platforms_operatingsystem" ("id","platform_id","name","version","codename","maker") VALUES (19,1,'PLD','3.0','Th','');
INSERT INTO "platforms_operatingsystem" ("id","platform_id","name","version","codename","maker") VALUES (20,1,'Arch','','Current','');
INSERT INTO "platforms_operatingsystem" ("id","platform_id","name","version","codename","maker") VALUES (21,1,'Debian','3.0','Woody','');
INSERT INTO "platforms_operatingsystem" ("id","platform_id","name","version","codename","maker") VALUES (22,1,'SUSE','10.0','','SUSE');
INSERT INTO "platforms_operatingsystem" ("id","platform_id","name","version","codename","maker") VALUES (23,1,'SUSE','10.1','','SUSE');
INSERT INTO "platforms_operatingsystem" ("id","platform_id","name","version","codename","maker") VALUES (24,1,'SUSE','10.2','','SUSE');
INSERT INTO "platforms_operatingsystem" ("id","platform_id","name","version","codename","maker") VALUES (25,1,'Gentoo','2006.1','','');
INSERT INTO "platforms_operatingsystem" ("id","platform_id","name","version","codename","maker") VALUES (26,1,'Gentoo','2007.0','','');
INSERT INTO "platforms_operatingsystem" ("id","platform_id","name","version","codename","maker") VALUES (27,1,'Ubuntu','7.10','Gutsy Gibbon','Canonical');
INSERT INTO "platforms_operatingsystem" ("id","platform_id","name","version","codename","maker") VALUES (28,1,'Debian','Testing','Lenny','');
INSERT INTO "platforms_operatingsystem" ("id","platform_id","name","version","codename","maker") VALUES (29,1,'Ubuntu','8.04 LTS','Hardy Heron','Canonical');
INSERT INTO "platforms_operatingsystem" ("id","platform_id","name","version","codename","maker") VALUES (30,1,'Debian','Unstable','Sid','');
INSERT INTO "platforms_operatingsystem" ("id","platform_id","name","version","codename","maker") VALUES (31,4,'FreeBSD','6.3','','');
INSERT INTO "platforms_operatingsystem" ("id","platform_id","name","version","codename","maker") VALUES (32,4,'FreeBSD','7.0','','');
INSERT INTO "platforms_operatingsystem" ("id","platform_id","name","version","codename","maker") VALUES (33,4,'FreeBSD','7.1','','');
INSERT INTO "platforms_operatingsystem" ("id","platform_id","name","version","codename","maker") VALUES (34,4,'FreeBSD','5.5','','');
INSERT INTO "platforms_operatingsystem" ("id","platform_id","name","version","codename","maker") VALUES (35,4,'OpenBSD','4.2','','');
INSERT INTO "platforms_operatingsystem" ("id","platform_id","name","version","codename","maker") VALUES (36,4,'OpenBSD','4.1','','');
INSERT INTO "platforms_operatingsystem" ("id","platform_id","name","version","codename","maker") VALUES (37,4,'NetBSD','4.0','','');
INSERT INTO "platforms_operatingsystem" ("id","platform_id","name","version","codename","maker") VALUES (38,4,'NetBSD','3.1','','');
SELECT setval('platforms_operatingsystem_id_seq', (SELECT max("id") FROM "platforms_operatingsystem"));
