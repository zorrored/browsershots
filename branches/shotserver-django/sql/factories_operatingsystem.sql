COPY factories_operatingsystem (id, operating_system_group_id, distro, version, codename, mobile) FROM stdin;
1	1	Ubuntu	6.6	Dapper	f
2	2	X	10.4	Tiger	f
3	3	NT	5.1	XP	f
4	4		6.1	Cobalt	t
5	5		6.1		t
6	6		5.8		f
7	7		2.6		f
8	1	Debian	3.1	Sarge	f
9	1	PLD	2.0	Ac	f
11	1	Gentoo	2006.0		f
12	3	98			f
13	3	ME			f
14	1	Kubuntu	6.4	Dapper	f
15	3	NT	6.0	Vista	f
16	1	Ubuntu	5.10	Breezy	f
17	1	Debian	3.2	Etch	f
18	1	Ubuntu	6.10	Edgy	f
19	3	2003		Server	f
20	2	X	10.5	Leopard	f
\.

SELECT 'factories_operatingsystem' AS table_name,  setval('factories_operatingsystem_id_seq', (SELECT max(id) FROM factories_operatingsystem)) as pkey_max;
