INSERT INTO "features_java" ("id","version") VALUES (1,'disabled');
INSERT INTO "features_java" ("id","version") VALUES (2,'enabled');
INSERT INTO "features_java" ("id","version") VALUES (3,'1.3');
INSERT INTO "features_java" ("id","version") VALUES (4,'1.4');
INSERT INTO "features_java" ("id","version") VALUES (5,'1.5');
INSERT INTO "features_java" ("id","version") VALUES (6,'1.6');
SELECT setval('features_java_id_seq', (SELECT max("id") FROM "features_java"));
