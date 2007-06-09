COPY platforms_platform (id, name, position) FROM stdin;
1	Linux	1
2	Mac OS	3
3	Windows	2
\.

SELECT 'platforms_platform' AS table_name,  setval('platforms_platform_id_seq', (SELECT max(id) FROM platforms_platform)) as pkey_max;
