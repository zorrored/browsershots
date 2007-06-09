COPY platforms_architecture (id, name) FROM stdin;
1	i686
2	PPC
\.

SELECT 'platforms_architecture' AS table_name,  setval('platforms_architecture_id_seq', (SELECT max(id) FROM platforms_architecture)) as pkey_max;
