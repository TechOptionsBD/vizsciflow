--
-- PostgreSQL database dump
--

-- Dumped from database version 13.8
-- Dumped by pg_dump version 13.8

-- Started on 2023-02-21 07:15:07 UTC

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 273 (class 1259 OID 17178)
-- Name: activities; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.activities (
    id integer NOT NULL,
    user_id integer,
    type character varying(30),
    status character varying(30),
    created_on timestamp without time zone,
    modified_on timestamp without time zone
);


ALTER TABLE public.activities OWNER TO phenodoop;

--
-- TOC entry 272 (class 1259 OID 17176)
-- Name: activities_id_seq; Type: SEQUENCE; Schema: public; Owner: phenodoop
--

CREATE SEQUENCE public.activities_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.activities_id_seq OWNER TO phenodoop;

--
-- TOC entry 3415 (class 0 OID 0)
-- Dependencies: 272
-- Name: activities_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.activities_id_seq OWNED BY public.activities.id;


--
-- TOC entry 275 (class 1259 OID 17191)
-- Name: activitylogs; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.activitylogs (
    id integer NOT NULL,
    activity_id integer,
    "time" timestamp without time zone,
    type text,
    log text
);


ALTER TABLE public.activitylogs OWNER TO phenodoop;

--
-- TOC entry 274 (class 1259 OID 17189)
-- Name: activitylogs_id_seq; Type: SEQUENCE; Schema: public; Owner: phenodoop
--

CREATE SEQUENCE public.activitylogs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.activitylogs_id_seq OWNER TO phenodoop;

--
-- TOC entry 3416 (class 0 OID 0)
-- Dependencies: 274
-- Name: activitylogs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.activitylogs_id_seq OWNED BY public.activitylogs.id;


--
-- TOC entry 271 (class 1259 OID 16970)
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO phenodoop;

--
-- TOC entry 242 (class 1259 OID 16695)
-- Name: comments; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.comments (
    id integer NOT NULL,
    body text,
    body_html text,
    "timestamp" timestamp without time zone,
    disabled boolean,
    author_id integer,
    post_id integer
);


ALTER TABLE public.comments OWNER TO phenodoop;

--
-- TOC entry 241 (class 1259 OID 16693)
-- Name: comments_id_seq; Type: SEQUENCE; Schema: public; Owner: phenodoop
--

CREATE SEQUENCE public.comments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.comments_id_seq OWNER TO phenodoop;

--
-- TOC entry 3417 (class 0 OID 0)
-- Dependencies: 241
-- Name: comments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.comments_id_seq OWNED BY public.comments.id;


--
-- TOC entry 213 (class 1259 OID 16450)
-- Name: data; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.data (
    id integer NOT NULL,
    value json
);


ALTER TABLE public.data OWNER TO phenodoop;

--
-- TOC entry 240 (class 1259 OID 16677)
-- Name: data_allocations; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.data_allocations (
    id integer NOT NULL,
    data_id integer NOT NULL,
    user_id integer NOT NULL,
    rights integer
);


ALTER TABLE public.data_allocations OWNER TO phenodoop;

--
-- TOC entry 239 (class 1259 OID 16675)
-- Name: data_allocations_id_seq; Type: SEQUENCE; Schema: public; Owner: phenodoop
--

CREATE SEQUENCE public.data_allocations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_allocations_id_seq OWNER TO phenodoop;

--
-- TOC entry 3418 (class 0 OID 0)
-- Dependencies: 239
-- Name: data_allocations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.data_allocations_id_seq OWNED BY public.data_allocations.id;


--
-- TOC entry 234 (class 1259 OID 16625)
-- Name: data_annotations; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.data_annotations (
    id integer NOT NULL,
    data_id integer,
    tag text NOT NULL
);


ALTER TABLE public.data_annotations OWNER TO phenodoop;

--
-- TOC entry 233 (class 1259 OID 16623)
-- Name: data_annotations_id_seq; Type: SEQUENCE; Schema: public; Owner: phenodoop
--

CREATE SEQUENCE public.data_annotations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_annotations_id_seq OWNER TO phenodoop;

--
-- TOC entry 3419 (class 0 OID 0)
-- Dependencies: 233
-- Name: data_annotations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.data_annotations_id_seq OWNED BY public.data_annotations.id;


--
-- TOC entry 212 (class 1259 OID 16448)
-- Name: data_id_seq; Type: SEQUENCE; Schema: public; Owner: phenodoop
--

CREATE SEQUENCE public.data_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_id_seq OWNER TO phenodoop;

--
-- TOC entry 3420 (class 0 OID 0)
-- Dependencies: 212
-- Name: data_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.data_id_seq OWNED BY public.data.id;


--
-- TOC entry 238 (class 1259 OID 16659)
-- Name: data_mimetypes; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.data_mimetypes (
    id integer NOT NULL,
    data_id integer NOT NULL,
    mimetype_id integer NOT NULL
);


ALTER TABLE public.data_mimetypes OWNER TO phenodoop;

--
-- TOC entry 237 (class 1259 OID 16657)
-- Name: data_mimetypes_id_seq; Type: SEQUENCE; Schema: public; Owner: phenodoop
--

CREATE SEQUENCE public.data_mimetypes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_mimetypes_id_seq OWNER TO phenodoop;

--
-- TOC entry 3421 (class 0 OID 0)
-- Dependencies: 237
-- Name: data_mimetypes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.data_mimetypes_id_seq OWNED BY public.data_mimetypes.id;


--
-- TOC entry 232 (class 1259 OID 16607)
-- Name: data_permissions; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.data_permissions (
    id integer NOT NULL,
    user_id integer,
    data_id integer,
    rights integer
);


ALTER TABLE public.data_permissions OWNER TO phenodoop;

--
-- TOC entry 231 (class 1259 OID 16605)
-- Name: data_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: phenodoop
--

CREATE SEQUENCE public.data_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_permissions_id_seq OWNER TO phenodoop;

--
-- TOC entry 3422 (class 0 OID 0)
-- Dependencies: 231
-- Name: data_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.data_permissions_id_seq OWNED BY public.data_permissions.id;


--
-- TOC entry 219 (class 1259 OID 16495)
-- Name: data_properties; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.data_properties (
    id integer NOT NULL,
    data_id integer,
    key text NOT NULL,
    value json NOT NULL
);


ALTER TABLE public.data_properties OWNER TO phenodoop;

--
-- TOC entry 218 (class 1259 OID 16493)
-- Name: data_properties_id_seq; Type: SEQUENCE; Schema: public; Owner: phenodoop
--

CREATE SEQUENCE public.data_properties_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_properties_id_seq OWNER TO phenodoop;

--
-- TOC entry 3423 (class 0 OID 0)
-- Dependencies: 218
-- Name: data_properties_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.data_properties_id_seq OWNED BY public.data_properties.id;


--
-- TOC entry 236 (class 1259 OID 16641)
-- Name: data_visualizers; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.data_visualizers (
    id integer NOT NULL,
    data_id integer NOT NULL,
    visualizer_id integer NOT NULL
);


ALTER TABLE public.data_visualizers OWNER TO phenodoop;

--
-- TOC entry 235 (class 1259 OID 16639)
-- Name: data_visualizers_id_seq; Type: SEQUENCE; Schema: public; Owner: phenodoop
--

CREATE SEQUENCE public.data_visualizers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_visualizers_id_seq OWNER TO phenodoop;

--
-- TOC entry 3424 (class 0 OID 0)
-- Dependencies: 235
-- Name: data_visualizers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.data_visualizers_id_seq OWNED BY public.data_visualizers.id;


--
-- TOC entry 205 (class 1259 OID 16409)
-- Name: datasets; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.datasets (
    id integer NOT NULL,
    schema json NOT NULL
);


ALTER TABLE public.datasets OWNER TO phenodoop;

--
-- TOC entry 204 (class 1259 OID 16407)
-- Name: datasets_id_seq; Type: SEQUENCE; Schema: public; Owner: phenodoop
--

