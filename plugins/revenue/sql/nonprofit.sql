INSERT INTO "revenue_nonprofit" ("id","name","url") VALUES (1,'Python Software Foundation','http://www.python.org/psf/');
INSERT INTO "revenue_nonprofit" ("id","name","url") VALUES (2,'Free Software Foundation','http://www.fsf.org/');
INSERT INTO "revenue_nonprofit" ("id","name","url") VALUES (3,'Free Software Foundation Europe','http://www.fsfeurope.org/');
SELECT setval('revenue_nonprofit_id_seq', (SELECT max("id") FROM "revenue_nonprofit"));
