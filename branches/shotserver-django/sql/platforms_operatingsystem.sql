COPY platforms_operatingsystem (id, platform_id, name, version, codename, maker) FROM stdin;
1	1	Debian	3.1	Sarge	
2	1	Debian	3.2	Etch	
3	1	PLD	2.0	Ac	
4	1	Gentoo	2006.0		
5	1	Ubuntu	5.10	Breezy Badger	Canonical
6	1	Ubuntu	6.06	Dapper Drake	Canonical
7	1	Ubuntu	6.10	Edgy Eft	Canonical
8	1	Ubuntu	7.04	Feisty Fawn	Canonical
9	2	Mac OS X	10.3	Jaguar	Apple
10	2	Mac OS X	10.4	Tiger	Apple
11	2	Mac OS X	10.5	Leopard	Apple
12	3	Windows	98		Microsoft
13	3	Windows	ME		Microsoft
14	3	Windows	XP		Microsoft
15	3	Windows	2003	Server	Microsoft
16	3	Windows	Vista		Microsoft
\.

SELECT 'platforms_operatingsystem' AS table_name,  setval('platforms_operatingsystem_id_seq', (SELECT max(id) FROM platforms_operatingsystem)) as pkey_max;