CREATE SEQUENCE public.datasets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.datasets_id_seq OWNER TO phenodoop;

--
-- TOC entry 3425 (class 0 OID 0)
-- Dependencies: 204
-- Name: datasets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.datasets_id_seq OWNED BY public.datasets.id;


--
-- TOC entry 217 (class 1259 OID 16479)
-- Name: datasource_allocations; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.datasource_allocations (
    id integer NOT NULL,
    datasource_id integer,
    url text NOT NULL
);


ALTER TABLE public.datasource_allocations OWNER TO phenodoop;

--
-- TOC entry 216 (class 1259 OID 16477)
-- Name: datasource_allocations_id_seq; Type: SEQUENCE; Schema: public; Owner: phenodoop
--

CREATE SEQUENCE public.datasource_allocations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.datasource_allocations_id_seq OWNER TO phenodoop;

--
-- TOC entry 3426 (class 0 OID 0)
-- Dependencies: 216
-- Name: datasource_allocations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.datasource_allocations_id_seq OWNED BY public.datasource_allocations.id;


--
-- TOC entry 203 (class 1259 OID 16398)
-- Name: datasources; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.datasources (
    id integer NOT NULL,
    name character varying(30),
    type character varying(30) NOT NULL,
    url text,
    root text,
    public text,
    "user" character varying(30),
    password character varying(50),
    prefix text,
    active boolean,
    temp text
);


ALTER TABLE public.datasources OWNER TO phenodoop;

--
-- TOC entry 202 (class 1259 OID 16396)
-- Name: datasources_id_seq; Type: SEQUENCE; Schema: public; Owner: phenodoop
--

CREATE SEQUENCE public.datasources_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.datasources_id_seq OWNER TO phenodoop;

--
-- TOC entry 3427 (class 0 OID 0)
-- Dependencies: 202
-- Name: datasources_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.datasources_id_seq OWNED BY public.datasources.id;


--
-- TOC entry 230 (class 1259 OID 16591)
-- Name: filter_history; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.filter_history (
    id integer NOT NULL,
    user_id integer NOT NULL,
    value json NOT NULL,
    created_on timestamp without time zone
);


ALTER TABLE public.filter_history OWNER TO phenodoop;

--
-- TOC entry 229 (class 1259 OID 16589)
-- Name: filter_history_id_seq; Type: SEQUENCE; Schema: public; Owner: phenodoop
--

CREATE SEQUENCE public.filter_history_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.filter_history_id_seq OWNER TO phenodoop;

--
-- TOC entry 3428 (class 0 OID 0)
-- Dependencies: 229
-- Name: filter_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.filter_history_id_seq OWNED BY public.filter_history.id;


--
-- TOC entry 228 (class 1259 OID 16575)
-- Name: filters; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.filters (
    id integer NOT NULL,
    user_id integer NOT NULL,
    name text NOT NULL,
    value json NOT NULL,
    created_on timestamp without time zone
);


ALTER TABLE public.filters OWNER TO phenodoop;

--
-- TOC entry 227 (class 1259 OID 16573)
-- Name: filters_id_seq; Type: SEQUENCE; Schema: public; Owner: phenodoop
--

CREATE SEQUENCE public.filters_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.filters_id_seq OWNER TO phenodoop;

--
-- TOC entry 3429 (class 0 OID 0)
-- Dependencies: 227
-- Name: filters_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.filters_id_seq OWNED BY public.filters.id;


--
-- TOC entry 220 (class 1259 OID 16509)
-- Name: follows; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.follows (
    follower_id integer NOT NULL,
    followed_id integer NOT NULL,
    "timestamp" timestamp without time zone
);


ALTER TABLE public.follows OWNER TO phenodoop;

--
-- TOC entry 270 (class 1259 OID 16941)
-- Name: indata; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.indata (
    id integer NOT NULL,
    task_id integer,
    data_id integer
);


ALTER TABLE public.indata OWNER TO phenodoop;

--
-- TOC entry 269 (class 1259 OID 16939)
-- Name: indata_id_seq; Type: SEQUENCE; Schema: public; Owner: phenodoop
--

CREATE SEQUENCE public.indata_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.indata_id_seq OWNER TO phenodoop;

--
-- TOC entry 3430 (class 0 OID 0)
-- Dependencies: 269
-- Name: indata_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.indata_id_seq OWNED BY public.indata.id;


--
-- TOC entry 211 (class 1259 OID 16439)
-- Name: mimetypes; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.mimetypes (
    id integer NOT NULL,
    name text NOT NULL,
    "desc" text,
    extension text
);


ALTER TABLE public.mimetypes OWNER TO phenodoop;

--
-- TOC entry 210 (class 1259 OID 16437)
-- Name: mimetypes_id_seq; Type: SEQUENCE; Schema: public; Owner: phenodoop
--

CREATE SEQUENCE public.mimetypes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mimetypes_id_seq OWNER TO phenodoop;

--
-- TOC entry 3431 (class 0 OID 0)
-- Dependencies: 210
-- Name: mimetypes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.mimetypes_id_seq OWNED BY public.mimetypes.id;


--
-- TOC entry 250 (class 1259 OID 16767)
-- Name: params; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.params (
    id integer NOT NULL,
    service_id integer,
    value json NOT NULL
);


ALTER TABLE public.params OWNER TO phenodoop;

--
-- TOC entry 249 (class 1259 OID 16765)
-- Name: params_id_seq; Type: SEQUENCE; Schema: public; Owner: phenodoop
--

CREATE SEQUENCE public.params_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.params_id_seq OWNER TO phenodoop;

--
-- TOC entry 3432 (class 0 OID 0)
-- Dependencies: 249
-- Name: params_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.params_id_seq OWNED BY public.params.id;


--
-- TOC entry 222 (class 1259 OID 16526)
-- Name: posts; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.posts (
    id integer NOT NULL,
    body text,
    body_html text,
    "timestamp" timestamp without time zone,
    author_id integer
);


ALTER TABLE public.posts OWNER TO phenodoop;

--
-- TOC entry 221 (class 1259 OID 16524)
-- Name: posts_id_seq; Type: SEQUENCE; Schema: public; Owner: phenodoop
--

CREATE SEQUENCE public.posts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.posts_id_seq OWNER TO phenodoop;

--
-- TOC entry 3433 (class 0 OID 0)
-- Dependencies: 221
-- Name: posts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.posts_id_seq OWNED BY public.posts.id;


--
-- TOC entry 252 (class 1259 OID 16783)
-- Name: returns; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.returns (
    id integer NOT NULL,
    service_id integer,
    value json NOT NULL
);


ALTER TABLE public.returns OWNER TO phenodoop;

--
-- TOC entry 251 (class 1259 OID 16781)
-- Name: returns_id_seq; Type: SEQUENCE; Schema: public; Owner: phenodoop
--

CREATE SEQUENCE public.returns_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.returns_id_seq OWNER TO phenodoop;

--
-- TOC entry 3434 (class 0 OID 0)
-- Dependencies: 251
-- Name: returns_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.returns_id_seq OWNED BY public.returns.id;


--
-- TOC entry 201 (class 1259 OID 16387)
-- Name: roles; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.roles (
    id integer NOT NULL,
    name character varying(64),
    "default" boolean,
    permissions integer
);


ALTER TABLE public.roles OWNER TO phenodoop;

--
-- TOC entry 200 (class 1259 OID 16385)
-- Name: roles_id_seq; Type: SEQUENCE; Schema: public; Owner: phenodoop
--

CREATE SEQUENCE public.roles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.roles_id_seq OWNER TO phenodoop;

--
-- TOC entry 3435 (class 0 OID 0)
-- Dependencies: 200
-- Name: roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.roles_id_seq OWNED BY public.roles.id;


--
-- TOC entry 260 (class 1259 OID 16854)
-- Name: runnableargs; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.runnableargs (
    id integer NOT NULL,
    runnable_id integer,
    value json NOT NULL
);


ALTER TABLE public.runnableargs OWNER TO phenodoop;

