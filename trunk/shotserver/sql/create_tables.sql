CREATE TABLE person (
person SERIAL PRIMARY KEY NOT NULL,
person_name VARCHAR(20) NOT NULL UNIQUE,
person_email VARCHAR(60) NOT NULL UNIQUE);

CREATE TABLE browser (
browser SERIAL PRIMARY KEY NOT NULL,
browser_name VARCHAR(20) NOT NULL UNIQUE,
browser_manufacturer VARCHAR(20));

CREATE TABLE browser_version (
browser_version SERIAL PRIMARY KEY NOT NULL,
browser INT NOT NULL,
browser_major INT,
browser_minor INT,
browser_engine VARCHAR(20),
FOREIGN KEY (browser) REFERENCES browser);

CREATE TABLE os (
os SERIAL PRIMARY KEY NOT NULL,
os_name VARCHAR(20) NOT NULL,
os_manufacturer VARCHAR(20));

CREATE TABLE os_version (
os_version SERIAL PRIMARY KEY NOT NULL,
os INT NOT NULL,
os_distro VARCHAR(20) NOT NULL,
os_codename VARCHAR(20) NOT NULL,
os_major INT,
os_minor INT,
FOREIGN KEY (os) REFERENCES os);

CREATE TABLE factory (
factory SERIAL PRIMARY KEY NOT NULL,
factory_name VARCHAR(20) NOT NULL UNIQUE,
factory_admin INT NOT NULL,
os_version INT NOT NULL,
factory_added TIMESTAMP DEFAULT NOW(),
factory_last_polled TIMESTAMP,
factory_last_uploaded TIMESTAMP,
FOREIGN KEY (factory_admin) REFERENCES person,
FOREIGN KEY (os_version) REFERENCES os_version);

CREATE TABLE factory_browser (
factory INT NOT NULL,
browser_version INT NOT NULL,
FOREIGN KEY (factory) REFERENCES factory,
FOREIGN KEY (browser_version) REFERENCES browser_version);

CREATE TABLE factory_screen (
factory INT NOT NULL,
screen_width INT NOT NULL,
screen_height INT NOT NULL,
FOREIGN KEY (factory) REFERENCES factory);

CREATE TABLE screenshot (
screenshot SERIAL PRIMARY KEY NOT NULL,
factory INT NOT NULL,
screenshot_width INT NOT NULL,
screenshot_height INT NOT NULL,
screenshot_uploaded TIMESTAMP DEFAULT NOW(),
FOREIGN KEY (factory) REFERENCES factory);

CREATE TABLE website (
website SERIAL PRIMARY KEY NOT NULL,
website_url VARCHAR(255) NOT NULL UNIQUE CHECK (website_url LIKE 'http://%'),
website_first_submitted TIMESTAMP DEFAULT NOW());

CREATE TABLE request (
request SERIAL PRIMARY KEY NOT NULL,
website INT NOT NULL,
request_browser INT NOT NULL,
request_major INT,
request_minor INT,
request_width INT,
request_os INT,
screenshot INT,
request_submitted TIMESTAMP DEFAULT NOW(),
FOREIGN KEY (request_browser) REFERENCES browser,
FOREIGN KEY (screenshot) REFERENCES screenshot);

CREATE TABLE lock (
request INT NOT NULL,
factory INT NOT NULL,
locked TIMESTAMP DEFAULT NOW(),
FOREIGN KEY (request) REFERENCES request,
FOREIGN KEY (factory) REFERENCES factory);
