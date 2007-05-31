--
-- PostgreSQL database dump
--

SET client_encoding = 'SQL_ASCII';
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA public IS 'Standard public schema';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: architecture; Type: TABLE; Schema: public; Owner: www-data; Tablespace: 
--

CREATE TABLE architecture (
    architecture serial NOT NULL,
    name character varying(20),
    created timestamp without time zone DEFAULT now(),
    creator integer NOT NULL,
    CONSTRAINT architecture_name_check CHECK (((name)::text ~ E'^\\w+$'::text))
);


--
-- Name: browser_group; Type: TABLE; Schema: public; Owner: www-data; Tablespace: 
--

CREATE TABLE browser_group (
    browser_group serial NOT NULL,
    name character varying(20) NOT NULL,
    manufacturer character varying(20),
    terminal boolean DEFAULT false NOT NULL,
    created timestamp without time zone DEFAULT now(),
    creator integer NOT NULL,
    "scroll" character varying(40),
    CONSTRAINT browser_group_name_check CHECK (((name)::text ~ E'^[\\w\\-]+$'::text))
);


--
-- Name: request; Type: TABLE; Schema: public; Owner: www-data; Tablespace: 
--

CREATE TABLE request (
    request serial NOT NULL,
    request_group integer NOT NULL,
    browser_group integer NOT NULL,
    major integer,
    minor integer,
    opsys_group integer,
    opsys integer,
    redirected timestamp without time zone,
    screenshot integer,
    locked timestamp without time zone,
    factory integer,
    priority integer DEFAULT 0 NOT NULL,
    factory_browser integer
);


--
-- Name: browser_stats; Type: VIEW; Schema: public; Owner: www-data
--

CREATE VIEW browser_stats AS
    SELECT browser_group.name, count(*) AS queued FROM (request JOIN browser_group USING (browser_group)) WHERE (request.screenshot IS NULL) GROUP BY browser_group.name;


--
-- Name: engine; Type: TABLE; Schema: public; Owner: www-data; Tablespace: 
--

CREATE TABLE engine (
    engine serial NOT NULL,
    name character varying(20),
    created timestamp without time zone DEFAULT now(),
    creator integer NOT NULL,
    CONSTRAINT engine_name_check CHECK (((name)::text ~ E'^\\w+$'::text))
);


--
-- Name: factory; Type: TABLE; Schema: public; Owner: www-data; Tablespace: 
--

CREATE TABLE factory (
    factory serial NOT NULL,
    name character varying(20) NOT NULL,
    salt character(4),
    "password" character(32),
    "owner" integer NOT NULL,
    opsys integer NOT NULL,
    architecture integer NOT NULL,
    last_poll timestamp without time zone,
    last_upload timestamp without time zone,
    created timestamp without time zone DEFAULT now(),
    creator integer NOT NULL,
    per_hour integer,
    per_day integer,
    CONSTRAINT factory_name_check CHECK (((name)::text ~ '^[a-z][a-z0-9_-]+[a-z0-9]$'::text)),
    CONSTRAINT factory_password_check CHECK (("password" ~ '[0-9a-f]{32}'::text)),
    CONSTRAINT factory_salt_check CHECK ((salt ~ '[0-9a-f]{4}'::text))
);


--
-- Name: factory_bpp; Type: TABLE; Schema: public; Owner: www-data; Tablespace: 
--

CREATE TABLE factory_bpp (
    factory integer NOT NULL,
    bpp integer NOT NULL
);


--
-- Name: factory_browser; Type: TABLE; Schema: public; Owner: www-data; Tablespace: 
--