--
-- TOC entry 259 (class 1259 OID 16852)
-- Name: runnableargs_id_seq; Type: SEQUENCE; Schema: public; Owner: phenodoop
--

CREATE SEQUENCE public.runnableargs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.runnableargs_id_seq OWNER TO phenodoop;

--
-- TOC entry 3436 (class 0 OID 0)
-- Dependencies: 259
-- Name: runnableargs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.runnableargs_id_seq OWNED BY public.runnableargs.id;


--
-- TOC entry 262 (class 1259 OID 16870)
-- Name: runnablereturns; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.runnablereturns (
    id integer NOT NULL,
    runnable_id integer,
    value json NOT NULL
);


ALTER TABLE public.runnablereturns OWNER TO phenodoop;

--
-- TOC entry 261 (class 1259 OID 16868)
-- Name: runnablereturns_id_seq; Type: SEQUENCE; Schema: public; Owner: phenodoop
--

CREATE SEQUENCE public.runnablereturns_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.runnablereturns_id_seq OWNER TO phenodoop;

--
-- TOC entry 3437 (class 0 OID 0)
-- Dependencies: 261
-- Name: runnablereturns_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.runnablereturns_id_seq OWNED BY public.runnablereturns.id;


--
-- TOC entry 256 (class 1259 OID 16817)
-- Name: runnables; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.runnables (
    id integer NOT NULL,
    workflow_id integer,
    user_id integer,
    celery_id character varying(64),
    status character varying(30),
    script text NOT NULL,
    "out" text,
    error text,
    view text,
    duration double precision,
    started_on timestamp without time zone,
    created_on timestamp without time zone,
    modified_on timestamp without time zone
);


ALTER TABLE public.runnables OWNER TO phenodoop;

--
-- TOC entry 255 (class 1259 OID 16815)
-- Name: runnables_id_seq; Type: SEQUENCE; Schema: public; Owner: phenodoop
--

CREATE SEQUENCE public.runnables_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.runnables_id_seq OWNER TO phenodoop;

--
-- TOC entry 3438 (class 0 OID 0)
-- Dependencies: 255
-- Name: runnables_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.runnables_id_seq OWNED BY public.runnables.id;


--
-- TOC entry 254 (class 1259 OID 16799)
-- Name: serviceaccesses; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.serviceaccesses (
    id integer NOT NULL,
    service_id integer NOT NULL,
    user_id integer NOT NULL,
    rights integer
);


ALTER TABLE public.serviceaccesses OWNER TO phenodoop;

--
-- TOC entry 253 (class 1259 OID 16797)
-- Name: serviceaccesses_id_seq; Type: SEQUENCE; Schema: public; Owner: phenodoop
--

CREATE SEQUENCE public.serviceaccesses_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.serviceaccesses_id_seq OWNER TO phenodoop;

--
-- TOC entry 3439 (class 0 OID 0)
-- Dependencies: 253
-- Name: serviceaccesses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.serviceaccesses_id_seq OWNED BY public.serviceaccesses.id;


--
-- TOC entry 226 (class 1259 OID 16559)
-- Name: services; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.services (
    id integer NOT NULL,
    user_id integer NOT NULL,
    value json NOT NULL,
    public boolean,
    active boolean,
    pipenv text,
    pippkgs text,
    reqfile text
);


ALTER TABLE public.services OWNER TO phenodoop;

--
-- TOC entry 225 (class 1259 OID 16557)
-- Name: services_id_seq; Type: SEQUENCE; Schema: public; Owner: phenodoop
--

CREATE SEQUENCE public.services_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.services_id_seq OWNER TO phenodoop;

--
-- TOC entry 3440 (class 0 OID 0)
-- Dependencies: 225
-- Name: services_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.services_id_seq OWNED BY public.services.id;


--
-- TOC entry 268 (class 1259 OID 16923)
-- Name: taskdata; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.taskdata (
    id integer NOT NULL,
    task_id integer,
    data_id integer
);


ALTER TABLE public.taskdata OWNER TO phenodoop;

--
-- TOC entry 267 (class 1259 OID 16921)
-- Name: taskdata_id_seq; Type: SEQUENCE; Schema: public; Owner: phenodoop
--

CREATE SEQUENCE public.taskdata_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.taskdata_id_seq OWNER TO phenodoop;

--
-- TOC entry 3441 (class 0 OID 0)
-- Dependencies: 267
-- Name: taskdata_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.taskdata_id_seq OWNED BY public.taskdata.id;


--
-- TOC entry 266 (class 1259 OID 16907)
-- Name: tasklogs; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.tasklogs (
    id integer NOT NULL,
    task_id integer,
    "time" timestamp without time zone,
    type text,
    log text
);


ALTER TABLE public.tasklogs OWNER TO phenodoop;

--
-- TOC entry 265 (class 1259 OID 16905)
-- Name: tasklogs_id_seq; Type: SEQUENCE; Schema: public; Owner: phenodoop
--

CREATE SEQUENCE public.tasklogs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tasklogs_id_seq OWNER TO phenodoop;

--
-- TOC entry 3442 (class 0 OID 0)
-- Dependencies: 265
-- Name: tasklogs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.tasklogs_id_seq OWNED BY public.tasklogs.id;


--
-- TOC entry 264 (class 1259 OID 16886)
-- Name: tasks; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.tasks (
    id integer NOT NULL,
    runnable_id integer,
    service_id integer,
    started_on timestamp without time zone,
    ended_on timestamp without time zone,
    status text,
    comment text,
    duration double precision
);


ALTER TABLE public.tasks OWNER TO phenodoop;

--
-- TOC entry 263 (class 1259 OID 16884)
-- Name: tasks_id_seq; Type: SEQUENCE; Schema: public; Owner: phenodoop
--

CREATE SEQUENCE public.tasks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tasks_id_seq OWNER TO phenodoop;

--
-- TOC entry 3443 (class 0 OID 0)
-- Dependencies: 263
-- Name: tasks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.tasks_id_seq OWNED BY public.tasks.id;


--
-- TOC entry 207 (class 1259 OID 16420)
-- Name: taskstatus; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.taskstatus (
    id integer NOT NULL,
    name character varying(30)
);


ALTER TABLE public.taskstatus OWNER TO phenodoop;

--
-- TOC entry 206 (class 1259 OID 16418)
-- Name: taskstatus_id_seq; Type: SEQUENCE; Schema: public; Owner: phenodoop
--

CREATE SEQUENCE public.taskstatus_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.taskstatus_id_seq OWNER TO phenodoop;

--
-- TOC entry 3444 (class 0 OID 0)
-- Dependencies: 206
-- Name: taskstatus_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.taskstatus_id_seq OWNED BY public.taskstatus.id;


--
-- TOC entry 215 (class 1259 OID 16461)
-- Name: users; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.users (
    id integer NOT NULL,
    email text,
    username text,
    role_id integer,
    password_hash text,
    confirmed boolean,
    name text,
    location text,
    about_me text,
    member_since timestamp without time zone,
    last_seen timestamp without time zone,
    avatar_hash text,
    oid integer
);


ALTER TABLE public.users OWNER TO phenodoop;

--
-- TOC entry 214 (class 1259 OID 16459)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: phenodoop
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO phenodoop;

--
-- TOC entry 3445 (class 0 OID 0)
-- Dependencies: 214
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 209 (class 1259 OID 16428)
-- Name: visualizers; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.visualizers (
    id integer NOT NULL,
    name text NOT NULL,
    "desc" text
);


ALTER TABLE public.visualizers OWNER TO phenodoop;

--
-- TOC entry 208 (class 1259 OID 16426)
-- Name: visualizers_id_seq; Type: SEQUENCE; Schema: public; Owner: phenodoop
--

CREATE SEQUENCE public.visualizers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.visualizers_id_seq OWNER TO phenodoop;

--
-- TOC entry 3446 (class 0 OID 0)
-- Dependencies: 208
-- Name: visualizers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.visualizers_id_seq OWNED BY public.visualizers.id;


