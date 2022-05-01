--
-- PostgreSQL database dump
--

-- Dumped from database version 13.6
-- Dumped by pg_dump version 13.6

-- Started on 2022-03-22 21:42:19 UTC

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
-- TOC entry 242 (class 1259 OID 18730)
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
-- TOC entry 241 (class 1259 OID 18728)
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
-- TOC entry 3394 (class 0 OID 0)
-- Dependencies: 241
-- Name: comments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.comments_id_seq OWNED BY public.comments.id;


--
-- TOC entry 213 (class 1259 OID 18485)
-- Name: data; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.data (
    id integer NOT NULL,
    value json
);


ALTER TABLE public.data OWNER TO phenodoop;

--
-- TOC entry 240 (class 1259 OID 18712)
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
-- TOC entry 239 (class 1259 OID 18710)
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
-- TOC entry 3395 (class 0 OID 0)
-- Dependencies: 239
-- Name: data_allocations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.data_allocations_id_seq OWNED BY public.data_allocations.id;


--
-- TOC entry 234 (class 1259 OID 18660)
-- Name: data_annotations; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.data_annotations (
    id integer NOT NULL,
    data_id integer,
    tag text NOT NULL
);


ALTER TABLE public.data_annotations OWNER TO phenodoop;

--
-- TOC entry 233 (class 1259 OID 18658)
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
-- TOC entry 3396 (class 0 OID 0)
-- Dependencies: 233
-- Name: data_annotations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.data_annotations_id_seq OWNED BY public.data_annotations.id;


--
-- TOC entry 212 (class 1259 OID 18483)
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
-- TOC entry 3397 (class 0 OID 0)
-- Dependencies: 212
-- Name: data_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.data_id_seq OWNED BY public.data.id;


--
-- TOC entry 238 (class 1259 OID 18694)
-- Name: data_mimetypes; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.data_mimetypes (
    id integer NOT NULL,
    data_id integer NOT NULL,
    mimetype_id integer NOT NULL
);


ALTER TABLE public.data_mimetypes OWNER TO phenodoop;

--
-- TOC entry 237 (class 1259 OID 18692)
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
-- TOC entry 3398 (class 0 OID 0)
-- Dependencies: 237
-- Name: data_mimetypes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.data_mimetypes_id_seq OWNED BY public.data_mimetypes.id;


--
-- TOC entry 232 (class 1259 OID 18642)
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
-- TOC entry 231 (class 1259 OID 18640)
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
-- TOC entry 3399 (class 0 OID 0)
-- Dependencies: 231
-- Name: data_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.data_permissions_id_seq OWNED BY public.data_permissions.id;


--
-- TOC entry 219 (class 1259 OID 18530)
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
-- TOC entry 218 (class 1259 OID 18528)
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
-- TOC entry 3400 (class 0 OID 0)
-- Dependencies: 218
-- Name: data_properties_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.data_properties_id_seq OWNED BY public.data_properties.id;


--
-- TOC entry 236 (class 1259 OID 18676)
-- Name: data_visualizers; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.data_visualizers (
    id integer NOT NULL,
    data_id integer NOT NULL,
    visualizer_id integer NOT NULL
);


ALTER TABLE public.data_visualizers OWNER TO phenodoop;

--
-- TOC entry 235 (class 1259 OID 18674)
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
-- TOC entry 3401 (class 0 OID 0)
-- Dependencies: 235
-- Name: data_visualizers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.data_visualizers_id_seq OWNED BY public.data_visualizers.id;


--
-- TOC entry 205 (class 1259 OID 18444)
-- Name: datasets; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.datasets (
    id integer NOT NULL,
    schema json NOT NULL
);


ALTER TABLE public.datasets OWNER TO phenodoop;

--
-- TOC entry 204 (class 1259 OID 18442)
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
-- TOC entry 3402 (class 0 OID 0)
-- Dependencies: 204
-- Name: datasets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.datasets_id_seq OWNED BY public.datasets.id;


--
-- TOC entry 217 (class 1259 OID 18514)
-- Name: datasource_allocations; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.datasource_allocations (
    id integer NOT NULL,
    datasource_id integer,
    url text NOT NULL
);


ALTER TABLE public.datasource_allocations OWNER TO phenodoop;

--
-- TOC entry 216 (class 1259 OID 18512)
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
-- TOC entry 3403 (class 0 OID 0)
-- Dependencies: 216
-- Name: datasource_allocations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.datasource_allocations_id_seq OWNED BY public.datasource_allocations.id;


--
-- TOC entry 203 (class 1259 OID 18433)
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
    prefix character text,
    active boolean,
    temp text
);


ALTER TABLE public.datasources OWNER TO phenodoop;

--
-- TOC entry 202 (class 1259 OID 18431)
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
-- TOC entry 3404 (class 0 OID 0)
-- Dependencies: 202
-- Name: datasources_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.datasources_id_seq OWNED BY public.datasources.id;


--
-- TOC entry 230 (class 1259 OID 18626)
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
-- TOC entry 229 (class 1259 OID 18624)
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
-- TOC entry 3405 (class 0 OID 0)
-- Dependencies: 229
-- Name: filter_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.filter_history_id_seq OWNED BY public.filter_history.id;


--
-- TOC entry 228 (class 1259 OID 18610)
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
-- TOC entry 227 (class 1259 OID 18608)
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
-- TOC entry 3406 (class 0 OID 0)
-- Dependencies: 227
-- Name: filters_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.filters_id_seq OWNED BY public.filters.id;


--
-- TOC entry 220 (class 1259 OID 18544)
-- Name: follows; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.follows (
    follower_id integer NOT NULL,
    followed_id integer NOT NULL,
    "timestamp" timestamp without time zone
);


ALTER TABLE public.follows OWNER TO phenodoop;

--
-- TOC entry 262 (class 1259 OID 18912)
-- Name: indata; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.indata (
    id integer NOT NULL,
    task_id integer,
    data_id integer
);


