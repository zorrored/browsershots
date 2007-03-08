COPY factories_architecture (id, name) FROM stdin;
1	i386
2	PPC
3	68000
4	Palm
5	AMD64
\.

SELECT 'factories_architecture' AS table_name,  setval('factories_architecture_id_seq', (SELECT max(id) FROM factories_architecture)) as pkey_max;