--
-- TOC entry 258 (class 1259 OID 16838)
-- Name: workflow_annotations; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.workflow_annotations (
    id integer NOT NULL,
    workflow_id integer,
    tag text NOT NULL
);


ALTER TABLE public.workflow_annotations OWNER TO phenodoop;

--
-- TOC entry 257 (class 1259 OID 16836)
-- Name: workflow_annotations_id_seq; Type: SEQUENCE; Schema: public; Owner: phenodoop
--

CREATE SEQUENCE public.workflow_annotations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.workflow_annotations_id_seq OWNER TO phenodoop;

--
-- TOC entry 3447 (class 0 OID 0)
-- Dependencies: 257
-- Name: workflow_annotations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.workflow_annotations_id_seq OWNED BY public.workflow_annotations.id;


--
-- TOC entry 244 (class 1259 OID 16717)
-- Name: workflowaccesses; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.workflowaccesses (
    id integer NOT NULL,
    workflow_id integer NOT NULL,
    user_id integer NOT NULL,
    rights integer
);


ALTER TABLE public.workflowaccesses OWNER TO phenodoop;

--
-- TOC entry 243 (class 1259 OID 16715)
-- Name: workflowaccesses_id_seq; Type: SEQUENCE; Schema: public; Owner: phenodoop
--

CREATE SEQUENCE public.workflowaccesses_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.workflowaccesses_id_seq OWNER TO phenodoop;

--
-- TOC entry 3448 (class 0 OID 0)
-- Dependencies: 243
-- Name: workflowaccesses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.workflowaccesses_id_seq OWNED BY public.workflowaccesses.id;


--
-- TOC entry 246 (class 1259 OID 16735)
-- Name: workflowparams; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.workflowparams (
    id integer NOT NULL,
    workflow_id integer,
    value json NOT NULL
);


ALTER TABLE public.workflowparams OWNER TO phenodoop;

--
-- TOC entry 245 (class 1259 OID 16733)
-- Name: workflowparams_id_seq; Type: SEQUENCE; Schema: public; Owner: phenodoop
--

CREATE SEQUENCE public.workflowparams_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.workflowparams_id_seq OWNER TO phenodoop;

--
-- TOC entry 3449 (class 0 OID 0)
-- Dependencies: 245
-- Name: workflowparams_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.workflowparams_id_seq OWNED BY public.workflowparams.id;


--
-- TOC entry 248 (class 1259 OID 16751)
-- Name: workflowreturns; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.workflowreturns (
    id integer NOT NULL,
    workflow_id integer,
    value json NOT NULL
);


ALTER TABLE public.workflowreturns OWNER TO phenodoop;

--
-- TOC entry 247 (class 1259 OID 16749)
-- Name: workflowreturns_id_seq; Type: SEQUENCE; Schema: public; Owner: phenodoop
--

CREATE SEQUENCE public.workflowreturns_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.workflowreturns_id_seq OWNER TO phenodoop;

--
-- TOC entry 3450 (class 0 OID 0)
-- Dependencies: 247
-- Name: workflowreturns_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.workflowreturns_id_seq OWNED BY public.workflowreturns.id;


--
-- TOC entry 224 (class 1259 OID 16543)
-- Name: workflows; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.workflows (
    id integer NOT NULL,
    user_id integer,
    created_on timestamp without time zone,
    modified_on timestamp without time zone,
    name text NOT NULL,
    "desc" text,
    script text NOT NULL,
    public boolean,
    temp boolean,
    derived integer
);


ALTER TABLE public.workflows OWNER TO phenodoop;

--
-- TOC entry 223 (class 1259 OID 16541)
-- Name: workflows_id_seq; Type: SEQUENCE; Schema: public; Owner: phenodoop
--

CREATE SEQUENCE public.workflows_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.workflows_id_seq OWNER TO phenodoop;

--
-- TOC entry 3451 (class 0 OID 0)
-- Dependencies: 223
-- Name: workflows_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.workflows_id_seq OWNED BY public.workflows.id;


--
-- TOC entry 3150 (class 2604 OID 17181)
-- Name: activities id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.activities ALTER COLUMN id SET DEFAULT nextval('public.activities_id_seq'::regclass);


--
-- TOC entry 3151 (class 2604 OID 17194)
-- Name: activitylogs id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.activitylogs ALTER COLUMN id SET DEFAULT nextval('public.activitylogs_id_seq'::regclass);


--
-- TOC entry 3135 (class 2604 OID 16698)
-- Name: comments id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.comments ALTER COLUMN id SET DEFAULT nextval('public.comments_id_seq'::regclass);


--
-- TOC entry 3121 (class 2604 OID 16453)
-- Name: data id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data ALTER COLUMN id SET DEFAULT nextval('public.data_id_seq'::regclass);


--
-- TOC entry 3134 (class 2604 OID 16680)
-- Name: data_allocations id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_allocations ALTER COLUMN id SET DEFAULT nextval('public.data_allocations_id_seq'::regclass);


--
-- TOC entry 3131 (class 2604 OID 16628)
-- Name: data_annotations id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_annotations ALTER COLUMN id SET DEFAULT nextval('public.data_annotations_id_seq'::regclass);


--
-- TOC entry 3133 (class 2604 OID 16662)
-- Name: data_mimetypes id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_mimetypes ALTER COLUMN id SET DEFAULT nextval('public.data_mimetypes_id_seq'::regclass);


--
-- TOC entry 3130 (class 2604 OID 16610)
-- Name: data_permissions id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_permissions ALTER COLUMN id SET DEFAULT nextval('public.data_permissions_id_seq'::regclass);


--
-- TOC entry 3124 (class 2604 OID 16498)
-- Name: data_properties id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_properties ALTER COLUMN id SET DEFAULT nextval('public.data_properties_id_seq'::regclass);


--
-- TOC entry 3132 (class 2604 OID 16644)
-- Name: data_visualizers id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_visualizers ALTER COLUMN id SET DEFAULT nextval('public.data_visualizers_id_seq'::regclass);


--
-- TOC entry 3117 (class 2604 OID 16412)
-- Name: datasets id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.datasets ALTER COLUMN id SET DEFAULT nextval('public.datasets_id_seq'::regclass);


--
-- TOC entry 3123 (class 2604 OID 16482)
-- Name: datasource_allocations id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.datasource_allocations ALTER COLUMN id SET DEFAULT nextval('public.datasource_allocations_id_seq'::regclass);


--
-- TOC entry 3116 (class 2604 OID 16401)
-- Name: datasources id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.datasources ALTER COLUMN id SET DEFAULT nextval('public.datasources_id_seq'::regclass);


--
-- TOC entry 3129 (class 2604 OID 16594)
-- Name: filter_history id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.filter_history ALTER COLUMN id SET DEFAULT nextval('public.filter_history_id_seq'::regclass);


--
-- TOC entry 3128 (class 2604 OID 16578)
-- Name: filters id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.filters ALTER COLUMN id SET DEFAULT nextval('public.filters_id_seq'::regclass);


--
-- TOC entry 3149 (class 2604 OID 16944)
-- Name: indata id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.indata ALTER COLUMN id SET DEFAULT nextval('public.indata_id_seq'::regclass);


--
-- TOC entry 3120 (class 2604 OID 16442)
-- Name: mimetypes id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.mimetypes ALTER COLUMN id SET DEFAULT nextval('public.mimetypes_id_seq'::regclass);


--
-- TOC entry 3139 (class 2604 OID 16770)
-- Name: params id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.params ALTER COLUMN id SET DEFAULT nextval('public.params_id_seq'::regclass);


--
-- TOC entry 3125 (class 2604 OID 16529)
-- Name: posts id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.posts ALTER COLUMN id SET DEFAULT nextval('public.posts_id_seq'::regclass);


--
-- TOC entry 3140 (class 2604 OID 16786)
-- Name: returns id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.returns ALTER COLUMN id SET DEFAULT nextval('public.returns_id_seq'::regclass);


--
-- TOC entry 3115 (class 2604 OID 16390)
-- Name: roles id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.roles ALTER COLUMN id SET DEFAULT nextval('public.roles_id_seq'::regclass);


