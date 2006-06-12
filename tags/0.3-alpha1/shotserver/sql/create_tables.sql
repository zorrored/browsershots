DROP TABLE person CASCADE;
CREATE TABLE person (
person SERIAL PRIMARY KEY NOT NULL,
name VARCHAR(20) NOT NULL,
salt CHAR(4) NOT NULL CHECK (salt ~ '[0-9a-f]{4}'),
password CHAR(32) NOT NULL CHECK (password ~ '[0-9a-f]{32}'),
email VARCHAR(60) NOT NULL UNIQUE,
created TIMESTAMP DEFAULT NOW());

DROP TABLE engine CASCADE;
CREATE TABLE engine (
engine SERIAL PRIMARY KEY NOT NULL,
name VARCHAR(20) CHECK (name ~ '^\\w+$'),
created TIMESTAMP DEFAULT NOW(),
creator INT NOT NULL REFERENCES person);

DROP TABLE architecture CASCADE;
CREATE TABLE architecture (
architecture SERIAL PRIMARY KEY NOT NULL,
name VARCHAR(20) CHECK (name ~ '^\\w+$'),
created TIMESTAMP DEFAULT NOW(),
creator INT NOT NULL REFERENCES person);

DROP TABLE browser_group CASCADE;
CREATE TABLE browser_group (
browser_group SERIAL PRIMARY KEY NOT NULL,
name VARCHAR(20) NOT NULL UNIQUE CHECK (name ~ '^\\w+$'),
manufacturer VARCHAR(20),
terminal BOOLEAN NOT NULL DEFAULT FALSE,
created TIMESTAMP DEFAULT NOW(),
creator INT NOT NULL REFERENCES person);

DROP TABLE browser CASCADE;
CREATE TABLE browser (
browser SERIAL PRIMARY KEY NOT NULL,
useragent VARCHAR(255) NOT NULL UNIQUE,
browser_group INT NOT NULL REFERENCES browser_group,
major INT NOT NULL,
minor INT,
engine INT REFERENCES engine,
created TIMESTAMP DEFAULT NOW(),
creator INT NOT NULL REFERENCES person);

DROP TABLE opsys_group CASCADE;
CREATE TABLE opsys_group (
opsys_group SERIAL PRIMARY KEY NOT NULL,
name VARCHAR(20) NOT NULL,
manufacturer VARCHAR(20),
created TIMESTAMP DEFAULT NOW(),
creator INT NOT NULL REFERENCES person);

DROP TABLE opsys CASCADE;
CREATE TABLE opsys (
opsys SERIAL PRIMARY KEY NOT NULL,
opsys_group INT NOT NULL REFERENCES opsys_group,
distro VARCHAR(20),
codename VARCHAR(20),
major INT,
minor INT,
mobile BOOLEAN NOT NULL DEFAULT FALSE,
created TIMESTAMP DEFAULT NOW(),
creator INT NOT NULL REFERENCES person);

DROP TABLE factory CASCADE;
CREATE TABLE factory (
factory SERIAL PRIMARY KEY NOT NULL,
name VARCHAR(20) NOT NULL UNIQUE CHECK (name ~ '^\\w+$'),
salt CHAR(4) CHECK (salt ~ '[0-9a-f]{4}'),
password CHAR(32) CHECK (password ~ '[0-9a-f]{32}'),
owner INT NOT NULL REFERENCES person,
opsys INT NOT NULL REFERENCES opsys,
architecture INT NOT NULL REFERENCES architecture,
last_poll TIMESTAMP,
last_upload TIMESTAMP,
created TIMESTAMP DEFAULT NOW(),
creator INT NOT NULL REFERENCES person);

DROP TABLE factory_browser CASCADE;
CREATE TABLE factory_browser (
factory INT NOT NULL REFERENCES factory,
browser INT NOT NULL REFERENCES browser);

DROP TABLE factory_screen CASCADE;
CREATE TABLE factory_screen (
factory INT NOT NULL REFERENCES factory,
width INT NOT NULL,
height INT NOT NULL);

DROP TABLE factory_feature CASCADE;
CREATE TABLE factory_feature (
factory INT NOT NULL REFERENCES factory,
name VARCHAR(20) NOT NULL,
intval INT,
strval VARCHAR(20),
CONSTRAINT intval_or_strval CHECK (
(intval IS NULL AND strval IS NOT NULL) OR
(strval IS NULL AND intval IS NOT NULL)));

DROP TABLE screenshot CASCADE;
CREATE TABLE screenshot (
screenshot SERIAL PRIMARY KEY NOT NULL,
hashkey CHAR(32) UNIQUE NOT NULL CHECK (hashkey ~ '[0-9a-f]{32}'),
factory INT NOT NULL REFERENCES factory,
browser INT NOT NULL REFERENCES browser,
width INT NOT NULL,
height INT NOT NULL,
created TIMESTAMP DEFAULT NOW());

DROP TABLE website CASCADE;
CREATE TABLE website (
website SERIAL PRIMARY KEY NOT NULL,
url VARCHAR(255) NOT NULL UNIQUE,
created TIMESTAMP DEFAULT NOW());

DROP TABLE request_group CASCADE;
CREATE TABLE request_group (
request_group SERIAL PRIMARY KEY NOT NULL,
website INT NOT NULL,
width INT,
bpp INT,
js VARCHAR(20),
java VARCHAR(20),
flash VARCHAR(20),
media VARCHAR(20),
expire TIMESTAMP,
created TIMESTAMP DEFAULT NOW(),
creator INT REFERENCES person);

DROP TABLE request CASCADE;
CREATE TABLE request (
request SERIAL PRIMARY KEY NOT NULL,
request_group INT NOT NULL REFERENCES request_group,
browser_group INT NOT NULL REFERENCES browser_group,
major INT,
minor INT,
opsys_group INT REFERENCES opsys_group,
opsys INT REFERENCES opsys,
browser INT REFERENCES browser,
redirected TIMESTAMP,
screenshot INT REFERENCES screenshot);

DROP TABLE lock CASCADE;
CREATE TABLE lock (
request INT NOT NULL UNIQUE REFERENCES request,
factory INT NOT NULL REFERENCES factory,
created TIMESTAMP DEFAULT NOW());

DROP TABLE failure CASCADE;
CREATE TABLE failure (
request INT NOT NULL REFERENCES request,
factory INT NOT NULL REFERENCES factory,
message VARCHAR(255),
created TIMESTAMP DEFAULT NOW());

DROP TABLE nonce CASCADE;
CREATE TABLE nonce (
nonce CHAR(32) PRIMARY KEY NOT NULL CHECK (nonce ~ '[0-9a-f]{32}'),
ip CIDR NOT NULL,
factory INT REFERENCES factory,
person INT REFERENCES person,
request INT REFERENCES request,
created TIMESTAMP DEFAULT NOW());
