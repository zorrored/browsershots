ALTER TABLE factories_colordepth
DROP CONSTRAINT factories_colordepth_factory_id_fkey;
ALTER TABLE factories_colordepth
ADD CONSTRAINT factories_colordepth_factory_id_fkey
FOREIGN KEY (factory_id) REFERENCES factories_factory(id)
ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;