--
-- TOC entry 3144 (class 2604 OID 16857)
-- Name: runnableargs id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.runnableargs ALTER COLUMN id SET DEFAULT nextval('public.runnableargs_id_seq'::regclass);


--
-- TOC entry 3145 (class 2604 OID 16873)
-- Name: runnablereturns id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.runnablereturns ALTER COLUMN id SET DEFAULT nextval('public.runnablereturns_id_seq'::regclass);


--
-- TOC entry 3142 (class 2604 OID 16820)
-- Name: runnables id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.runnables ALTER COLUMN id SET DEFAULT nextval('public.runnables_id_seq'::regclass);


--
-- TOC entry 3141 (class 2604 OID 16802)
-- Name: serviceaccesses id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.serviceaccesses ALTER COLUMN id SET DEFAULT nextval('public.serviceaccesses_id_seq'::regclass);


--
-- TOC entry 3127 (class 2604 OID 16964)
-- Name: services id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.services ALTER COLUMN id SET DEFAULT nextval('public.services_id_seq'::regclass);


--
-- TOC entry 3148 (class 2604 OID 16926)
-- Name: taskdata id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.taskdata ALTER COLUMN id SET DEFAULT nextval('public.taskdata_id_seq'::regclass);


--
-- TOC entry 3147 (class 2604 OID 16910)
-- Name: tasklogs id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.tasklogs ALTER COLUMN id SET DEFAULT nextval('public.tasklogs_id_seq'::regclass);


--
-- TOC entry 3146 (class 2604 OID 16889)
-- Name: tasks id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.tasks ALTER COLUMN id SET DEFAULT nextval('public.tasks_id_seq'::regclass);


--
-- TOC entry 3118 (class 2604 OID 16423)
-- Name: taskstatus id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.taskstatus ALTER COLUMN id SET DEFAULT nextval('public.taskstatus_id_seq'::regclass);


--
-- TOC entry 3122 (class 2604 OID 16464)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 3119 (class 2604 OID 16431)
-- Name: visualizers id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.visualizers ALTER COLUMN id SET DEFAULT nextval('public.visualizers_id_seq'::regclass);


--
-- TOC entry 3143 (class 2604 OID 16841)
-- Name: workflow_annotations id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.workflow_annotations ALTER COLUMN id SET DEFAULT nextval('public.workflow_annotations_id_seq'::regclass);


--
-- TOC entry 3136 (class 2604 OID 16720)
-- Name: workflowaccesses id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.workflowaccesses ALTER COLUMN id SET DEFAULT nextval('public.workflowaccesses_id_seq'::regclass);


--
-- TOC entry 3137 (class 2604 OID 16738)
-- Name: workflowparams id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.workflowparams ALTER COLUMN id SET DEFAULT nextval('public.workflowparams_id_seq'::regclass);


--
-- TOC entry 3138 (class 2604 OID 16754)
-- Name: workflowreturns id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.workflowreturns ALTER COLUMN id SET DEFAULT nextval('public.workflowreturns_id_seq'::regclass);


--
-- TOC entry 3126 (class 2604 OID 16546)
-- Name: workflows id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.workflows ALTER COLUMN id SET DEFAULT nextval('public.workflows_id_seq'::regclass);


--
-- TOC entry 3234 (class 2606 OID 17183)
-- Name: activities activities_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.activities
    ADD CONSTRAINT activities_pkey PRIMARY KEY (id);


--
-- TOC entry 3236 (class 2606 OID 17199)
-- Name: activitylogs activitylogs_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.activitylogs
    ADD CONSTRAINT activitylogs_pkey PRIMARY KEY (id);


--
-- TOC entry 3232 (class 2606 OID 16974)
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- TOC entry 3201 (class 2606 OID 16703)
-- Name: comments comments_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_pkey PRIMARY KEY (id);


--
-- TOC entry 3199 (class 2606 OID 16682)
-- Name: data_allocations data_allocations_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_allocations
    ADD CONSTRAINT data_allocations_pkey PRIMARY KEY (id);


--
-- TOC entry 3193 (class 2606 OID 16633)
-- Name: data_annotations data_annotations_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_annotations
    ADD CONSTRAINT data_annotations_pkey PRIMARY KEY (id);


--
-- TOC entry 3197 (class 2606 OID 16664)
-- Name: data_mimetypes data_mimetypes_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_mimetypes
    ADD CONSTRAINT data_mimetypes_pkey PRIMARY KEY (id);


--
-- TOC entry 3191 (class 2606 OID 16612)
-- Name: data_permissions data_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_permissions
    ADD CONSTRAINT data_permissions_pkey PRIMARY KEY (id);


--
-- TOC entry 3168 (class 2606 OID 16458)
-- Name: data data_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data
    ADD CONSTRAINT data_pkey PRIMARY KEY (id);


--
-- TOC entry 3176 (class 2606 OID 16503)
-- Name: data_properties data_properties_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_properties
    ADD CONSTRAINT data_properties_pkey PRIMARY KEY (id);


--
-- TOC entry 3195 (class 2606 OID 16646)
-- Name: data_visualizers data_visualizers_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_visualizers
    ADD CONSTRAINT data_visualizers_pkey PRIMARY KEY (id);


--
-- TOC entry 3160 (class 2606 OID 16417)
-- Name: datasets datasets_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.datasets
    ADD CONSTRAINT datasets_pkey PRIMARY KEY (id);


--
-- TOC entry 3174 (class 2606 OID 16487)
-- Name: datasource_allocations datasource_allocations_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.datasource_allocations
    ADD CONSTRAINT datasource_allocations_pkey PRIMARY KEY (id);


--
-- TOC entry 3158 (class 2606 OID 16406)
-- Name: datasources datasources_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.datasources
    ADD CONSTRAINT datasources_pkey PRIMARY KEY (id);


--
-- TOC entry 3189 (class 2606 OID 16599)
-- Name: filter_history filter_history_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.filter_history
    ADD CONSTRAINT filter_history_pkey PRIMARY KEY (id);


--
-- TOC entry 3187 (class 2606 OID 16583)
-- Name: filters filters_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.filters
    ADD CONSTRAINT filters_pkey PRIMARY KEY (id);


--
-- TOC entry 3178 (class 2606 OID 16513)
-- Name: follows follows_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.follows
    ADD CONSTRAINT follows_pkey PRIMARY KEY (follower_id, followed_id);


--
-- TOC entry 3230 (class 2606 OID 16946)
-- Name: indata indata_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.indata
    ADD CONSTRAINT indata_pkey PRIMARY KEY (id);


--
-- TOC entry 3166 (class 2606 OID 16447)
-- Name: mimetypes mimetypes_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.mimetypes
    ADD CONSTRAINT mimetypes_pkey PRIMARY KEY (id);


--
-- TOC entry 3210 (class 2606 OID 16775)
-- Name: params params_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.params
    ADD CONSTRAINT params_pkey PRIMARY KEY (id);


--
-- TOC entry 3181 (class 2606 OID 16534)
-- Name: posts posts_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_pkey PRIMARY KEY (id);


--
-- TOC entry 3212 (class 2606 OID 16791)
-- Name: returns returns_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.returns
    ADD CONSTRAINT returns_pkey PRIMARY KEY (id);


--
-- TOC entry 3154 (class 2606 OID 16394)
-- Name: roles roles_name_key; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_name_key UNIQUE (name);


--
-- TOC entry 3156 (class 2606 OID 16392)
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- TOC entry 3220 (class 2606 OID 16862)
-- Name: runnableargs runnableargs_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.runnableargs
    ADD CONSTRAINT runnableargs_pkey PRIMARY KEY (id);


--
-- TOC entry 3222 (class 2606 OID 16878)
-- Name: runnablereturns runnablereturns_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.runnablereturns
    ADD CONSTRAINT runnablereturns_pkey PRIMARY KEY (id);


--
-- TOC entry 3216 (class 2606 OID 16825)
-- Name: runnables runnables_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.runnables
    ADD CONSTRAINT runnables_pkey PRIMARY KEY (id);