ALTER TABLE public.indata OWNER TO phenodoop;

--
-- TOC entry 261 (class 1259 OID 18910)
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
-- TOC entry 3407 (class 0 OID 0)
-- Dependencies: 261
-- Name: indata_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.indata_id_seq OWNED BY public.indata.id;


--
-- TOC entry 211 (class 1259 OID 18474)
-- Name: mimetypes; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.mimetypes (
    id integer NOT NULL,
    name text NOT NULL,
    "desc" text
);


ALTER TABLE public.mimetypes OWNER TO phenodoop;

--
-- TOC entry 210 (class 1259 OID 18472)
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
-- TOC entry 3408 (class 0 OID 0)
-- Dependencies: 210
-- Name: mimetypes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.mimetypes_id_seq OWNED BY public.mimetypes.id;


--
-- TOC entry 246 (class 1259 OID 18770)
-- Name: params; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.params (
    id integer NOT NULL,
    service_id integer,
    value json NOT NULL
);


ALTER TABLE public.params OWNER TO phenodoop;

--
-- TOC entry 245 (class 1259 OID 18768)
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
-- TOC entry 3409 (class 0 OID 0)
-- Dependencies: 245
-- Name: params_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.params_id_seq OWNED BY public.params.id;


--
-- TOC entry 222 (class 1259 OID 18561)
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
-- TOC entry 221 (class 1259 OID 18559)
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
-- TOC entry 3410 (class 0 OID 0)
-- Dependencies: 221
-- Name: posts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.posts_id_seq OWNED BY public.posts.id;


--
-- TOC entry 248 (class 1259 OID 18786)
-- Name: returns; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.returns (
    id integer NOT NULL,
    service_id integer,
    value json NOT NULL
);


ALTER TABLE public.returns OWNER TO phenodoop;

--
-- TOC entry 247 (class 1259 OID 18784)
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
-- TOC entry 3411 (class 0 OID 0)
-- Dependencies: 247
-- Name: returns_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.returns_id_seq OWNED BY public.returns.id;


--
-- TOC entry 201 (class 1259 OID 18422)
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
-- TOC entry 200 (class 1259 OID 18420)
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
-- TOC entry 3412 (class 0 OID 0)
-- Dependencies: 200
-- Name: roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.roles_id_seq OWNED BY public.roles.id;


--
-- TOC entry 252 (class 1259 OID 18820)
-- Name: runnables; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.runnables (
    id integer NOT NULL,
    workflow_id integer,
    user_id integer,
    celery_id character varying(64),
    status character varying(30),
    script text NOT NULL,
    args text,
    "out" text,
    error text,
    view text,
    duration integer,
    started_on timestamp without time zone,
    created_on timestamp without time zone,
    modified_on timestamp without time zone
);


ALTER TABLE public.runnables OWNER TO phenodoop;

--
-- TOC entry 251 (class 1259 OID 18818)
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
-- TOC entry 3413 (class 0 OID 0)
-- Dependencies: 251
-- Name: runnables_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.runnables_id_seq OWNED BY public.runnables.id;


--
-- TOC entry 250 (class 1259 OID 18802)
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
-- TOC entry 249 (class 1259 OID 18800)
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
-- TOC entry 3414 (class 0 OID 0)
-- Dependencies: 249
-- Name: serviceaccesses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.serviceaccesses_id_seq OWNED BY public.serviceaccesses.id;


--
-- TOC entry 226 (class 1259 OID 18594)
-- Name: services; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.services (
    id integer NOT NULL,
    user_id integer NOT NULL,
    value json NOT NULL,
    public boolean,
    active boolean
);


ALTER TABLE public.services OWNER TO phenodoop;

--
-- TOC entry 225 (class 1259 OID 18592)
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
-- TOC entry 3415 (class 0 OID 0)
-- Dependencies: 225
-- Name: services_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.services_id_seq OWNED BY public.services.id;


--
-- TOC entry 260 (class 1259 OID 18894)
-- Name: taskdata; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.taskdata (
    id integer NOT NULL,
    task_id integer,
    data_id integer
);


ALTER TABLE public.taskdata OWNER TO phenodoop;

--
-- TOC entry 259 (class 1259 OID 18892)
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
-- TOC entry 3416 (class 0 OID 0)
-- Dependencies: 259
-- Name: taskdata_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.taskdata_id_seq OWNED BY public.taskdata.id;


--
-- TOC entry 258 (class 1259 OID 18878)
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
-- TOC entry 257 (class 1259 OID 18876)
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
-- TOC entry 3417 (class 0 OID 0)
-- Dependencies: 257
-- Name: tasklogs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.tasklogs_id_seq OWNED BY public.tasklogs.id;


--
-- TOC entry 256 (class 1259 OID 18857)
-- Name: tasks; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.tasks (
    id integer NOT NULL,
    runnable_id integer,
    service_id integer,
    started_on timestamp without time zone,
    ended_on timestamp without time zone,
    status text,
    comment text
);


ALTER TABLE public.tasks OWNER TO phenodoop;

--
-- TOC entry 255 (class 1259 OID 18855)
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
-- TOC entry 3418 (class 0 OID 0)
-- Dependencies: 255
-- Name: tasks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.tasks_id_seq OWNED BY public.tasks.id;


--
-- TOC entry 207 (class 1259 OID 18455)
-- Name: taskstatus; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.taskstatus (
    id integer NOT NULL,
    name character varying(30)
);


ALTER TABLE public.taskstatus OWNER TO phenodoop;

--
-- TOC entry 206 (class 1259 OID 18453)
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
-- TOC entry 3419 (class 0 OID 0)
-- Dependencies: 206
-- Name: taskstatus_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.taskstatus_id_seq OWNED BY public.taskstatus.id;