CREATE TABLE factory_browser (
    factory integer NOT NULL,
    last_upload timestamp without time zone,
    user_agent character varying(255),
    command character varying(255),
    disabled timestamp without time zone,
    factory_browser serial NOT NULL,
    major integer NOT NULL,
    minor integer NOT NULL,
    engine integer,
    browser_group integer NOT NULL,
    created timestamp without time zone DEFAULT now(),
    creator integer NOT NULL,
    version character varying(20) NOT NULL,
    engine_version character varying(20),
    java character varying(10),
    js character varying(10),
    flash character varying(10),
    CONSTRAINT user_agent_engine_version CHECK (((user_agent)::text ~ (engine_version)::text)),
    CONSTRAINT user_agent_version CHECK ((((user_agent)::text ~ (version)::text) OR ((user_agent)::text ~ 'Safari'::text))),
    CONSTRAINT version_major_minor CHECK (((version)::text ~ (((major)::text || '.0?'::text) || (minor)::text)))
);


--
-- Name: factory_feature; Type: TABLE; Schema: public; Owner: www-data; Tablespace: 
--

CREATE TABLE factory_feature (
    factory integer NOT NULL,
    name character varying(20) NOT NULL,
    intval integer,
    strval character varying(20),
    CONSTRAINT intval_or_strval CHECK ((((intval IS NULL) AND (strval IS NOT NULL)) OR ((strval IS NULL) AND (intval IS NOT NULL))))
);


--
-- Name: factory_screen; Type: TABLE; Schema: public; Owner: www-data; Tablespace: 
--

CREATE TABLE factory_screen (
    factory integer NOT NULL,
    width integer NOT NULL,
    height integer NOT NULL
);


--
-- Name: failure; Type: TABLE; Schema: public; Owner: www-data; Tablespace: 
--

CREATE TABLE failure (
    request integer NOT NULL,
    factory integer NOT NULL,
    message character varying(255),
    created timestamp without time zone DEFAULT now()
);


--
-- Name: nonce; Type: TABLE; Schema: public; Owner: www-data; Tablespace: 
--

CREATE TABLE nonce (
    nonce character(32) NOT NULL,
    ip cidr NOT NULL,
    factory integer,
    person integer,
    request integer,
    created timestamp without time zone DEFAULT now(),
    CONSTRAINT nonce_nonce_check CHECK ((nonce ~ '[0-9a-f]{32}'::text))
);


--
-- Name: opsys; Type: TABLE; Schema: public; Owner: www-data; Tablespace: 
--

CREATE TABLE opsys (
    opsys serial NOT NULL,
    opsys_group integer NOT NULL,
    distro character varying(20),
    codename character varying(20),
    major integer,
    minor integer,
    mobile boolean DEFAULT false NOT NULL,
    created timestamp without time zone DEFAULT now(),
    creator integer NOT NULL
);


--
-- Name: opsys_group; Type: TABLE; Schema: public; Owner: www-data; Tablespace: 
--

CREATE TABLE opsys_group (
    opsys_group serial NOT NULL,
    name character varying(20) NOT NULL,
    manufacturer character varying(20),
    created timestamp without time zone DEFAULT now(),
    creator integer NOT NULL
);


--
-- Name: person; Type: TABLE; Schema: public; Owner: www-data; Tablespace: 
--

CREATE TABLE person (
    person serial NOT NULL,
    salt character(4) NOT NULL,
    "password" character(32) NOT NULL,
    email character varying(60) NOT NULL,
    created timestamp without time zone DEFAULT now(),
    nickname character varying(20) NOT NULL,
    name character varying(40) NOT NULL,
    htpasswd character(37),
    CONSTRAINT person_nickname_check CHECK (((nickname)::text ~ '[a-z][0-9a-z]*'::text)),
    CONSTRAINT person_password_check CHECK (("password" ~ '[0-9a-f]{32}'::text)),
    CONSTRAINT person_salt_check CHECK ((salt ~ '[0-9a-f]{4}'::text))
);


--
-- Name: priority_domain; Type: TABLE; Schema: public; Owner: www-data; Tablespace: 
--

