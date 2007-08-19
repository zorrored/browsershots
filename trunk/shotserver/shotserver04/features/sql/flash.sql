INSERT INTO "features_flash" ("id","version") VALUES (1,'disabled');
INSERT INTO "features_flash" ("id","version") VALUES (2,'enabled');
INSERT INTO "features_flash" ("id","version") VALUES (3,'5');
INSERT INTO "features_flash" ("id","version") VALUES (4,'6');
INSERT INTO "features_flash" ("id","version") VALUES (5,'7');
INSERT INTO "features_flash" ("id","version") VALUES (6,'8');
INSERT INTO "features_flash" ("id","version") VALUES (7,'9');
SELECT setval('features_flash_id_seq', (SELECT max("id") FROM "features_flash"));