--
-- TOC entry 215 (class 1259 OID 18496)
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
-- TOC entry 214 (class 1259 OID 18494)
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
-- TOC entry 3420 (class 0 OID 0)
-- Dependencies: 214
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 209 (class 1259 OID 18463)
-- Name: visualizers; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.visualizers (
    id integer NOT NULL,
    name text NOT NULL,
    "desc" text
);


ALTER TABLE public.visualizers OWNER TO phenodoop;

--
-- TOC entry 208 (class 1259 OID 18461)
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
-- TOC entry 3421 (class 0 OID 0)
-- Dependencies: 208
-- Name: visualizers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.visualizers_id_seq OWNED BY public.visualizers.id;


--
-- TOC entry 254 (class 1259 OID 18841)
-- Name: workflow_annotations; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.workflow_annotations (
    id integer NOT NULL,
    workflow_id integer,
    tag text NOT NULL
);


ALTER TABLE public.workflow_annotations OWNER TO phenodoop;

--
-- TOC entry 253 (class 1259 OID 18839)
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
-- TOC entry 3422 (class 0 OID 0)
-- Dependencies: 253
-- Name: workflow_annotations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.workflow_annotations_id_seq OWNED BY public.workflow_annotations.id;


--
-- TOC entry 244 (class 1259 OID 18752)
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
-- TOC entry 243 (class 1259 OID 18750)
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
-- TOC entry 3423 (class 0 OID 0)
-- Dependencies: 243
-- Name: workflowaccesses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.workflowaccesses_id_seq OWNED BY public.workflowaccesses.id;


--
-- TOC entry 224 (class 1259 OID 18578)
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
    derived integer,
    args json
);


ALTER TABLE public.workflows OWNER TO phenodoop;

--
-- TOC entry 223 (class 1259 OID 18576)
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
-- TOC entry 3424 (class 0 OID 0)
-- Dependencies: 223
-- Name: workflows_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.workflows_id_seq OWNED BY public.workflows.id;


--
-- TOC entry 3077 (class 2604 OID 18733)
-- Name: comments id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.comments ALTER COLUMN id SET DEFAULT nextval('public.comments_id_seq'::regclass);


--
-- TOC entry 3063 (class 2604 OID 18488)
-- Name: data id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data ALTER COLUMN id SET DEFAULT nextval('public.data_id_seq'::regclass);


--
-- TOC entry 3076 (class 2604 OID 18715)
-- Name: data_allocations id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_allocations ALTER COLUMN id SET DEFAULT nextval('public.data_allocations_id_seq'::regclass);


--
-- TOC entry 3073 (class 2604 OID 18663)
-- Name: data_annotations id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_annotations ALTER COLUMN id SET DEFAULT nextval('public.data_annotations_id_seq'::regclass);


--
-- TOC entry 3075 (class 2604 OID 18697)
-- Name: data_mimetypes id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_mimetypes ALTER COLUMN id SET DEFAULT nextval('public.data_mimetypes_id_seq'::regclass);


--
-- TOC entry 3072 (class 2604 OID 18645)
-- Name: data_permissions id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_permissions ALTER COLUMN id SET DEFAULT nextval('public.data_permissions_id_seq'::regclass);


--
-- TOC entry 3066 (class 2604 OID 18533)
-- Name: data_properties id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_properties ALTER COLUMN id SET DEFAULT nextval('public.data_properties_id_seq'::regclass);


--
-- TOC entry 3074 (class 2604 OID 18679)
-- Name: data_visualizers id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_visualizers ALTER COLUMN id SET DEFAULT nextval('public.data_visualizers_id_seq'::regclass);


--
-- TOC entry 3059 (class 2604 OID 18447)
-- Name: datasets id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.datasets ALTER COLUMN id SET DEFAULT nextval('public.datasets_id_seq'::regclass);


--
-- TOC entry 3065 (class 2604 OID 18517)
-- Name: datasource_allocations id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.datasource_allocations ALTER COLUMN id SET DEFAULT nextval('public.datasource_allocations_id_seq'::regclass);


--
-- TOC entry 3058 (class 2604 OID 18436)
-- Name: datasources id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.datasources ALTER COLUMN id SET DEFAULT nextval('public.datasources_id_seq'::regclass);


--
-- TOC entry 3071 (class 2604 OID 18629)
-- Name: filter_history id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.filter_history ALTER COLUMN id SET DEFAULT nextval('public.filter_history_id_seq'::regclass);


--
-- TOC entry 3070 (class 2604 OID 18613)
-- Name: filters id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.filters ALTER COLUMN id SET DEFAULT nextval('public.filters_id_seq'::regclass);


--
-- TOC entry 3087 (class 2604 OID 18915)
-- Name: indata id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.indata ALTER COLUMN id SET DEFAULT nextval('public.indata_id_seq'::regclass);


--
-- TOC entry 3062 (class 2604 OID 18477)
-- Name: mimetypes id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.mimetypes ALTER COLUMN id SET DEFAULT nextval('public.mimetypes_id_seq'::regclass);


--
-- TOC entry 3079 (class 2604 OID 18773)
-- Name: params id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.params ALTER COLUMN id SET DEFAULT nextval('public.params_id_seq'::regclass);


--
-- TOC entry 3067 (class 2604 OID 18564)
-- Name: posts id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.posts ALTER COLUMN id SET DEFAULT nextval('public.posts_id_seq'::regclass);


--
-- TOC entry 3080 (class 2604 OID 18789)
-- Name: returns id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.returns ALTER COLUMN id SET DEFAULT nextval('public.returns_id_seq'::regclass);


--
-- TOC entry 3057 (class 2604 OID 18425)
-- Name: roles id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.roles ALTER COLUMN id SET DEFAULT nextval('public.roles_id_seq'::regclass);


--
-- TOC entry 3082 (class 2604 OID 18823)
-- Name: runnables id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.runnables ALTER COLUMN id SET DEFAULT nextval('public.runnables_id_seq'::regclass);