CREATE TABLE priority_domain (
    "domain" character varying(255) NOT NULL,
    expire timestamp without time zone,
    priority integer
);


--
-- Name: request_group; Type: TABLE; Schema: public; Owner: www-data; Tablespace: 
--

CREATE TABLE request_group (
    request_group serial NOT NULL,
    website integer NOT NULL,
    width integer,
    bpp integer,
    js character varying(20),
    java character varying(20),
    flash character varying(20),
    media character varying(20),
    expire timestamp without time zone,
    created timestamp without time zone DEFAULT now(),
    creator integer
);


--
-- Name: screenshot; Type: TABLE; Schema: public; Owner: www-data; Tablespace: 
--

CREATE TABLE screenshot (
    screenshot serial NOT NULL,
    hashkey character(32) NOT NULL,
    factory integer NOT NULL,
    width integer NOT NULL,
    height integer NOT NULL,
    created timestamp without time zone DEFAULT now(),
    factory_browser integer,
    CONSTRAINT screenshot_hashkey_check CHECK ((hashkey ~ '[0-9a-f]{32}'::text))
);


--
-- Name: website; Type: TABLE; Schema: public; Owner: www-data; Tablespace: 
--

CREATE TABLE website (
    website serial NOT NULL,
    url character varying(255) NOT NULL,
    created timestamp without time zone DEFAULT now()
);


--
-- Name: architecture_pkey; Type: CONSTRAINT; Schema: public; Owner: www-data; Tablespace: 
--

ALTER TABLE ONLY architecture
    ADD CONSTRAINT architecture_pkey PRIMARY KEY (architecture);


--
-- Name: browser_group_name_key; Type: CONSTRAINT; Schema: public; Owner: www-data; Tablespace: 
--

ALTER TABLE ONLY browser_group
    ADD CONSTRAINT browser_group_name_key UNIQUE (name);


--
-- Name: browser_group_pkey; Type: CONSTRAINT; Schema: public; Owner: www-data; Tablespace: 
--

ALTER TABLE ONLY browser_group
    ADD CONSTRAINT browser_group_pkey PRIMARY KEY (browser_group);


--
-- Name: engine_pkey; Type: CONSTRAINT; Schema: public; Owner: www-data; Tablespace: 
--

ALTER TABLE ONLY engine
    ADD CONSTRAINT engine_pkey PRIMARY KEY (engine);


--
-- Name: factory_browser_pkey; Type: CONSTRAINT; Schema: public; Owner: www-data; Tablespace: 
--

ALTER TABLE ONLY factory_browser
    ADD CONSTRAINT factory_browser_pkey PRIMARY KEY (factory_browser);


--
-- Name: factory_name_key; Type: CONSTRAINT; Schema: public; Owner: www-data; Tablespace: 
--

ALTER TABLE ONLY factory
    ADD CONSTRAINT factory_name_key UNIQUE (name);


--
-- Name: factory_pkey; Type: CONSTRAINT; Schema: public; Owner: www-data; Tablespace: 
--

ALTER TABLE ONLY factory
    ADD CONSTRAINT factory_pkey PRIMARY KEY (factory);


--
-- Name: nonce_pkey; Type: CONSTRAINT; Schema: public; Owner: www-data; Tablespace: 
--

ALTER TABLE ONLY nonce
    ADD CONSTRAINT nonce_pkey PRIMARY KEY (nonce);


--
-- Name: opsys_group_pkey; Type: CONSTRAINT; Schema: public; Owner: www-data; Tablespace: 
--

ALTER TABLE ONLY opsys_group
    ADD CONSTRAINT opsys_group_pkey PRIMARY KEY (opsys_group);


--
-- Name: opsys_pkey; Type: CONSTRAINT; Schema: public; Owner: www-data; Tablespace: 
--

ALTER TABLE ONLY opsys
    ADD CONSTRAINT opsys_pkey PRIMARY KEY (opsys);


