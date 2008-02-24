ALTER TABLE factories_screensize
DROP CONSTRAINT factories_screensize_factory_id_fkey;
ALTER TABLE factories_screensize
ADD CONSTRAINT factories_screensize_factory_id_fkey
FOREIGN KEY (factory_id) REFERENCES factories_factory(id)
ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;