--
-- TOC entry 3214 (class 2606 OID 16804)
-- Name: serviceaccesses serviceaccesses_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.serviceaccesses
    ADD CONSTRAINT serviceaccesses_pkey PRIMARY KEY (id);


--
-- TOC entry 3185 (class 2606 OID 16567)
-- Name: services services_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.services
    ADD CONSTRAINT services_pkey PRIMARY KEY (id);


--
-- TOC entry 3228 (class 2606 OID 16928)
-- Name: taskdata taskdata_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.taskdata
    ADD CONSTRAINT taskdata_pkey PRIMARY KEY (id);


--
-- TOC entry 3226 (class 2606 OID 16915)
-- Name: tasklogs tasklogs_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.tasklogs
    ADD CONSTRAINT tasklogs_pkey PRIMARY KEY (id);


--
-- TOC entry 3224 (class 2606 OID 16894)
-- Name: tasks tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_pkey PRIMARY KEY (id);


--
-- TOC entry 3162 (class 2606 OID 16425)
-- Name: taskstatus taskstatus_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.taskstatus
    ADD CONSTRAINT taskstatus_pkey PRIMARY KEY (id);


--
-- TOC entry 3172 (class 2606 OID 16469)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 3164 (class 2606 OID 16436)
-- Name: visualizers visualizers_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.visualizers
    ADD CONSTRAINT visualizers_pkey PRIMARY KEY (id);


--
-- TOC entry 3218 (class 2606 OID 16846)
-- Name: workflow_annotations workflow_annotations_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.workflow_annotations
    ADD CONSTRAINT workflow_annotations_pkey PRIMARY KEY (id);


--
-- TOC entry 3204 (class 2606 OID 16722)
-- Name: workflowaccesses workflowaccesses_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.workflowaccesses
    ADD CONSTRAINT workflowaccesses_pkey PRIMARY KEY (id);


--
-- TOC entry 3206 (class 2606 OID 16743)
-- Name: workflowparams workflowparams_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.workflowparams
    ADD CONSTRAINT workflowparams_pkey PRIMARY KEY (id);


--
-- TOC entry 3208 (class 2606 OID 16759)
-- Name: workflowreturns workflowreturns_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.workflowreturns
    ADD CONSTRAINT workflowreturns_pkey PRIMARY KEY (id);


--
-- TOC entry 3183 (class 2606 OID 16551)
-- Name: workflows workflows_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.workflows
    ADD CONSTRAINT workflows_pkey PRIMARY KEY (id);


--
-- TOC entry 3202 (class 1259 OID 16714)
-- Name: ix_comments_timestamp; Type: INDEX; Schema: public; Owner: phenodoop
--

CREATE INDEX ix_comments_timestamp ON public.comments USING btree ("timestamp");


--
-- TOC entry 3179 (class 1259 OID 16540)
-- Name: ix_posts_timestamp; Type: INDEX; Schema: public; Owner: phenodoop
--

CREATE INDEX ix_posts_timestamp ON public.posts USING btree ("timestamp");


--
-- TOC entry 3152 (class 1259 OID 16395)
-- Name: ix_roles_default; Type: INDEX; Schema: public; Owner: phenodoop
--

CREATE INDEX ix_roles_default ON public.roles USING btree ("default");


--
-- TOC entry 3169 (class 1259 OID 16475)
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: phenodoop
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- TOC entry 3170 (class 1259 OID 16476)
-- Name: ix_users_username; Type: INDEX; Schema: public; Owner: phenodoop
--

CREATE UNIQUE INDEX ix_users_username ON public.users USING btree (username);


--
-- TOC entry 3278 (class 2606 OID 17184)
-- Name: activities activities_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.activities
    ADD CONSTRAINT activities_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 3279 (class 2606 OID 17200)
-- Name: activitylogs activitylogs_activity_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.activitylogs
    ADD CONSTRAINT activitylogs_activity_id_fkey FOREIGN KEY (activity_id) REFERENCES public.activities(id);


--
-- TOC entry 3256 (class 2606 OID 16704)
-- Name: comments comments_author_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_author_id_fkey FOREIGN KEY (author_id) REFERENCES public.users(id);


--
-- TOC entry 3257 (class 2606 OID 16709)
-- Name: comments comments_post_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_post_id_fkey FOREIGN KEY (post_id) REFERENCES public.posts(id);


--
-- TOC entry 3254 (class 2606 OID 16683)
-- Name: data_allocations data_allocations_data_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_allocations
    ADD CONSTRAINT data_allocations_data_id_fkey FOREIGN KEY (data_id) REFERENCES public.data(id);


--
-- TOC entry 3255 (class 2606 OID 16688)
-- Name: data_allocations data_allocations_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_allocations
    ADD CONSTRAINT data_allocations_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 3249 (class 2606 OID 16634)
-- Name: data_annotations data_annotations_data_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_annotations
    ADD CONSTRAINT data_annotations_data_id_fkey FOREIGN KEY (data_id) REFERENCES public.datasource_allocations(id);


--
-- TOC entry 3252 (class 2606 OID 16665)
-- Name: data_mimetypes data_mimetypes_data_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_mimetypes
    ADD CONSTRAINT data_mimetypes_data_id_fkey FOREIGN KEY (data_id) REFERENCES public.datasource_allocations(id);


--
-- TOC entry 3253 (class 2606 OID 16670)
-- Name: data_mimetypes data_mimetypes_mimetype_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_mimetypes
    ADD CONSTRAINT data_mimetypes_mimetype_id_fkey FOREIGN KEY (mimetype_id) REFERENCES public.mimetypes(id);


--
-- TOC entry 3248 (class 2606 OID 16618)
-- Name: data_permissions data_permissions_data_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_permissions
    ADD CONSTRAINT data_permissions_data_id_fkey FOREIGN KEY (data_id) REFERENCES public.datasource_allocations(id);


--
-- TOC entry 3247 (class 2606 OID 16613)
-- Name: data_permissions data_permissions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_permissions
    ADD CONSTRAINT data_permissions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 3239 (class 2606 OID 16504)
-- Name: data_properties data_properties_data_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_properties
    ADD CONSTRAINT data_properties_data_id_fkey FOREIGN KEY (data_id) REFERENCES public.data(id);


--
-- TOC entry 3250 (class 2606 OID 16647)
-- Name: data_visualizers data_visualizers_data_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_visualizers
    ADD CONSTRAINT data_visualizers_data_id_fkey FOREIGN KEY (data_id) REFERENCES public.datasource_allocations(id);


--
-- TOC entry 3251 (class 2606 OID 16652)
-- Name: data_visualizers data_visualizers_visualizer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_visualizers
    ADD CONSTRAINT data_visualizers_visualizer_id_fkey FOREIGN KEY (visualizer_id) REFERENCES public.visualizers(id);


--
-- TOC entry 3238 (class 2606 OID 16488)
-- Name: datasource_allocations datasource_allocations_datasource_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.datasource_allocations
    ADD CONSTRAINT datasource_allocations_datasource_id_fkey FOREIGN KEY (datasource_id) REFERENCES public.datasources(id);


--
-- TOC entry 3246 (class 2606 OID 16600)
-- Name: filter_history filter_history_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.filter_history
    ADD CONSTRAINT filter_history_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 3245 (class 2606 OID 16584)
-- Name: filters filters_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.filters
    ADD CONSTRAINT filters_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 3241 (class 2606 OID 16519)
-- Name: follows follows_followed_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.follows
    ADD CONSTRAINT follows_followed_id_fkey FOREIGN KEY (followed_id) REFERENCES public.users(id);


--
-- TOC entry 3240 (class 2606 OID 16514)
-- Name: follows follows_follower_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.follows
    ADD CONSTRAINT follows_follower_id_fkey FOREIGN KEY (follower_id) REFERENCES public.users(id);


--
-- TOC entry 3277 (class 2606 OID 16952)
-- Name: indata indata_data_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.indata
    ADD CONSTRAINT indata_data_id_fkey FOREIGN KEY (data_id) REFERENCES public.data(id);