--
-- Name: person_email_key; Type: CONSTRAINT; Schema: public; Owner: www-data; Tablespace: 
--

ALTER TABLE ONLY person
    ADD CONSTRAINT person_email_key UNIQUE (email);


--
-- Name: person_pkey; Type: CONSTRAINT; Schema: public; Owner: www-data; Tablespace: 
--

ALTER TABLE ONLY person
    ADD CONSTRAINT person_pkey PRIMARY KEY (person);


--
-- Name: priority_domain_domain_key; Type: CONSTRAINT; Schema: public; Owner: www-data; Tablespace: 
--

ALTER TABLE ONLY priority_domain
    ADD CONSTRAINT priority_domain_domain_key UNIQUE ("domain");


--
-- Name: request_group_pkey; Type: CONSTRAINT; Schema: public; Owner: www-data; Tablespace: 
--

ALTER TABLE ONLY request_group
    ADD CONSTRAINT request_group_pkey PRIMARY KEY (request_group);


--
-- Name: request_pkey; Type: CONSTRAINT; Schema: public; Owner: www-data; Tablespace: 
--

ALTER TABLE ONLY request
    ADD CONSTRAINT request_pkey PRIMARY KEY (request);


--
-- Name: screenshot_hashkey_key; Type: CONSTRAINT; Schema: public; Owner: www-data; Tablespace: 
--

ALTER TABLE ONLY screenshot
    ADD CONSTRAINT screenshot_hashkey_key UNIQUE (hashkey);


--
-- Name: screenshot_pkey; Type: CONSTRAINT; Schema: public; Owner: www-data; Tablespace: 
--

ALTER TABLE ONLY screenshot
    ADD CONSTRAINT screenshot_pkey PRIMARY KEY (screenshot);


--
-- Name: website_pkey; Type: CONSTRAINT; Schema: public; Owner: www-data; Tablespace: 
--

ALTER TABLE ONLY website
    ADD CONSTRAINT website_pkey PRIMARY KEY (website);


--
-- Name: website_url_key; Type: CONSTRAINT; Schema: public; Owner: www-data; Tablespace: 
--

ALTER TABLE ONLY website
    ADD CONSTRAINT website_url_key UNIQUE (url);


--
-- Name: factory_bpp_unique; Type: INDEX; Schema: public; Owner: www-data; Tablespace: 
--

CREATE UNIQUE INDEX factory_bpp_unique ON factory_bpp USING btree (factory, bpp);


--
-- Name: factory_browser_major_minor_unique; Type: INDEX; Schema: public; Owner: www-data; Tablespace: 
--

CREATE UNIQUE INDEX factory_browser_major_minor_unique ON factory_browser USING btree (factory, browser_group, major, minor);


--
-- Name: factory_feature_unique; Type: INDEX; Schema: public; Owner: www-data; Tablespace: 
--

CREATE UNIQUE INDEX factory_feature_unique ON factory_feature USING btree (factory, name, intval, strval);


--
-- Name: factory_screen_unique; Type: INDEX; Schema: public; Owner: www-data; Tablespace: 
--

CREATE UNIQUE INDEX factory_screen_unique ON factory_screen USING btree (factory, width, height);


--
-- Name: nonce_request; Type: INDEX; Schema: public; Owner: www-data; Tablespace: 
--

CREATE INDEX nonce_request ON nonce USING btree (request) WHERE (request IS NOT NULL);


--
-- Name: request_group_bpp; Type: INDEX; Schema: public; Owner: www-data; Tablespace: 
--

CREATE INDEX request_group_bpp ON request_group USING btree (bpp);


--
-- Name: request_group_created; Type: INDEX; Schema: public; Owner: www-data; Tablespace: 
--

CREATE INDEX request_group_created ON request_group USING btree (created);


--
-- Name: request_group_flash; Type: INDEX; Schema: public; Owner: www-data; Tablespace: 
--

