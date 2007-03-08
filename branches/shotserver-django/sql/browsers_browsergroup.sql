COPY browsers_browsergroup (id, name, maker, terminal) FROM stdin;
1	Firefox	Mozilla	f
2	Safari	Apple	f
3	MSIE	Microsoft	f
4	Konqueror	KDE	f
5	Galeon		f
6	Mozilla	Mozilla	f
7	Epiphany		f
8	Opera	Opera	f
9	Camino		f
10	Links		t
11	Lynx		t
12	W3M		t
13	NetFront		f
14	WebToGo		f
15	EudoraWeb		f
16	SeaMonkey	Mozilla	f
17	Flock	Mozilla	f
18	Navigator	Netscape	f
19	BonEcho	Mozilla	f
20	Phoenix	Mozilla	f
21	Firebird	Mozilla	f
22	Dillo		f
25	K-Meleon		f
26	Netscape	Netscape	f
27	Kazehakase		f
28	Iceweasel	GNU	f
\.

SELECT 'browsers_browsergroup' AS table_name,  setval('browsers_browsergroup_id_seq', (SELECT max(id) FROM browsers_browsergroup)) as pkey_max;