--
-- TOC entry 3081 (class 2604 OID 18805)
-- Name: serviceaccesses id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.serviceaccesses ALTER COLUMN id SET DEFAULT nextval('public.serviceaccesses_id_seq'::regclass);


--
-- TOC entry 3069 (class 2604 OID 18597)
-- Name: services id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.services ALTER COLUMN id SET DEFAULT nextval('public.services_id_seq'::regclass);


--
-- TOC entry 3086 (class 2604 OID 18897)
-- Name: taskdata id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.taskdata ALTER COLUMN id SET DEFAULT nextval('public.taskdata_id_seq'::regclass);


--
-- TOC entry 3085 (class 2604 OID 18881)
-- Name: tasklogs id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.tasklogs ALTER COLUMN id SET DEFAULT nextval('public.tasklogs_id_seq'::regclass);


--
-- TOC entry 3084 (class 2604 OID 18860)
-- Name: tasks id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.tasks ALTER COLUMN id SET DEFAULT nextval('public.tasks_id_seq'::regclass);


--
-- TOC entry 3060 (class 2604 OID 18458)
-- Name: taskstatus id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.taskstatus ALTER COLUMN id SET DEFAULT nextval('public.taskstatus_id_seq'::regclass);


--
-- TOC entry 3064 (class 2604 OID 18499)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 3061 (class 2604 OID 18466)
-- Name: visualizers id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.visualizers ALTER COLUMN id SET DEFAULT nextval('public.visualizers_id_seq'::regclass);


--
-- TOC entry 3083 (class 2604 OID 18844)
-- Name: workflow_annotations id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.workflow_annotations ALTER COLUMN id SET DEFAULT nextval('public.workflow_annotations_id_seq'::regclass);


--
-- TOC entry 3078 (class 2604 OID 18755)
-- Name: workflowaccesses id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.workflowaccesses ALTER COLUMN id SET DEFAULT nextval('public.workflowaccesses_id_seq'::regclass);


--
-- TOC entry 3068 (class 2604 OID 18581)
-- Name: workflows id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.workflows ALTER COLUMN id SET DEFAULT nextval('public.workflows_id_seq'::regclass);


--
-- TOC entry 3368 (class 0 OID 18730)
-- Dependencies: 242
-- Data for Name: comments; Type: TABLE DATA; Schema: public; Owner: phenodoop
--



--
-- TOC entry 3339 (class 0 OID 18485)
-- Dependencies: 213
-- Data for Name: data; Type: TABLE DATA; Schema: public; Owner: phenodoop
--



--
-- TOC entry 3366 (class 0 OID 18712)
-- Dependencies: 240
-- Data for Name: data_allocations; Type: TABLE DATA; Schema: public; Owner: phenodoop
--



--
-- TOC entry 3360 (class 0 OID 18660)
-- Dependencies: 234
-- Data for Name: data_annotations; Type: TABLE DATA; Schema: public; Owner: phenodoop
--



--
-- TOC entry 3364 (class 0 OID 18694)
-- Dependencies: 238
-- Data for Name: data_mimetypes; Type: TABLE DATA; Schema: public; Owner: phenodoop
--



--
-- TOC entry 3358 (class 0 OID 18642)
-- Dependencies: 232
-- Data for Name: data_permissions; Type: TABLE DATA; Schema: public; Owner: phenodoop
--



--
-- TOC entry 3345 (class 0 OID 18530)
-- Dependencies: 219
-- Data for Name: data_properties; Type: TABLE DATA; Schema: public; Owner: phenodoop
--



--
-- TOC entry 3362 (class 0 OID 18676)
-- Dependencies: 236
-- Data for Name: data_visualizers; Type: TABLE DATA; Schema: public; Owner: phenodoop
--



--
-- TOC entry 3331 (class 0 OID 18444)
-- Dependencies: 205
-- Data for Name: datasets; Type: TABLE DATA; Schema: public; Owner: phenodoop
--



--
-- TOC entry 3343 (class 0 OID 18514)
-- Dependencies: 217
-- Data for Name: datasource_allocations; Type: TABLE DATA; Schema: public; Owner: phenodoop
--



--
-- TOC entry 3329 (class 0 OID 18433)
-- Dependencies: 203
-- Data for Name: datasources; Type: TABLE DATA; Schema: public; Owner: phenodoop
--

INSERT INTO public.datasources VALUES (1, 'HDFS', 'hdfs', 'hdfs://206.12.102.75:54310/', '/user', '/public', 'hadoop', 'spark#2018', 'HDFS', true, NULL);
INSERT INTO public.datasources VALUES (2, 'LocalFS', 'posix', '/home/vizsciflow/storage', '/', '/public', NULL, NULL, NULL, true, NULL);
INSERT INTO public.datasources VALUES (3, 'GalaxyFS', 'gfs', 'http://sr-p2irc-big8.usask.ca:8080', '/', NULL, NULL, '7483fa940d53add053903042c39f853a', 'GalaxyFS', true, NULL);
INSERT INTO public.datasources VALUES (4, 'HDFS-BIG', 'hdfs', 'http://sr-p2irc-big1.usask.ca:50070', '/user', '/public', 'hdfs', NULL, 'GalaxyFS', true, NULL);
INSERT INTO public.datasources VALUES (5, 'COPERNICUS', 'scidata', '/copernicus', '/', NULL, NULL, NULL, 'https://p2irc-data-dev.usask.ca/api', true, NULL);


--
-- TOC entry 3356 (class 0 OID 18626)
-- Dependencies: 230
-- Data for Name: filter_history; Type: TABLE DATA; Schema: public; Owner: phenodoop
--



--
-- TOC entry 3354 (class 0 OID 18610)
-- Dependencies: 228
-- Data for Name: filters; Type: TABLE DATA; Schema: public; Owner: phenodoop
--



--
-- TOC entry 3346 (class 0 OID 18544)
-- Dependencies: 220
-- Data for Name: follows; Type: TABLE DATA; Schema: public; Owner: phenodoop
--



