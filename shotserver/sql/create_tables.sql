CREATE TABLE browser (
id SERIAL PRIMARY KEY NOT NULL,
name VARCHAR(20) NOT NULL UNIQUE,
manufacturer VARCHAR(20));

CREATE TABLE browser_version (
id SERIAL PRIMARY KEY NOT NULL,
browser INT NOT NULL,
major INT,
minor INT,
engine VARCHAR(20),
FOREIGN KEY (browser) REFERENCES browser);

CREATE TABLE os (
id SERIAL PRIMARY KEY NOT NULL,
name VARCHAR(20) NOT NULL,
distro VARCHAR(20) NOT NULL,
version VARCHAR(20) NOT NULL,
major INT,
minor INT,
manufacturer VARCHAR(20));

CREATE TABLE factory (
id SERIAL PRIMARY KEY NOT NULL,
name VARCHAR(20) NOT NULL UNIQUE,
os INT NOT NULL,
FOREIGN KEY (os) REFERENCES os);

CREATE TABLE factory_browser (
factory INT NOT NULL,
browser_version INT NOT NULL,
FOREIGN KEY (factory) REFERENCES factory,
FOREIGN KEY (browser_version) REFERENCES browser_version);

CREATE TABLE factory_resolution (
factory INT NOT NULL,
width INT NOT NULL,
height INT NOT NULL,
FOREIGN KEY (factory) REFERENCES factory);

CREATE TABLE screenshot (
id SERIAL PRIMARY KEY NOT NULL,
factory INT NOT NULL,
width INT NOT NULL,
height INT NOT NULL,
FOREIGN KEY (factory) REFERENCES factory);

CREATE TABLE website (
id SERIAL PRIMARY KEY NOT NULL,
url VARCHAR(255) NOT NULL UNIQUE CHECK (url LIKE 'http://%'));

CREATE TABLE job (
website INT NOT NULL,
browser INT NOT NULL,
browser_major INT,
browser_minor INT,
width INT,

screenshot INT,
submitted TIMESTAMP,
FOREIGN KEY (browser) REFERENCES browser,
FOREIGN KEY (screenshot) REFERENCES screenshot);
