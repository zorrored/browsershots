COPY browsers_engine (id, name, maker) FROM stdin;
1	Gecko	
2	KHTML	
3	Opera	
4	AppleWebKit	
\.

SELECT 'browsers_engine' AS table_name,  setval('browsers_engine_id_seq', (SELECT max(id) FROM browsers_engine)) as pkey_max;