--
-- TOC entry 3388 (class 0 OID 18912)
-- Dependencies: 262
-- Data for Name: indata; Type: TABLE DATA; Schema: public; Owner: phenodoop
--



--
-- TOC entry 3337 (class 0 OID 18474)
-- Dependencies: 211
-- Data for Name: mimetypes; Type: TABLE DATA; Schema: public; Owner: phenodoop
--



--
-- TOC entry 3372 (class 0 OID 18770)
-- Dependencies: 246
-- Data for Name: params; Type: TABLE DATA; Schema: public; Owner: phenodoop
--



--
-- TOC entry 3348 (class 0 OID 18561)
-- Dependencies: 222
-- Data for Name: posts; Type: TABLE DATA; Schema: public; Owner: phenodoop
--



--
-- TOC entry 3374 (class 0 OID 18786)
-- Dependencies: 248
-- Data for Name: returns; Type: TABLE DATA; Schema: public; Owner: phenodoop
--



--
-- TOC entry 3327 (class 0 OID 18422)
-- Dependencies: 201
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: phenodoop
--

INSERT INTO public.roles VALUES (1, 'User', true, 15);
INSERT INTO public.roles VALUES (2, 'Moderator', false, 63);
INSERT INTO public.roles VALUES (3, 'Administrator', false, 255);


--
-- TOC entry 3378 (class 0 OID 18820)
-- Dependencies: 252
-- Data for Name: runnables; Type: TABLE DATA; Schema: public; Owner: phenodoop
--



--
-- TOC entry 3376 (class 0 OID 18802)
-- Dependencies: 250
-- Data for Name: serviceaccesses; Type: TABLE DATA; Schema: public; Owner: phenodoop
--



--
-- TOC entry 3352 (class 0 OID 18594)
-- Dependencies: 226
-- Data for Name: services; Type: TABLE DATA; Schema: public; Owner: phenodoop
--



--
-- TOC entry 3386 (class 0 OID 18894)
-- Dependencies: 260
-- Data for Name: taskdata; Type: TABLE DATA; Schema: public; Owner: phenodoop
--



--
-- TOC entry 3384 (class 0 OID 18878)
-- Dependencies: 258
-- Data for Name: tasklogs; Type: TABLE DATA; Schema: public; Owner: phenodoop
--



--
-- TOC entry 3382 (class 0 OID 18857)
-- Dependencies: 256
-- Data for Name: tasks; Type: TABLE DATA; Schema: public; Owner: phenodoop
--



--
-- TOC entry 3333 (class 0 OID 18455)
-- Dependencies: 207
-- Data for Name: taskstatus; Type: TABLE DATA; Schema: public; Owner: phenodoop
--



--
-- TOC entry 3341 (class 0 OID 18496)
-- Dependencies: 215
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: phenodoop
--



--
-- TOC entry 3335 (class 0 OID 18463)
-- Dependencies: 209
-- Data for Name: visualizers; Type: TABLE DATA; Schema: public; Owner: phenodoop
--



--
-- TOC entry 3380 (class 0 OID 18841)
-- Dependencies: 254
-- Data for Name: workflow_annotations; Type: TABLE DATA; Schema: public; Owner: phenodoop
--



--
-- TOC entry 3370 (class 0 OID 18752)
-- Dependencies: 244
-- Data for Name: workflowaccesses; Type: TABLE DATA; Schema: public; Owner: phenodoop
--



--
-- TOC entry 3350 (class 0 OID 18578)
-- Dependencies: 224
-- Data for Name: workflows; Type: TABLE DATA; Schema: public; Owner: phenodoop
--



--
-- TOC entry 3425 (class 0 OID 0)
-- Dependencies: 241
-- Name: comments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.comments_id_seq', 1, false);


--
-- TOC entry 3426 (class 0 OID 0)
-- Dependencies: 239
-- Name: data_allocations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.data_allocations_id_seq', 1, false);


--
-- TOC entry 3427 (class 0 OID 0)
-- Dependencies: 233
-- Name: data_annotations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.data_annotations_id_seq', 1, false);


--
-- TOC entry 3428 (class 0 OID 0)
-- Dependencies: 212
-- Name: data_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.data_id_seq', 1, false);


--
-- TOC entry 3429 (class 0 OID 0)
-- Dependencies: 237
-- Name: data_mimetypes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.data_mimetypes_id_seq', 1, false);


--
-- TOC entry 3430 (class 0 OID 0)
-- Dependencies: 231
-- Name: data_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.data_permissions_id_seq', 1, false);


--
-- TOC entry 3431 (class 0 OID 0)
-- Dependencies: 218
-- Name: data_properties_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.data_properties_id_seq', 1, false);


--
-- TOC entry 3432 (class 0 OID 0)
-- Dependencies: 235
-- Name: data_visualizers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.data_visualizers_id_seq', 1, false);


--
-- TOC entry 3433 (class 0 OID 0)
-- Dependencies: 204
-- Name: datasets_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.datasets_id_seq', 1, false);


--
-- TOC entry 3434 (class 0 OID 0)
-- Dependencies: 216
-- Name: datasource_allocations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.datasource_allocations_id_seq', 1, false);


--
-- TOC entry 3435 (class 0 OID 0)
-- Dependencies: 202
-- Name: datasources_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.datasources_id_seq', 4, true);


--
-- TOC entry 3436 (class 0 OID 0)
-- Dependencies: 229
-- Name: filter_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.filter_history_id_seq', 1, false);


--
-- TOC entry 3437 (class 0 OID 0)
-- Dependencies: 227
-- Name: filters_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.filters_id_seq', 1, false);


--
-- TOC entry 3438 (class 0 OID 0)
-- Dependencies: 261
-- Name: indata_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.indata_id_seq', 1, false);


--
-- TOC entry 3439 (class 0 OID 0)
-- Dependencies: 210
-- Name: mimetypes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.mimetypes_id_seq', 1, false);