CREATE INDEX request_group_flash ON request_group USING btree (flash);


--
-- Name: request_group_java; Type: INDEX; Schema: public; Owner: www-data; Tablespace: 
--

CREATE INDEX request_group_java ON request_group USING btree (java);


--
-- Name: request_group_js; Type: INDEX; Schema: public; Owner: www-data; Tablespace: 
--

CREATE INDEX request_group_js ON request_group USING btree (js);


--
-- Name: request_group_media; Type: INDEX; Schema: public; Owner: www-data; Tablespace: 
--

CREATE INDEX request_group_media ON request_group USING btree (media);


--
-- Name: request_group_width; Type: INDEX; Schema: public; Owner: www-data; Tablespace: 
--

CREATE INDEX request_group_width ON request_group USING btree (width);


--
-- Name: request_locked; Type: INDEX; Schema: public; Owner: www-data; Tablespace: 
--

CREATE INDEX request_locked ON request USING btree (locked);


--
-- Name: request_priority; Type: INDEX; Schema: public; Owner: www-data; Tablespace: 
--

CREATE INDEX request_priority ON request USING btree (priority);


--
-- Name: request_request_group; Type: INDEX; Schema: public; Owner: www-data; Tablespace: 
--

CREATE INDEX request_request_group ON request USING btree (request_group);


--
-- Name: request_screenshot; Type: INDEX; Schema: public; Owner: www-data; Tablespace: 
--

CREATE INDEX request_screenshot ON request USING btree (screenshot);


--
-- Name: request_screenshot_null; Type: INDEX; Schema: public; Owner: www-data; Tablespace: 
--

CREATE INDEX request_screenshot_null ON request USING btree (screenshot) WHERE (screenshot IS NULL);


--
-- Name: screenshot_created; Type: INDEX; Schema: public; Owner: www-data; Tablespace: 
--

CREATE INDEX screenshot_created ON screenshot USING btree (created);


--
-- Name: screenshot_factory; Type: INDEX; Schema: public; Owner: www-data; Tablespace: 
--

CREATE INDEX screenshot_factory ON screenshot USING btree (factory);


--
-- Name: architecture_creator_fkey; Type: FK CONSTRAINT; Schema: public; Owner: www-data
--

ALTER TABLE ONLY architecture
    ADD CONSTRAINT architecture_creator_fkey FOREIGN KEY (creator) REFERENCES person(person);


--
-- Name: browser_engine_fkey; Type: FK CONSTRAINT; Schema: public; Owner: www-data
--

ALTER TABLE ONLY factory_browser
    ADD CONSTRAINT browser_engine_fkey FOREIGN KEY (engine) REFERENCES engine(engine);


--
-- Name: browser_group_creator_fkey; Type: FK CONSTRAINT; Schema: public; Owner: www-data
--

ALTER TABLE ONLY browser_group
    ADD CONSTRAINT browser_group_creator_fkey FOREIGN KEY (creator) REFERENCES person(person);


--
-- Name: engine_creator_fkey; Type: FK CONSTRAINT; Schema: public; Owner: www-data
--

ALTER TABLE ONLY engine
    ADD CONSTRAINT engine_creator_fkey FOREIGN KEY (creator) REFERENCES person(person);


--
-- Name: factory_architecture_fkey; Type: FK CONSTRAINT; Schema: public; Owner: www-data
--

ALTER TABLE ONLY factory
    ADD CONSTRAINT factory_architecture_fkey FOREIGN KEY (architecture) REFERENCES architecture(architecture);


--
-- Name: factory_bpp_factory_fkey; Type: FK CONSTRAINT; Schema: public; Owner: www-data
--

ALTER TABLE ONLY factory_bpp
    ADD CONSTRAINT factory_bpp_factory_fkey FOREIGN KEY (factory) REFERENCES factory(factory);


--
-- Name: factory_browser_browser_group_fkey; Type: FK CONSTRAINT; Schema: public; Owner: www-data
--