--
-- TOC entry 3276 (class 2606 OID 16947)
-- Name: indata indata_task_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.indata
    ADD CONSTRAINT indata_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.tasks(id);


--
-- TOC entry 3262 (class 2606 OID 16776)
-- Name: params params_service_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.params
    ADD CONSTRAINT params_service_id_fkey FOREIGN KEY (service_id) REFERENCES public.services(id);


--
-- TOC entry 3242 (class 2606 OID 16535)
-- Name: posts posts_author_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_author_id_fkey FOREIGN KEY (author_id) REFERENCES public.users(id);


--
-- TOC entry 3263 (class 2606 OID 16792)
-- Name: returns returns_service_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.returns
    ADD CONSTRAINT returns_service_id_fkey FOREIGN KEY (service_id) REFERENCES public.services(id);


--
-- TOC entry 3269 (class 2606 OID 16863)
-- Name: runnableargs runnableargs_runnable_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.runnableargs
    ADD CONSTRAINT runnableargs_runnable_id_fkey FOREIGN KEY (runnable_id) REFERENCES public.runnables(id);


--
-- TOC entry 3270 (class 2606 OID 16879)
-- Name: runnablereturns runnablereturns_runnable_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.runnablereturns
    ADD CONSTRAINT runnablereturns_runnable_id_fkey FOREIGN KEY (runnable_id) REFERENCES public.runnables(id);


--
-- TOC entry 3267 (class 2606 OID 16831)
-- Name: runnables runnables_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.runnables
    ADD CONSTRAINT runnables_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 3266 (class 2606 OID 16826)
-- Name: runnables runnables_workflow_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.runnables
    ADD CONSTRAINT runnables_workflow_id_fkey FOREIGN KEY (workflow_id) REFERENCES public.workflows(id) ON DELETE CASCADE;


--
-- TOC entry 3264 (class 2606 OID 16805)
-- Name: serviceaccesses serviceaccesses_service_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.serviceaccesses
    ADD CONSTRAINT serviceaccesses_service_id_fkey FOREIGN KEY (service_id) REFERENCES public.services(id) ON DELETE CASCADE;


--
-- TOC entry 3265 (class 2606 OID 16810)
-- Name: serviceaccesses serviceaccesses_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.serviceaccesses
    ADD CONSTRAINT serviceaccesses_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 3244 (class 2606 OID 16568)
-- Name: services services_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.services
    ADD CONSTRAINT services_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 3275 (class 2606 OID 16934)
-- Name: taskdata taskdata_data_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.taskdata
    ADD CONSTRAINT taskdata_data_id_fkey FOREIGN KEY (data_id) REFERENCES public.data(id);


--
-- TOC entry 3274 (class 2606 OID 16929)
-- Name: taskdata taskdata_task_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.taskdata
    ADD CONSTRAINT taskdata_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.tasks(id);


--
-- TOC entry 3273 (class 2606 OID 16916)
-- Name: tasklogs tasklogs_task_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.tasklogs
    ADD CONSTRAINT tasklogs_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.tasks(id);


--
-- TOC entry 3271 (class 2606 OID 16895)
-- Name: tasks tasks_runnable_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_runnable_id_fkey FOREIGN KEY (runnable_id) REFERENCES public.runnables(id);


--
-- TOC entry 3272 (class 2606 OID 16900)
-- Name: tasks tasks_service_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_service_id_fkey FOREIGN KEY (service_id) REFERENCES public.services(id);


--
-- TOC entry 3237 (class 2606 OID 16470)
-- Name: users users_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id);


--
-- TOC entry 3268 (class 2606 OID 16847)
-- Name: workflow_annotations workflow_annotations_workflow_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.workflow_annotations
    ADD CONSTRAINT workflow_annotations_workflow_id_fkey FOREIGN KEY (workflow_id) REFERENCES public.workflows(id);


--
-- TOC entry 3259 (class 2606 OID 16728)
-- Name: workflowaccesses workflowaccesses_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.workflowaccesses
    ADD CONSTRAINT workflowaccesses_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 3258 (class 2606 OID 16723)
-- Name: workflowaccesses workflowaccesses_workflow_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.workflowaccesses
    ADD CONSTRAINT workflowaccesses_workflow_id_fkey FOREIGN KEY (workflow_id) REFERENCES public.workflows(id);


--
-- TOC entry 3260 (class 2606 OID 16744)
-- Name: workflowparams workflowparams_workflow_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.workflowparams
    ADD CONSTRAINT workflowparams_workflow_id_fkey FOREIGN KEY (workflow_id) REFERENCES public.workflows(id);


--
-- TOC entry 3261 (class 2606 OID 16760)
-- Name: workflowreturns workflowreturns_workflow_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.workflowreturns
    ADD CONSTRAINT workflowreturns_workflow_id_fkey FOREIGN KEY (workflow_id) REFERENCES public.workflows(id);


--
-- TOC entry 3243 (class 2606 OID 16552)
-- Name: workflows workflows_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.workflows
    ADD CONSTRAINT workflows_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


-- Completed on 2023-02-12 16:53:08 UTC
--
-- TOC entry 3204 (class 0 OID 25054)
-- Dependencies: 203
-- Data for Name: datasources; Type: TABLE DATA; Schema: public; Owner: phenodoop
--

COPY public.datasources (id, name, type, url, root, public, "user", password, prefix, active, temp) FROM stdin;
2	LocalFS	posix	/home/vizsciflow/storage	/	/public	users	\N	\N	t	\N
1	HDFS	hdfs	hdfs://206.12.102.75:54310/	/user	/public	hadoop	spark#2018	HDFS	f	\N
3	GalaxyFS	gfs	http://sr-p2irc-big8.usask.ca:8080	/	\N	\N	7483fa940d53add053903042c39f853a	GalaxyFS	f	\N
4	HDFS-BIG	hdfs	http://sr-p2irc-big1.usask.ca:50070	/user	/public	hdfs	\N	GalaxyFS	f	\N
5	COPERNICUS	scidata	/copernicus	/	\N	\N	\N	https://p2irc-data-dev.usask.ca/api	f	\N
\.


--
-- TOC entry 3202 (class 0 OID 25043)
-- Dependencies: 201
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: phenodoop
--

COPY public.roles (id, name, "default", permissions) FROM stdin;
1	User	t	15
2	Moderator	f	63
3	Administrator	f	255
\.


--
-- TOC entry 3208 (class 0 OID 25117)
-- Dependencies: 215
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: phenodoop
--