--
-- TOC entry 3440 (class 0 OID 0)
-- Dependencies: 245
-- Name: params_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.params_id_seq', 1, false);


--
-- TOC entry 3441 (class 0 OID 0)
-- Dependencies: 221
-- Name: posts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.posts_id_seq', 1, false);


--
-- TOC entry 3442 (class 0 OID 0)
-- Dependencies: 247
-- Name: returns_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.returns_id_seq', 1, false);


--
-- TOC entry 3443 (class 0 OID 0)
-- Dependencies: 200
-- Name: roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.roles_id_seq', 3, true);


--
-- TOC entry 3444 (class 0 OID 0)
-- Dependencies: 251
-- Name: runnables_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.runnables_id_seq', 1, false);


--
-- TOC entry 3445 (class 0 OID 0)
-- Dependencies: 249
-- Name: serviceaccesses_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.serviceaccesses_id_seq', 1, false);


--
-- TOC entry 3446 (class 0 OID 0)
-- Dependencies: 225
-- Name: services_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.services_id_seq', 1, false);


--
-- TOC entry 3447 (class 0 OID 0)
-- Dependencies: 259
-- Name: taskdata_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.taskdata_id_seq', 1, false);


--
-- TOC entry 3448 (class 0 OID 0)
-- Dependencies: 257
-- Name: tasklogs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.tasklogs_id_seq', 1, false);


--
-- TOC entry 3449 (class 0 OID 0)
-- Dependencies: 255
-- Name: tasks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.tasks_id_seq', 1, false);


--
-- TOC entry 3450 (class 0 OID 0)
-- Dependencies: 206
-- Name: taskstatus_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.taskstatus_id_seq', 1, false);


--
-- TOC entry 3451 (class 0 OID 0)
-- Dependencies: 214
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.users_id_seq', 1, false);


--
-- TOC entry 3452 (class 0 OID 0)
-- Dependencies: 208
-- Name: visualizers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.visualizers_id_seq', 1, false);


--
-- TOC entry 3453 (class 0 OID 0)
-- Dependencies: 253
-- Name: workflow_annotations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.workflow_annotations_id_seq', 1, false);


--
-- TOC entry 3454 (class 0 OID 0)
-- Dependencies: 243
-- Name: workflowaccesses_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.workflowaccesses_id_seq', 1, false);


--
-- TOC entry 3455 (class 0 OID 0)
-- Dependencies: 223
-- Name: workflows_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.workflows_id_seq', 1, false);


--
-- TOC entry 3137 (class 2606 OID 18738)
-- Name: comments comments_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_pkey PRIMARY KEY (id);


--
-- TOC entry 3135 (class 2606 OID 18717)
-- Name: data_allocations data_allocations_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_allocations
    ADD CONSTRAINT data_allocations_pkey PRIMARY KEY (id);


--
-- TOC entry 3129 (class 2606 OID 18668)
-- Name: data_annotations data_annotations_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_annotations
    ADD CONSTRAINT data_annotations_pkey PRIMARY KEY (id);


--
-- TOC entry 3133 (class 2606 OID 18699)
-- Name: data_mimetypes data_mimetypes_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_mimetypes
    ADD CONSTRAINT data_mimetypes_pkey PRIMARY KEY (id);


--
-- TOC entry 3127 (class 2606 OID 18647)
-- Name: data_permissions data_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_permissions
    ADD CONSTRAINT data_permissions_pkey PRIMARY KEY (id);


--
-- TOC entry 3104 (class 2606 OID 18493)
-- Name: data data_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data
    ADD CONSTRAINT data_pkey PRIMARY KEY (id);


--
-- TOC entry 3112 (class 2606 OID 18538)
-- Name: data_properties data_properties_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_properties
    ADD CONSTRAINT data_properties_pkey PRIMARY KEY (id);


--
-- TOC entry 3131 (class 2606 OID 18681)
-- Name: data_visualizers data_visualizers_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_visualizers
    ADD CONSTRAINT data_visualizers_pkey PRIMARY KEY (id);


--
-- TOC entry 3096 (class 2606 OID 18452)
-- Name: datasets datasets_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.datasets
    ADD CONSTRAINT datasets_pkey PRIMARY KEY (id);


--
-- TOC entry 3110 (class 2606 OID 18522)
-- Name: datasource_allocations datasource_allocations_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.datasource_allocations
    ADD CONSTRAINT datasource_allocations_pkey PRIMARY KEY (id);


--
-- TOC entry 3094 (class 2606 OID 18441)
-- Name: datasources datasources_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.datasources
    ADD CONSTRAINT datasources_pkey PRIMARY KEY (id);


--
-- TOC entry 3125 (class 2606 OID 18634)
-- Name: filter_history filter_history_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.filter_history
    ADD CONSTRAINT filter_history_pkey PRIMARY KEY (id);


--
-- TOC entry 3123 (class 2606 OID 18618)
-- Name: filters filters_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.filters
    ADD CONSTRAINT filters_pkey PRIMARY KEY (id);


--
-- TOC entry 3114 (class 2606 OID 18548)
-- Name: follows follows_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.follows
    ADD CONSTRAINT follows_pkey PRIMARY KEY (follower_id, followed_id);


--
-- TOC entry 3158 (class 2606 OID 18917)
-- Name: indata indata_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.indata
    ADD CONSTRAINT indata_pkey PRIMARY KEY (id);


--
-- TOC entry 3102 (class 2606 OID 18482)
-- Name: mimetypes mimetypes_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.mimetypes
    ADD CONSTRAINT mimetypes_pkey PRIMARY KEY (id);


--
-- TOC entry 3142 (class 2606 OID 18778)
-- Name: params params_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.params
    ADD CONSTRAINT params_pkey PRIMARY KEY (id);


--
-- TOC entry 3117 (class 2606 OID 18569)
-- Name: posts posts_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_pkey PRIMARY KEY (id);


