COPY browsers_engine (id, name, maker) FROM stdin;
1	Gecko	Mozilla
2	KHTML	KDE
3	Opera	Opera
4	AppleWebKit	Apple
\.

SELECT 'browsers_engine' AS table_name,  setval('browsers_engine_id_seq', (SELECT max(id) FROM browsers_engine)) as pkey_max;