COPY public.users (id, email, username, role_id, password_hash, confirmed, name, location, about_me, member_since, last_seen, avatar_hash, oid) FROM stdin;
2	admin@gmail.com	admin	1	pbkdf2:sha256:150000$Mq3vil34$2eed4c2335b885d935afd3431335a43f5805cc7898cf4bf38e4f9d33f6b93088	t	\N	\N	\N	2022-03-26 02:08:18.006236	2022-03-26 02:08:18.006247	75d23af433e0cea4c0e45a56dba18b30	0
7	vuchi81928@gmail.com	chi	1	pbkdf2:sha256:150000$vim3eMTc$80bc6c5cd013bb75ce9be452c42d019f6a6e6ab9515796cb5470efdb3ed2b75c	t	\N	\N	\N	2022-06-22 15:43:31.865117	2022-07-06 17:37:30.159847	2ecfe9f56b5b666566a9f8adbf52c8f2	0
8	\N	lij313	3	\N	t	\N	\N	\N	2022-06-22 20:25:46.80228	2022-06-22 20:28:10.771697	\N	1
6	chi@gmail.com	Chi	1	pbkdf2:sha256:150000$1oAjICcB$3ab9a16d92fb628191e7e8ca6c397058ccd52164e7cbee6c300dc65b468648a7	t	\N	\N	\N	2022-06-13 20:21:13.378088	2022-11-21 23:31:41.711652	77b82a4b3885db1bbdd501151ef041bb	0
4	\N	ylw576	3	\N	t	\N	\N	\N	2022-05-17 20:09:35.87382	2022-09-02 16:19:08.317255	\N	1
5	\N	cpv616	3	\N	t	\N	\N	\N	2022-05-17 21:41:25.399188	2022-11-12 20:15:32.833469	\N	1
11	\N	mda439	3	\N	t	\N	\N	\N	2023-01-05 17:08:15.295159	2023-01-05 17:21:48.127244	\N	1
9	\N	are390	3	\N	t	\N	\N	\N	2022-06-22 21:35:29.112098	2022-06-22 21:37:48.5812	\N	1
3	\N	muh026	3	\N	t	\N	\N	\N	2022-03-26 17:33:02.625438	2023-01-27 17:43:54.134476	\N	1
10	\N	fst926	3	\N	t	\N	\N	\N	2022-08-31 16:44:05.390019	2022-08-31 16:44:35.547436	\N	1
1	testuser@usask.ca	testuser	1	pbkdf2:sha256:150000$MlNghkPq$62c21d6af5e1f9e3aec6d15b552590a7548bd6fc62d1d6652754ba10579dd8a8	t	\N	\N	\N	2022-03-26 02:08:17.969979	2023-01-28 15:51:12.215524	d13bd861fa052670527a8bd372a9fb24	0
12	\N	mdn769	3	\N	t	\N	\N	\N	2023-01-05 17:25:58.59458	2023-01-05 17:25:58.594589	\N	1
13	\N	faa634	3	\N	t	\N	\N	\N	2023-01-05 18:27:29.813162	2023-01-05 18:27:29.813172	\N	1
\.


--
-- TOC entry 3209 (class 0 OID 25165)
-- Dependencies: 220
-- Data for Name: follows; Type: TABLE DATA; Schema: public; Owner: phenodoop
--

COPY public.follows (follower_id, followed_id, "timestamp") FROM stdin;
1	1	2022-03-26 02:08:17.975892
2	2	2022-03-26 02:08:18.008072
3	3	2022-03-26 17:33:02.661472
4	4	2022-05-17 20:09:35.921485
5	5	2022-05-17 21:41:25.401706
6	6	2022-06-13 20:21:13.381629
7	7	2022-06-22 15:43:31.9016
8	8	2022-06-22 20:25:46.858244
9	9	2022-06-22 21:35:29.113894
10	10	2022-08-31 16:44:05.479445
11	11	2023-01-05 17:08:15.353305
12	12	2023-01-05 17:25:58.596838
13	13	2023-01-05 18:27:29.815072
\.


--
-- TOC entry 3206 (class 0 OID 25095)
-- Dependencies: 211
-- Data for Name: mimetypes; Type: TABLE DATA; Schema: public; Owner: phenodoop
--

COPY public.mimetypes (id, name, "desc", extension) FROM stdin;
1	text/plain	lastz generated by BlastZ tool	lastz
2	text/plain	BED file	bed
3	text/plain	dups file	localdups
4	text/plain	filtered	filtered
5	text/plain	tandems	tandems
6	text/plain	all	all
7	text/plain	aligncoords	aligncoords
8	text/plain	gcoords	gcoords
9	text/plain	gevolinks	gevolinks
10	text/plain	condensed	condensed
11	text/plain	GeneOrder	go
12	text/plain	last tool output	last
13	text/plain	\N	ks
14	text/plain	\N	sam
15	text/plain	\N	txt
\.


--
-- TOC entry 3215 (class 0 OID 0)
-- Dependencies: 202
-- Name: datasources_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.datasources_id_seq', 5, true);


--
-- TOC entry 3216 (class 0 OID 0)
-- Dependencies: 210
-- Name: mimetypes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.mimetypes_id_seq', 15, true);


--
-- TOC entry 3217 (class 0 OID 0)
-- Dependencies: 200
-- Name: roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.roles_id_seq', 3, true);


--
-- TOC entry 3218 (class 0 OID 0)
-- Dependencies: 214
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.users_id_seq', 13, true);

-- Name: data_chunks; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.data_chunks (
    id integer NOT NULL,
    user_id integer,
    file_uuid text,
    path text,
    chunk integer,
    total_chunk integer,
    uploaded_size text,
    total_size text
);


ALTER TABLE public.data_chunks OWNER TO phenodoop;

--
-- TOC entry 280 (class 1259 OID 18191)
-- Name: data_chunks_id_seq; Type: SEQUENCE; Schema: public; Owner: phenodoop
--

CREATE SEQUENCE public.data_chunks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_chunks_id_seq OWNER TO phenodoop;

--
-- TOC entry 3238 (class 0 OID 0)
-- Dependencies: 280
-- Name: data_chunks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.data_chunks_id_seq OWNED BY public.data_chunks.id;


--
-- TOC entry 276 (class 1259 OID 18159)
-- Name: dockercontainers; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.dockercontainers (
    id integer NOT NULL,
    user_id integer NOT NULL,
    image_id integer NOT NULL,
    name text NOT NULL,
    args text,
    command text
);


ALTER TABLE public.dockercontainers OWNER TO phenodoop;

--
-- TOC entry 277 (class 1259 OID 18165)
-- Name: dockercontainers_id_seq; Type: SEQUENCE; Schema: public; Owner: phenodoop
--

CREATE SEQUENCE public.dockercontainers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dockercontainers_id_seq OWNER TO phenodoop;

--
-- TOC entry 3239 (class 0 OID 0)
-- Dependencies: 277
-- Name: dockercontainers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.dockercontainers_id_seq OWNED BY public.dockercontainers.id;


--
-- TOC entry 278 (class 1259 OID 18167)
-- Name: dockerimages; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.dockerimages (
    id integer NOT NULL,
    user_id integer,
    name text
);


ALTER TABLE public.dockerimages OWNER TO phenodoop;

--
-- TOC entry 279 (class 1259 OID 18173)
-- Name: dockerimages_id_seq; Type: SEQUENCE; Schema: public; Owner: phenodoop
--

CREATE SEQUENCE public.dockerimages_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dockerimages_id_seq OWNER TO phenodoop;

--
-- TOC entry 3240 (class 0 OID 0)
-- Dependencies: 279
-- Name: dockerimages_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.dockerimages_id_seq OWNED BY public.dockerimages.id;


--
-- TOC entry 3096 (class 2604 OID 18200)
-- Name: data_chunks id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_chunks ALTER COLUMN id SET DEFAULT nextval('public.data_chunks_id_seq'::regclass);


--
-- TOC entry 3094 (class 2604 OID 18175)
-- Name: dockercontainers id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.dockercontainers ALTER COLUMN id SET DEFAULT nextval('public.dockercontainers_id_seq'::regclass);


--
-- TOC entry 3095 (class 2604 OID 18176)
-- Name: dockerimages id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.dockerimages ALTER COLUMN id SET DEFAULT nextval('public.dockerimages_id_seq'::regclass);


--
-- TOC entry 3098 (class 2606 OID 18178)
-- Name: dockercontainers dockercontainers_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.dockercontainers
    ADD CONSTRAINT dockercontainers_pkey PRIMARY KEY (id);


--
-- TOC entry 3100 (class 2606 OID 18180)
-- Name: dockerimages dockerimages_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.dockerimages
    ADD CONSTRAINT dockerimages_pkey PRIMARY KEY (id);


--
-- TOC entry 3101 (class 2606 OID 18181)
-- Name: dockercontainers fk_dockerimages_dockercontainers; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.dockercontainers
    ADD CONSTRAINT fk_dockerimages_dockercontainers FOREIGN KEY (image_id) REFERENCES public.dockerimages(id);


--
-- TOC entry 3102 (class 2606 OID 18186)
-- Name: dockercontainers fk_users_dockercontainers; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.dockercontainers
    ADD CONSTRAINT fk_users_dockercontainers FOREIGN KEY (user_id) REFERENCES public.users(id);

-- Completed on 2023-01-29 05:16:34 UTC

--
-- PostgreSQL database dump complete
--


--
-- PostgreSQL database dump complete
--

