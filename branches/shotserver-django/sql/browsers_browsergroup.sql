COPY browsers_browsergroup (id, name, maker, terminal) FROM stdin;
1	Firefox	Mozilla	f
2	Safari	Apple	f
3	Internet Explorer	Microsoft	f
4	Konqueror	KDE	f
5	Galeon		f
6	Mozilla	Mozilla	f
7	Epiphany		f
8	Opera	Opera	f
9	Camino		f
10	Links		t
11	Lynx		t
12	W3M		t
13	SeaMonkey	Mozilla	f
14	Flock	Mozilla	f
15	Navigator	Netscape	f
16	Phoenix	Mozilla	f
17	Firebird	Mozilla	f
18	Dillo		f
19	Netscape	Netscape	f
20	Iceweasel	GNU	f
\.

SELECT 'browsers_browsergroup' AS table_name,  setval('browsers_browsergroup_id_seq', (SELECT max(id) FROM browsers_browsergroup)) as pkey_max;