ALTER TABLE ONLY factory_browser
    ADD CONSTRAINT factory_browser_browser_group_fkey FOREIGN KEY (browser_group) REFERENCES browser_group(browser_group);


--
-- Name: factory_browser_creator_fkey; Type: FK CONSTRAINT; Schema: public; Owner: www-data
--

ALTER TABLE ONLY factory_browser
    ADD CONSTRAINT factory_browser_creator_fkey FOREIGN KEY (creator) REFERENCES person(person);


--
-- Name: factory_browser_factory_fkey; Type: FK CONSTRAINT; Schema: public; Owner: www-data
--

ALTER TABLE ONLY factory_browser
    ADD CONSTRAINT factory_browser_factory_fkey FOREIGN KEY (factory) REFERENCES factory(factory);


--
-- Name: factory_creator_fkey; Type: FK CONSTRAINT; Schema: public; Owner: www-data
--

ALTER TABLE ONLY factory
    ADD CONSTRAINT factory_creator_fkey FOREIGN KEY (creator) REFERENCES person(person);


--
-- Name: factory_feature_factory_fkey; Type: FK CONSTRAINT; Schema: public; Owner: www-data
--

ALTER TABLE ONLY factory_feature
    ADD CONSTRAINT factory_feature_factory_fkey FOREIGN KEY (factory) REFERENCES factory(factory);


--
-- Name: factory_opsys_fkey; Type: FK CONSTRAINT; Schema: public; Owner: www-data
--

ALTER TABLE ONLY factory
    ADD CONSTRAINT factory_opsys_fkey FOREIGN KEY (opsys) REFERENCES opsys(opsys);


--
-- Name: factory_owner_fkey; Type: FK CONSTRAINT; Schema: public; Owner: www-data
--

ALTER TABLE ONLY factory
    ADD CONSTRAINT factory_owner_fkey FOREIGN KEY ("owner") REFERENCES person(person);


--
-- Name: factory_screen_factory_fkey; Type: FK CONSTRAINT; Schema: public; Owner: www-data
--

ALTER TABLE ONLY factory_screen
    ADD CONSTRAINT factory_screen_factory_fkey FOREIGN KEY (factory) REFERENCES factory(factory);


--
-- Name: failure_factory_fkey; Type: FK CONSTRAINT; Schema: public; Owner: www-data
--

ALTER TABLE ONLY failure
    ADD CONSTRAINT failure_factory_fkey FOREIGN KEY (factory) REFERENCES factory(factory);


--
-- Name: failure_request_fkey; Type: FK CONSTRAINT; Schema: public; Owner: www-data
--

ALTER TABLE ONLY failure
    ADD CONSTRAINT failure_request_fkey FOREIGN KEY (request) REFERENCES request(request) ON DELETE CASCADE;


--
-- Name: nonce_factory_fkey; Type: FK CONSTRAINT; Schema: public; Owner: www-data
--

ALTER TABLE ONLY nonce
    ADD CONSTRAINT nonce_factory_fkey FOREIGN KEY (factory) REFERENCES factory(factory);


--
-- Name: nonce_person_fkey; Type: FK CONSTRAINT; Schema: public; Owner: www-data
--

ALTER TABLE ONLY nonce
    ADD CONSTRAINT nonce_person_fkey FOREIGN KEY (person) REFERENCES person(person);


--
-- Name: nonce_request_fkey; Type: FK CONSTRAINT; Schema: public; Owner: www-data
--

ALTER TABLE ONLY nonce
    ADD CONSTRAINT nonce_request_fkey FOREIGN KEY (request) REFERENCES request(request);


--
-- Name: opsys_creator_fkey; Type: FK CONSTRAINT; Schema: public; Owner: www-data
--

ALTER TABLE ONLY opsys
    ADD CONSTRAINT opsys_creator_fkey FOREIGN KEY (creator) REFERENCES person(person);