--
-- TOC entry 3144 (class 2606 OID 18794)
-- Name: returns returns_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.returns
    ADD CONSTRAINT returns_pkey PRIMARY KEY (id);


--
-- TOC entry 3090 (class 2606 OID 18429)
-- Name: roles roles_name_key; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_name_key UNIQUE (name);


--
-- TOC entry 3092 (class 2606 OID 18427)
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- TOC entry 3148 (class 2606 OID 18828)
-- Name: runnables runnables_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.runnables
    ADD CONSTRAINT runnables_pkey PRIMARY KEY (id);


--
-- TOC entry 3146 (class 2606 OID 18807)
-- Name: serviceaccesses serviceaccesses_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.serviceaccesses
    ADD CONSTRAINT serviceaccesses_pkey PRIMARY KEY (id);


--
-- TOC entry 3121 (class 2606 OID 18602)
-- Name: services services_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.services
    ADD CONSTRAINT services_pkey PRIMARY KEY (id);


--
-- TOC entry 3156 (class 2606 OID 18899)
-- Name: taskdata taskdata_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.taskdata
    ADD CONSTRAINT taskdata_pkey PRIMARY KEY (id);


--
-- TOC entry 3154 (class 2606 OID 18886)
-- Name: tasklogs tasklogs_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.tasklogs
    ADD CONSTRAINT tasklogs_pkey PRIMARY KEY (id);


--
-- TOC entry 3152 (class 2606 OID 18865)
-- Name: tasks tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_pkey PRIMARY KEY (id);


--
-- TOC entry 3098 (class 2606 OID 18460)
-- Name: taskstatus taskstatus_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.taskstatus
    ADD CONSTRAINT taskstatus_pkey PRIMARY KEY (id);


--
-- TOC entry 3108 (class 2606 OID 18504)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 3100 (class 2606 OID 18471)
-- Name: visualizers visualizers_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.visualizers
    ADD CONSTRAINT visualizers_pkey PRIMARY KEY (id);


--
-- TOC entry 3150 (class 2606 OID 18849)
-- Name: workflow_annotations workflow_annotations_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.workflow_annotations
    ADD CONSTRAINT workflow_annotations_pkey PRIMARY KEY (id);


--
-- TOC entry 3140 (class 2606 OID 18757)
-- Name: workflowaccesses workflowaccesses_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.workflowaccesses
    ADD CONSTRAINT workflowaccesses_pkey PRIMARY KEY (id);


--
-- TOC entry 3119 (class 2606 OID 18586)
-- Name: workflows workflows_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.workflows
    ADD CONSTRAINT workflows_pkey PRIMARY KEY (id);


--
-- TOC entry 3138 (class 1259 OID 18749)
-- Name: ix_comments_timestamp; Type: INDEX; Schema: public; Owner: phenodoop
--

CREATE INDEX ix_comments_timestamp ON public.comments USING btree ("timestamp");


--
-- TOC entry 3115 (class 1259 OID 18575)
-- Name: ix_posts_timestamp; Type: INDEX; Schema: public; Owner: phenodoop
--

CREATE INDEX ix_posts_timestamp ON public.posts USING btree ("timestamp");


--
-- TOC entry 3088 (class 1259 OID 18430)
-- Name: ix_roles_default; Type: INDEX; Schema: public; Owner: phenodoop
--

CREATE INDEX ix_roles_default ON public.roles USING btree ("default");


--
-- TOC entry 3105 (class 1259 OID 18511)
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: phenodoop
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- TOC entry 3106 (class 1259 OID 18510)
-- Name: ix_users_username; Type: INDEX; Schema: public; Owner: phenodoop
--

CREATE UNIQUE INDEX ix_users_username ON public.users USING btree (username);


--
-- TOC entry 3178 (class 2606 OID 18739)
-- Name: comments comments_author_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_author_id_fkey FOREIGN KEY (author_id) REFERENCES public.users(id);


--
-- TOC entry 3179 (class 2606 OID 18744)
-- Name: comments comments_post_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_post_id_fkey FOREIGN KEY (post_id) REFERENCES public.posts(id);


--
-- TOC entry 3176 (class 2606 OID 18718)
-- Name: data_allocations data_allocations_data_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_allocations
    ADD CONSTRAINT data_allocations_data_id_fkey FOREIGN KEY (data_id) REFERENCES public.data(id);


--
-- TOC entry 3177 (class 2606 OID 18723)
-- Name: data_allocations data_allocations_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_allocations
    ADD CONSTRAINT data_allocations_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 3171 (class 2606 OID 18669)
-- Name: data_annotations data_annotations_data_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_annotations
    ADD CONSTRAINT data_annotations_data_id_fkey FOREIGN KEY (data_id) REFERENCES public.datasource_allocations(id);


--
-- TOC entry 3174 (class 2606 OID 18700)
-- Name: data_mimetypes data_mimetypes_data_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_mimetypes
    ADD CONSTRAINT data_mimetypes_data_id_fkey FOREIGN KEY (data_id) REFERENCES public.datasource_allocations(id);


--
-- TOC entry 3175 (class 2606 OID 18705)
-- Name: data_mimetypes data_mimetypes_mimetype_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_mimetypes
    ADD CONSTRAINT data_mimetypes_mimetype_id_fkey FOREIGN KEY (mimetype_id) REFERENCES public.mimetypes(id);


--
-- TOC entry 3170 (class 2606 OID 18653)
-- Name: data_permissions data_permissions_data_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_permissions
    ADD CONSTRAINT data_permissions_data_id_fkey FOREIGN KEY (data_id) REFERENCES public.datasource_allocations(id);


--
-- TOC entry 3169 (class 2606 OID 18648)
-- Name: data_permissions data_permissions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_permissions
    ADD CONSTRAINT data_permissions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 3161 (class 2606 OID 18539)
-- Name: data_properties data_properties_data_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_properties
    ADD CONSTRAINT data_properties_data_id_fkey FOREIGN KEY (data_id) REFERENCES public.data(id);


