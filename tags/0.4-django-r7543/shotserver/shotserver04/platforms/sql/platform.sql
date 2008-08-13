INSERT INTO "platforms_platform" ("id","name","position") VALUES (1,'Linux',1);
INSERT INTO "platforms_platform" ("id","name","position") VALUES (2,'Mac OS',3);
INSERT INTO "platforms_platform" ("id","name","position") VALUES (3,'Windows',2);
INSERT INTO "platforms_platform" ("id","name","position") VALUES (4,'BSD',4);
SELECT setval('platforms_platform_id_seq', (SELECT max("id") FROM "platforms_platform"));
