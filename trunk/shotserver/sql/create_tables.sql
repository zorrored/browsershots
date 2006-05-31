DROP TABLE person CASCADE;
CREATE TABLE person (
person SERIAL PRIMARY KEY NOT NULL,
name VARCHAR(20) NOT NULL UNIQUE,
email VARCHAR(60) NOT NULL UNIQUE,
created TIMESTAMP DEFAULT NOW());

DROP TABLE engine CASCADE;
CREATE TABLE engine (
engine SERIAL PRIMARY KEY NOT NULL,
name VARCHAR(20),
created TIMESTAMP DEFAULT NOW(),
creator INT NOT NULL REFERENCES person);

DROP TABLE architecture CASCADE;
CREATE TABLE architecture (
architecture SERIAL PRIMARY KEY NOT NULL,
name VARCHAR(20),
created TIMESTAMP DEFAULT NOW(),
creator INT NOT NULL REFERENCES person);

DROP TABLE browser CASCADE;
CREATE TABLE browser (
browser SERIAL PRIMARY KEY NOT NULL,
name VARCHAR(20) NOT NULL UNIQUE,
manufacturer VARCHAR(20),
terminal BOOLEAN NOT NULL DEFAULT FALSE,
created TIMESTAMP DEFAULT NOW(),
creator INT NOT NULL REFERENCES person);

DROP TABLE browser_version CASCADE;
CREATE TABLE browser_version (
browser_version SERIAL PRIMARY KEY NOT NULL,
browser INT NOT NULL REFERENCES browser,
major INT NOT NULL,
minor INT,
engine INT REFERENCES engine,
created TIMESTAMP DEFAULT NOW(),
creator INT NOT NULL REFERENCES person);

DROP TABLE opsys CASCADE;
CREATE TABLE opsys (
opsys SERIAL PRIMARY KEY NOT NULL,
name VARCHAR(20) NOT NULL,
manufacturer VARCHAR(20),
created TIMESTAMP DEFAULT NOW(),
creator INT NOT NULL REFERENCES person);

DROP TABLE opsys_version CASCADE;
CREATE TABLE opsys_version (
opsys_version SERIAL PRIMARY KEY NOT NULL,
opsys INT NOT NULL REFERENCES opsys,
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
name VARCHAR(20) NOT NULL UNIQUE,
opsys_version INT NOT NULL REFERENCES opsys_version,
architecture INT NOT NULL REFERENCES architecture,
created TIMESTAMP DEFAULT NOW(),
creator INT NOT NULL REFERENCES person,
last_poll TIMESTAMP,
last_upload TIMESTAMP);

DROP TABLE factory_browser CASCADE;
CREATE TABLE factory_browser (
factory INT NOT NULL REFERENCES factory,
browser_version INT NOT NULL REFERENCES browser_version);

DROP TABLE factory_screen CASCADE;
CREATE TABLE factory_screen (
factory INT NOT NULL REFERENCES factory,
width INT NOT NULL,
height INT NOT NULL);

DROP TABLE factory_feature CASCADE;
CREATE TABLE factory_feature (
factory INT NOT NULL REFERENCES factory,
name CHAR(8) NOT NULL,
intval INT,
strval CHAR(16));

DROP TABLE screenshot CASCADE;
CREATE TABLE screenshot (
screenshot SERIAL PRIMARY KEY NOT NULL,
factory INT NOT NULL REFERENCES factory,
width INT NOT NULL,
height INT NOT NULL,
created TIMESTAMP DEFAULT NOW());

DROP TABLE website CASCADE;
CREATE TABLE website (
website SERIAL PRIMARY KEY NOT NULL,
url VARCHAR(255) NOT NULL UNIQUE,
created TIMESTAMP DEFAULT NOW());

DROP TABLE request CASCADE;
CREATE TABLE request (
request SERIAL PRIMARY KEY NOT NULL,
website INT NOT NULL,
bpp INT,
js CHAR(4),
java CHAR(16),
flash CHAR(16),
media CHAR(16),
expire INT,
created TIMESTAMP DEFAULT NOW(),
creator INT REFERENCES person);

DROP TABLE request_browser CASCADE;
CREATE TABLE request_browser (
request INT NOT NULL REFERENCES request,
browser INT NOT NULL REFERENCES browser,
browser_version INT,
major INT,
minor INT,
width INT,
opsys INT,
opsys_version INT,
screenshot INT REFERENCES screenshot);

DROP TABLE lock CASCADE;
CREATE TABLE lock (
request INT NOT NULL REFERENCES request,
factory INT NOT NULL REFERENCES factory,
created TIMESTAMP DEFAULT NOW());
