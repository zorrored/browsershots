CREATE TABLE person (
person SERIAL PRIMARY KEY NOT NULL,
name VARCHAR(20) NOT NULL UNIQUE,
email VARCHAR(60) NOT NULL UNIQUE,
created TIMESTAMP DEFAULT NOW());

CREATE TABLE engine (
engine SERIAL PRIMARY KEY NOT NULL,
name VARCHAR(20),
created TIMESTAMP DEFAULT NOW(),
creator INT NOT NULL REFERENCES person);

CREATE TABLE architecture (
architecture SERIAL PRIMARY KEY NOT NULL,
name VARCHAR(20),
created TIMESTAMP DEFAULT NOW(),
creator INT NOT NULL REFERENCES person);

CREATE TABLE browser (
browser SERIAL PRIMARY KEY NOT NULL,
name VARCHAR(20) NOT NULL UNIQUE,
manufacturer VARCHAR(20),
terminal BOOLEAN NOT NULL DEFAULT FALSE,
created TIMESTAMP DEFAULT NOW(),
creator INT NOT NULL REFERENCES person);

CREATE TABLE browser_version (
browser_version SERIAL PRIMARY KEY NOT NULL,
browser INT NOT NULL REFERENCES browser,
major INT NOT NULL,
minor INT,
engine INT REFERENCES engine,
created TIMESTAMP DEFAULT NOW(),
creator INT NOT NULL REFERENCES person);

CREATE TABLE platform (
platform SERIAL PRIMARY KEY NOT NULL,
name VARCHAR(20) NOT NULL,
manufacturer VARCHAR(20),
created TIMESTAMP DEFAULT NOW(),
creator INT NOT NULL REFERENCES person);

CREATE TABLE platform_version (
platform_version SERIAL PRIMARY KEY NOT NULL,
platform INT NOT NULL REFERENCES platform,
distro VARCHAR(20),
codename VARCHAR(20),
major INT,
minor INT,
mobile BOOLEAN NOT NULL DEFAULT FALSE,
created TIMESTAMP DEFAULT NOW(),
creator INT NOT NULL REFERENCES person);

CREATE TABLE factory (
factory SERIAL PRIMARY KEY NOT NULL,
name VARCHAR(20) NOT NULL UNIQUE,
platform_version INT NOT NULL REFERENCES platform_version,
architecture INT NOT NULL REFERENCES architecture,
created TIMESTAMP DEFAULT NOW(),
creator INT NOT NULL REFERENCES person,
last_poll TIMESTAMP,
last_upload TIMESTAMP);

CREATE TABLE factory_browser (
factory INT NOT NULL REFERENCES factory,
browser_version INT NOT NULL REFERENCES browser_version);

CREATE TABLE factory_screen (
factory INT NOT NULL REFERENCES factory,
width INT NOT NULL,
height INT NOT NULL);

CREATE TABLE factory_feature (
factory INT NOT NULL REFERENCES factory,
name CHAR(8) NOT NULL,
intval INT,
strval CHAR(16));

CREATE TABLE screenshot (
screenshot SERIAL PRIMARY KEY NOT NULL,
factory INT NOT NULL REFERENCES factory,
width INT NOT NULL,
height INT NOT NULL,
created TIMESTAMP DEFAULT NOW());

CREATE TABLE website (
website SERIAL PRIMARY KEY NOT NULL,
url VARCHAR(255) NOT NULL UNIQUE,
created TIMESTAMP DEFAULT NOW());

CREATE TABLE request (
request SERIAL PRIMARY KEY NOT NULL,
website INT NOT NULL,
width INT,
bpp INT,
js CHAR(4),
java CHAR(16),
flash CHAR(16),
media CHAR(16),
expire INT,
created TIMESTAMP DEFAULT NOW(),
creator INT REFERENCES person);

CREATE TABLE request_browser (
request INT NOT NULL REFERENCES request,
browser INT NOT NULL REFERENCES browser,
browser_version INT,
major INT,
minor INT,
platform INT,
platform_version INT,
screenshot INT REFERENCES screenshot);

CREATE TABLE lock (
request INT NOT NULL REFERENCES request,
factory INT NOT NULL REFERENCES factory,
created TIMESTAMP DEFAULT NOW());
