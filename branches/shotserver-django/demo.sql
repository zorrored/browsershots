INSERT INTO factories_operatingsystemgroup
  (name, maker) VALUES
  ('Linux', '');
INSERT INTO factories_operatingsystem
  (operatingsystemgroup_id, distro, version, codename) VALUES
  (1, 'Ubuntu', '6.06 LTS', 'Dapper Drake');

INSERT INTO factories_operatingsystemgroup
  (name, maker) VALUES
  ('Mac OS', 'Apple');
INSERT INTO factories_operatingsystem
  (operatingsystemgroup_id, distro, version, codename) VALUES
  (2, 'X', '10.4', 'Tiger');

INSERT INTO factories_operatingsystemgroup
  (name, maker) VALUES
  ('Windows', 'Microsoft');
INSERT INTO factories_operatingsystem
  (operatingsystemgroup_id, distro, version, codename) VALUES
  (3, 'NT', '5.1', 'XP');


INSERT INTO factories_factory
  (name, architecture, operatingsystem_id, admin_id, created) VALUES
  ('argo', 'i386', 1, 1, NOW());
INSERT INTO factories_screensize
  (factory_id, width, height) VALUES
  (1, 800, 600);
INSERT INTO factories_screensize
  (factory_id, width, height) VALUES
  (1, 1024, 768);

INSERT INTO factories_factory
  (name, architecture, operatingsystem_id, admin_id, created) VALUES
  ('runt', 'PPC', 2, 1, NOW());
INSERT INTO factories_screensize
  (factory_id, width, height) VALUES
  (2, 1024, 768);
INSERT INTO browsers_browsergroup
  (name, maker, terminal) VALUES
  ('Firefox', 'Mozilla', False);
INSERT INTO browsers_engine
  (name, maker) VALUES
  ('Gecko', 'Mozilla');
INSERT INTO browsers_browser
  (factory_id, user_agent, browser_group_id, version, major, minor,
   engine_id, engine_version) VALUES
  (1, '', 1, '2.0', 2, 0, 1, '20070216');