--
-- TOC entry 3172 (class 2606 OID 18682)
-- Name: data_visualizers data_visualizers_data_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_visualizers
    ADD CONSTRAINT data_visualizers_data_id_fkey FOREIGN KEY (data_id) REFERENCES public.datasource_allocations(id);


--
-- TOC entry 3173 (class 2606 OID 18687)
-- Name: data_visualizers data_visualizers_visualizer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_visualizers
    ADD CONSTRAINT data_visualizers_visualizer_id_fkey FOREIGN KEY (visualizer_id) REFERENCES public.visualizers(id);


--
-- TOC entry 3160 (class 2606 OID 18523)
-- Name: datasource_allocations datasource_allocations_datasource_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.datasource_allocations
    ADD CONSTRAINT datasource_allocations_datasource_id_fkey FOREIGN KEY (datasource_id) REFERENCES public.datasources(id);


--
-- TOC entry 3168 (class 2606 OID 18635)
-- Name: filter_history filter_history_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.filter_history
    ADD CONSTRAINT filter_history_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 3167 (class 2606 OID 18619)
-- Name: filters filters_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.filters
    ADD CONSTRAINT filters_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 3163 (class 2606 OID 18554)
-- Name: follows follows_followed_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.follows
    ADD CONSTRAINT follows_followed_id_fkey FOREIGN KEY (followed_id) REFERENCES public.users(id);


--
-- TOC entry 3162 (class 2606 OID 18549)
-- Name: follows follows_follower_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.follows
    ADD CONSTRAINT follows_follower_id_fkey FOREIGN KEY (follower_id) REFERENCES public.users(id);


--
-- TOC entry 3195 (class 2606 OID 18923)
-- Name: indata indata_data_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.indata
    ADD CONSTRAINT indata_data_id_fkey FOREIGN KEY (data_id) REFERENCES public.data(id);


--
-- TOC entry 3194 (class 2606 OID 18918)
-- Name: indata indata_task_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.indata
    ADD CONSTRAINT indata_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.tasks(id);


--
-- TOC entry 3182 (class 2606 OID 18779)
-- Name: params params_service_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.params
    ADD CONSTRAINT params_service_id_fkey FOREIGN KEY (service_id) REFERENCES public.services(id);


--
-- TOC entry 3164 (class 2606 OID 18570)
-- Name: posts posts_author_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_author_id_fkey FOREIGN KEY (author_id) REFERENCES public.users(id);


--
-- TOC entry 3183 (class 2606 OID 18795)
-- Name: returns returns_service_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.returns
    ADD CONSTRAINT returns_service_id_fkey FOREIGN KEY (service_id) REFERENCES public.services(id);


--
-- TOC entry 3187 (class 2606 OID 18834)
-- Name: runnables runnables_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.runnables
    ADD CONSTRAINT runnables_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 3186 (class 2606 OID 18829)
-- Name: runnables runnables_workflow_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.runnables
    ADD CONSTRAINT runnables_workflow_id_fkey FOREIGN KEY (workflow_id) REFERENCES public.workflows(id) ON DELETE CASCADE;


--
-- TOC entry 3184 (class 2606 OID 18808)
-- Name: serviceaccesses serviceaccesses_service_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.serviceaccesses
    ADD CONSTRAINT serviceaccesses_service_id_fkey FOREIGN KEY (service_id) REFERENCES public.services(id) ON DELETE CASCADE;


--
-- TOC entry 3185 (class 2606 OID 18813)
-- Name: serviceaccesses serviceaccesses_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.serviceaccesses
    ADD CONSTRAINT serviceaccesses_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 3166 (class 2606 OID 18603)
-- Name: services services_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.services
    ADD CONSTRAINT services_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 3193 (class 2606 OID 18905)
-- Name: taskdata taskdata_data_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.taskdata
    ADD CONSTRAINT taskdata_data_id_fkey FOREIGN KEY (data_id) REFERENCES public.data(id);


--
-- TOC entry 3192 (class 2606 OID 18900)
-- Name: taskdata taskdata_task_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.taskdata
    ADD CONSTRAINT taskdata_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.tasks(id);


--
-- TOC entry 3191 (class 2606 OID 18887)
-- Name: tasklogs tasklogs_task_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.tasklogs
    ADD CONSTRAINT tasklogs_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.tasks(id);


--
-- TOC entry 3189 (class 2606 OID 18866)
-- Name: tasks tasks_runnable_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_runnable_id_fkey FOREIGN KEY (runnable_id) REFERENCES public.runnables(id);


--
-- TOC entry 3190 (class 2606 OID 18871)
-- Name: tasks tasks_service_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_service_id_fkey FOREIGN KEY (service_id) REFERENCES public.services(id);


--
-- TOC entry 3159 (class 2606 OID 18505)
-- Name: users users_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id);


--
-- TOC entry 3188 (class 2606 OID 18850)
-- Name: workflow_annotations workflow_annotations_workflow_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.workflow_annotations
    ADD CONSTRAINT workflow_annotations_workflow_id_fkey FOREIGN KEY (workflow_id) REFERENCES public.workflows(id);


--
-- TOC entry 3181 (class 2606 OID 18763)
-- Name: workflowaccesses workflowaccesses_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.workflowaccesses
    ADD CONSTRAINT workflowaccesses_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 3180 (class 2606 OID 18758)
-- Name: workflowaccesses workflowaccesses_workflow_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.workflowaccesses
    ADD CONSTRAINT workflowaccesses_workflow_id_fkey FOREIGN KEY (workflow_id) REFERENCES public.workflows(id);


--
-- TOC entry 3165 (class 2606 OID 18587)
-- Name: workflows workflows_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.workflows
    ADD CONSTRAINT workflows_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


-- Completed on 2022-03-22 21:42:20 UTC

--
-- PostgreSQL database dump complete
--

