COPY factories_operatingsystemgroup (id, name, maker) FROM stdin;
1	Linux	
2	Mac OS	Apple
3	Windows	Microsoft
4	Palm OS	
5	Symbian	
6	Solaris	
7	TOS	
\.

SELECT 'factories_operatingsystemgroup' AS table_name,  setval('factories_operatingsystemgroup_id_seq', (SELECT max(id) FROM factories_operatingsystemgroup)) as pkey_max;
