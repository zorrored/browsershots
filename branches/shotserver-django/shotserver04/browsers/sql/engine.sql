INSERT INTO "browsers_engine" ("id","name","maker") VALUES (1,'Gecko','Mozilla');
INSERT INTO "browsers_engine" ("id","name","maker") VALUES (2,'KHTML','KDE');
INSERT INTO "browsers_engine" ("id","name","maker") VALUES (3,'Opera','Opera');
INSERT INTO "browsers_engine" ("id","name","maker") VALUES (4,'AppleWebKit','Apple');
SELECT setval('browsers_engine_id_seq', (SELECT max("id") FROM "browsers_engine"));
