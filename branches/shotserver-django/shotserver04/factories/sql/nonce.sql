ALTER TABLE factories_nonce
ADD CONSTRAINT factories_nonce_hashkey_check
CHECK (hashkey ~ '^[0-9a-f]{32}$');
