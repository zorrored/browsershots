INSERT INTO "platforms_architecture" ("id","name") VALUES (1,'i686');
INSERT INTO "platforms_architecture" ("id","name") VALUES (2,'PPC');
SELECT setval('platforms_architecture_id_seq', (SELECT max("id") FROM "platforms_architecture"));