--
-- Name: opsys_group_creator_fkey; Type: FK CONSTRAINT; Schema: public; Owner: www-data
--

ALTER TABLE ONLY opsys_group
    ADD CONSTRAINT opsys_group_creator_fkey FOREIGN KEY (creator) REFERENCES person(person);


--
-- Name: opsys_opsys_group_fkey; Type: FK CONSTRAINT; Schema: public; Owner: www-data
--

ALTER TABLE ONLY opsys
    ADD CONSTRAINT opsys_opsys_group_fkey FOREIGN KEY (opsys_group) REFERENCES opsys_group(opsys_group);


--
-- Name: request_browser_group_fkey; Type: FK CONSTRAINT; Schema: public; Owner: www-data
--

ALTER TABLE ONLY request
    ADD CONSTRAINT request_browser_group_fkey FOREIGN KEY (browser_group) REFERENCES browser_group(browser_group);


--
-- Name: request_factory_browser_fkey; Type: FK CONSTRAINT; Schema: public; Owner: www-data
--

ALTER TABLE ONLY request
    ADD CONSTRAINT request_factory_browser_fkey FOREIGN KEY (factory_browser) REFERENCES factory_browser(factory_browser);


--
-- Name: request_factory_fkey; Type: FK CONSTRAINT; Schema: public; Owner: www-data
--

ALTER TABLE ONLY request
    ADD CONSTRAINT request_factory_fkey FOREIGN KEY (factory) REFERENCES factory(factory);


--
-- Name: request_group_creator_fkey; Type: FK CONSTRAINT; Schema: public; Owner: www-data
--

ALTER TABLE ONLY request_group
    ADD CONSTRAINT request_group_creator_fkey FOREIGN KEY (creator) REFERENCES person(person);


--
-- Name: request_group_website_fkey; Type: FK CONSTRAINT; Schema: public; Owner: www-data
--

ALTER TABLE ONLY request_group
    ADD CONSTRAINT request_group_website_fkey FOREIGN KEY (website) REFERENCES website(website);


--
-- Name: request_opsys_fkey; Type: FK CONSTRAINT; Schema: public; Owner: www-data
--

ALTER TABLE ONLY request
    ADD CONSTRAINT request_opsys_fkey FOREIGN KEY (opsys) REFERENCES opsys(opsys);


--
-- Name: request_opsys_group_fkey; Type: FK CONSTRAINT; Schema: public; Owner: www-data
--

ALTER TABLE ONLY request
    ADD CONSTRAINT request_opsys_group_fkey FOREIGN KEY (opsys_group) REFERENCES opsys_group(opsys_group);


--
-- Name: request_request_group_fkey; Type: FK CONSTRAINT; Schema: public; Owner: www-data
--

ALTER TABLE ONLY request
    ADD CONSTRAINT request_request_group_fkey FOREIGN KEY (request_group) REFERENCES request_group(request_group);


--
-- Name: request_screenshot_fkey; Type: FK CONSTRAINT; Schema: public; Owner: www-data
--

ALTER TABLE ONLY request
    ADD CONSTRAINT request_screenshot_fkey FOREIGN KEY (screenshot) REFERENCES screenshot(screenshot) ON DELETE CASCADE;


--
-- Name: screenshot_factory_browser_fkey; Type: FK CONSTRAINT; Schema: public; Owner: www-data
--

ALTER TABLE ONLY screenshot
    ADD CONSTRAINT screenshot_factory_browser_fkey FOREIGN KEY (factory_browser) REFERENCES factory_browser(factory_browser);


--
-- Name: screenshot_factory_fkey; Type: FK CONSTRAINT; Schema: public; Owner: www-data
--

ALTER TABLE ONLY screenshot
    ADD CONSTRAINT screenshot_factory_fkey FOREIGN KEY (factory) REFERENCES factory(factory);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

