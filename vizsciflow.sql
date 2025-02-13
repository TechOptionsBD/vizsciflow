--
-- PostgreSQL database dump
--

-- Dumped from database version 13.18 (Debian 13.18-0+deb11u1)
-- Dumped by pg_dump version 13.18 (Debian 13.18-0+deb11u1)

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
-- Name: activities_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.activities_id_seq OWNED BY public.activities.id;


--
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
-- Name: activitylogs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.activitylogs_id_seq OWNED BY public.activitylogs.id;


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO phenodoop;

--
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
-- Name: comments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.comments_id_seq OWNED BY public.comments.id;


--
-- Name: data; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.data (
    id integer NOT NULL,
    value json
);


ALTER TABLE public.data OWNER TO phenodoop;

--
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
-- Name: data_allocations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.data_allocations_id_seq OWNED BY public.data_allocations.id;


--
-- Name: data_annotations; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.data_annotations (
    id integer NOT NULL,
    data_id integer,
    tag text NOT NULL
);


ALTER TABLE public.data_annotations OWNER TO phenodoop;

--
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
-- Name: data_annotations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.data_annotations_id_seq OWNED BY public.data_annotations.id;


--
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
-- Name: data_chunks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.data_chunks_id_seq OWNED BY public.data_chunks.id;


--
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
-- Name: data_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.data_id_seq OWNED BY public.data.id;


--
-- Name: data_mimetypes; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.data_mimetypes (
    id integer NOT NULL,
    data_id integer NOT NULL,
    mimetype_id integer NOT NULL
);


ALTER TABLE public.data_mimetypes OWNER TO phenodoop;

--
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
-- Name: data_mimetypes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.data_mimetypes_id_seq OWNED BY public.data_mimetypes.id;


--
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
-- Name: data_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.data_permissions_id_seq OWNED BY public.data_permissions.id;


--
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
-- Name: data_properties_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.data_properties_id_seq OWNED BY public.data_properties.id;


--
-- Name: data_visualizers; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.data_visualizers (
    id integer NOT NULL,
    data_id integer NOT NULL,
    visualizer_id integer NOT NULL
);


ALTER TABLE public.data_visualizers OWNER TO phenodoop;

--
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
-- Name: data_visualizers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.data_visualizers_id_seq OWNED BY public.data_visualizers.id;


--
-- Name: datasets; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.datasets (
    id integer NOT NULL,
    schema json NOT NULL
);


ALTER TABLE public.datasets OWNER TO phenodoop;

--
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
-- Name: datasets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.datasets_id_seq OWNED BY public.datasets.id;


--
-- Name: datasource_allocations; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.datasource_allocations (
    id integer NOT NULL,
    datasource_id integer,
    url text NOT NULL
);


ALTER TABLE public.datasource_allocations OWNER TO phenodoop;

--
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
-- Name: datasource_allocations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.datasource_allocations_id_seq OWNED BY public.datasource_allocations.id;


--
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
-- Name: datasources_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.datasources_id_seq OWNED BY public.datasources.id;


--
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
-- Name: dockercontainers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.dockercontainers_id_seq OWNED BY public.dockercontainers.id;


--
-- Name: dockerimages; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.dockerimages (
    id integer NOT NULL,
    user_id integer,
    name text
);


ALTER TABLE public.dockerimages OWNER TO phenodoop;

--
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
-- Name: dockerimages_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.dockerimages_id_seq OWNED BY public.dockerimages.id;


--
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
-- Name: filter_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.filter_history_id_seq OWNED BY public.filter_history.id;


--
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
-- Name: filters_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.filters_id_seq OWNED BY public.filters.id;


--
-- Name: follows; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.follows (
    follower_id integer NOT NULL,
    followed_id integer NOT NULL,
    "timestamp" timestamp without time zone
);


ALTER TABLE public.follows OWNER TO phenodoop;

--
-- Name: indata; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.indata (
    id integer NOT NULL,
    task_id integer,
    data_id integer
);


ALTER TABLE public.indata OWNER TO phenodoop;

--
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
-- Name: indata_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.indata_id_seq OWNED BY public.indata.id;


--
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
-- Name: mimetypes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.mimetypes_id_seq OWNED BY public.mimetypes.id;


--
-- Name: params; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.params (
    id integer NOT NULL,
    service_id integer,
    value json NOT NULL
);


ALTER TABLE public.params OWNER TO phenodoop;

--
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
-- Name: params_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.params_id_seq OWNED BY public.params.id;


--
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
-- Name: posts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.posts_id_seq OWNED BY public.posts.id;


--
-- Name: returns; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.returns (
    id integer NOT NULL,
    service_id integer,
    value json NOT NULL
);


ALTER TABLE public.returns OWNER TO phenodoop;

--
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
-- Name: returns_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.returns_id_seq OWNED BY public.returns.id;


--
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
-- Name: roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.roles_id_seq OWNED BY public.roles.id;


--
-- Name: runnableargs; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.runnableargs (
    id integer NOT NULL,
    runnable_id integer,
    value json NOT NULL
);


ALTER TABLE public.runnableargs OWNER TO phenodoop;

--
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
-- Name: runnableargs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.runnableargs_id_seq OWNED BY public.runnableargs.id;


--
-- Name: runnablereturns; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.runnablereturns (
    id integer NOT NULL,
    runnable_id integer,
    value json NOT NULL
);


ALTER TABLE public.runnablereturns OWNER TO phenodoop;

--
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
-- Name: runnablereturns_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.runnablereturns_id_seq OWNED BY public.runnablereturns.id;


--
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
-- Name: runnables_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.runnables_id_seq OWNED BY public.runnables.id;


--
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
-- Name: serviceaccesses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.serviceaccesses_id_seq OWNED BY public.serviceaccesses.id;


--
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
-- Name: services_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.services_id_seq OWNED BY public.services.id;


--
-- Name: taskdata; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.taskdata (
    id integer NOT NULL,
    task_id integer,
    data_id integer
);


ALTER TABLE public.taskdata OWNER TO phenodoop;

--
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
-- Name: taskdata_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.taskdata_id_seq OWNED BY public.taskdata.id;


--
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
-- Name: tasklogs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.tasklogs_id_seq OWNED BY public.tasklogs.id;


--
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
-- Name: tasks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.tasks_id_seq OWNED BY public.tasks.id;


--
-- Name: taskstatus; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.taskstatus (
    id integer NOT NULL,
    name character varying(30)
);


ALTER TABLE public.taskstatus OWNER TO phenodoop;

--
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
-- Name: taskstatus_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.taskstatus_id_seq OWNED BY public.taskstatus.id;


--
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
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: visualizers; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.visualizers (
    id integer NOT NULL,
    name text NOT NULL,
    "desc" text
);


ALTER TABLE public.visualizers OWNER TO phenodoop;

--
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
-- Name: visualizers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.visualizers_id_seq OWNED BY public.visualizers.id;


--
-- Name: workflow_annotations; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.workflow_annotations (
    id integer NOT NULL,
    workflow_id integer,
    tag text NOT NULL
);


ALTER TABLE public.workflow_annotations OWNER TO phenodoop;

--
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
-- Name: workflow_annotations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.workflow_annotations_id_seq OWNED BY public.workflow_annotations.id;


--
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
-- Name: workflowaccesses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.workflowaccesses_id_seq OWNED BY public.workflowaccesses.id;


--
-- Name: workflowparams; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.workflowparams (
    id integer NOT NULL,
    workflow_id integer,
    value json NOT NULL
);


ALTER TABLE public.workflowparams OWNER TO phenodoop;

--
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
-- Name: workflowparams_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.workflowparams_id_seq OWNED BY public.workflowparams.id;


--
-- Name: workflowreturns; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.workflowreturns (
    id integer NOT NULL,
    workflow_id integer,
    value json NOT NULL
);


ALTER TABLE public.workflowreturns OWNER TO phenodoop;

--
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
-- Name: workflowreturns_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.workflowreturns_id_seq OWNED BY public.workflowreturns.id;


--
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
-- Name: workflows_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.workflows_id_seq OWNED BY public.workflows.id;


--
-- Name: activities id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.activities ALTER COLUMN id SET DEFAULT nextval('public.activities_id_seq'::regclass);


--
-- Name: activitylogs id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.activitylogs ALTER COLUMN id SET DEFAULT nextval('public.activitylogs_id_seq'::regclass);


--
-- Name: comments id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.comments ALTER COLUMN id SET DEFAULT nextval('public.comments_id_seq'::regclass);


--
-- Name: data id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data ALTER COLUMN id SET DEFAULT nextval('public.data_id_seq'::regclass);


--
-- Name: data_allocations id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_allocations ALTER COLUMN id SET DEFAULT nextval('public.data_allocations_id_seq'::regclass);


--
-- Name: data_annotations id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_annotations ALTER COLUMN id SET DEFAULT nextval('public.data_annotations_id_seq'::regclass);


--
-- Name: data_chunks id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_chunks ALTER COLUMN id SET DEFAULT nextval('public.data_chunks_id_seq'::regclass);


--
-- Name: data_mimetypes id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_mimetypes ALTER COLUMN id SET DEFAULT nextval('public.data_mimetypes_id_seq'::regclass);


--
-- Name: data_permissions id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_permissions ALTER COLUMN id SET DEFAULT nextval('public.data_permissions_id_seq'::regclass);


--
-- Name: data_properties id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_properties ALTER COLUMN id SET DEFAULT nextval('public.data_properties_id_seq'::regclass);


--
-- Name: data_visualizers id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_visualizers ALTER COLUMN id SET DEFAULT nextval('public.data_visualizers_id_seq'::regclass);


--
-- Name: datasets id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.datasets ALTER COLUMN id SET DEFAULT nextval('public.datasets_id_seq'::regclass);


--
-- Name: datasource_allocations id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.datasource_allocations ALTER COLUMN id SET DEFAULT nextval('public.datasource_allocations_id_seq'::regclass);


--
-- Name: datasources id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.datasources ALTER COLUMN id SET DEFAULT nextval('public.datasources_id_seq'::regclass);


--
-- Name: dockercontainers id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.dockercontainers ALTER COLUMN id SET DEFAULT nextval('public.dockercontainers_id_seq'::regclass);


--
-- Name: dockerimages id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.dockerimages ALTER COLUMN id SET DEFAULT nextval('public.dockerimages_id_seq'::regclass);


--
-- Name: filter_history id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.filter_history ALTER COLUMN id SET DEFAULT nextval('public.filter_history_id_seq'::regclass);


--
-- Name: filters id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.filters ALTER COLUMN id SET DEFAULT nextval('public.filters_id_seq'::regclass);


--
-- Name: indata id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.indata ALTER COLUMN id SET DEFAULT nextval('public.indata_id_seq'::regclass);


--
-- Name: mimetypes id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.mimetypes ALTER COLUMN id SET DEFAULT nextval('public.mimetypes_id_seq'::regclass);


--
-- Name: params id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.params ALTER COLUMN id SET DEFAULT nextval('public.params_id_seq'::regclass);


--
-- Name: posts id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.posts ALTER COLUMN id SET DEFAULT nextval('public.posts_id_seq'::regclass);


--
-- Name: returns id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.returns ALTER COLUMN id SET DEFAULT nextval('public.returns_id_seq'::regclass);


--
-- Name: roles id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.roles ALTER COLUMN id SET DEFAULT nextval('public.roles_id_seq'::regclass);


--
-- Name: runnableargs id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.runnableargs ALTER COLUMN id SET DEFAULT nextval('public.runnableargs_id_seq'::regclass);


--
-- Name: runnablereturns id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.runnablereturns ALTER COLUMN id SET DEFAULT nextval('public.runnablereturns_id_seq'::regclass);


--
-- Name: runnables id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.runnables ALTER COLUMN id SET DEFAULT nextval('public.runnables_id_seq'::regclass);


--
-- Name: serviceaccesses id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.serviceaccesses ALTER COLUMN id SET DEFAULT nextval('public.serviceaccesses_id_seq'::regclass);


--
-- Name: services id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.services ALTER COLUMN id SET DEFAULT nextval('public.services_id_seq'::regclass);


--
-- Name: taskdata id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.taskdata ALTER COLUMN id SET DEFAULT nextval('public.taskdata_id_seq'::regclass);


--
-- Name: tasklogs id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.tasklogs ALTER COLUMN id SET DEFAULT nextval('public.tasklogs_id_seq'::regclass);


--
-- Name: tasks id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.tasks ALTER COLUMN id SET DEFAULT nextval('public.tasks_id_seq'::regclass);


--
-- Name: taskstatus id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.taskstatus ALTER COLUMN id SET DEFAULT nextval('public.taskstatus_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: visualizers id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.visualizers ALTER COLUMN id SET DEFAULT nextval('public.visualizers_id_seq'::regclass);


--
-- Name: workflow_annotations id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.workflow_annotations ALTER COLUMN id SET DEFAULT nextval('public.workflow_annotations_id_seq'::regclass);


--
-- Name: workflowaccesses id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.workflowaccesses ALTER COLUMN id SET DEFAULT nextval('public.workflowaccesses_id_seq'::regclass);


--
-- Name: workflowparams id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.workflowparams ALTER COLUMN id SET DEFAULT nextval('public.workflowparams_id_seq'::regclass);


--
-- Name: workflowreturns id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.workflowreturns ALTER COLUMN id SET DEFAULT nextval('public.workflowreturns_id_seq'::regclass);


--
-- Name: workflows id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.workflows ALTER COLUMN id SET DEFAULT nextval('public.workflows_id_seq'::regclass);


--
-- Data for Name: activities; Type: TABLE DATA; Schema: public; Owner: phenodoop
--

COPY public.activities (id, user_id, type, status, created_on, modified_on) FROM stdin;
\.


--
-- Data for Name: activitylogs; Type: TABLE DATA; Schema: public; Owner: phenodoop
--

COPY public.activitylogs (id, activity_id, "time", type, log) FROM stdin;
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: phenodoop
--

COPY public.alembic_version (version_num) FROM stdin;
\.


--
-- Data for Name: comments; Type: TABLE DATA; Schema: public; Owner: phenodoop
--

COPY public.comments (id, body, body_html, "timestamp", disabled, author_id, post_id) FROM stdin;
\.


--
-- Data for Name: data; Type: TABLE DATA; Schema: public; Owner: phenodoop
--

COPY public.data (id, value) FROM stdin;
1	{"name": "data", "value": "/public/MiSeq_SOP/F3D3_S191_L001_R1_001.fastq", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 02:21:53.153096", "modified": "2025-01-28 02:21:53.153109"}
2	{"name": "data", "value": "/public/MiSeq_SOP/F3D3_S191_L001_R1_001.fastq", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 03:15:12.703772", "modified": "2025-01-28 03:15:12.703785"}
3	{"name": "data", "value": "/public/MiSeq_SOP/F3D3_S191_L001_R1_001.fastq", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 03:35:43.026782", "modified": "2025-01-28 03:35:43.026799"}
4	{"name": "data", "value": "/public/MiSeq_SOP/F3D3_S191_L001_R1_001.fastq", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 03:37:05.519438", "modified": "2025-01-28 03:37:05.519451"}
5	{"value": "/users/testuser/temp/869ebd91-fbd0-4a47-a229-cde144bdfb34/e786148b-a489-4e12-9d5c-6f14a7172c56/c208f319-9368-4c37-aeae-27ac3a3c4cff.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 03:37:18.001264", "modified": "2025-01-28 03:37:18.001274"}
6	{"name": "data", "value": "/public/bioml/images", "type": "1", "datatype": "<class 'str'>", "created": "2025-01-28 03:37:18.127967", "modified": "2025-01-28 03:37:18.127982"}
7	{"name": "data", "value": "/public/bioml/images", "type": "1", "datatype": "<class 'str'>", "created": "2025-01-28 04:06:57.787209", "modified": "2025-01-28 04:06:57.787220"}
8	{"value": "/users/testuser/temp/48d74d14-8c51-45c2-815d-355b3bf2d5fc/be6ec724-854a-4b8a-8dcb-8141dcaf58a7/06f98a4a-8397-4208-8d47-92d7089b2d56.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 04:11:44.157532", "modified": "2025-01-28 04:11:44.157550"}
9	{"name": "data", "value": "/public/MiSeq_SOP/F3D3_S191_L001_R1_001.fastq", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 04:36:04.912754", "modified": "2025-01-28 04:36:04.912765"}
10	{"value": "/users/testuser/temp/14181ab4-f8da-4a0d-9e41-8bf3a4fbbedf/128c979c-d727-449e-9090-df50def28ac9/270e528a-5892-4d26-86e3-62fb37e47b04.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 04:37:58.201568", "modified": "2025-01-28 04:37:58.201582"}
11	{"name": "data", "value": "/public/bioml/images", "type": "1", "datatype": "<class 'str'>", "created": "2025-01-28 04:37:58.292369", "modified": "2025-01-28 04:37:58.292378"}
12	{"name": "data", "value": "/public/MiSeq_SOP/F3D3_S191_L001_R1_001.fastq", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 04:38:14.230083", "modified": "2025-01-28 04:38:14.230097"}
13	{"value": "/users/testuser/temp/adbfb43a-47a4-413c-a148-e7ddbdda1e67/d090b945-809e-4711-9d73-23d8c6c0a9c4/bf591e6d-e2f2-407e-98a5-36937e658e17.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 04:38:14.994259", "modified": "2025-01-28 04:38:14.994270"}
14	{"name": "data", "value": "/public/bioml/images", "type": "1", "datatype": "<class 'str'>", "created": "2025-01-28 04:38:15.089630", "modified": "2025-01-28 04:38:15.089679"}
15	{"value": "/users/testuser/temp/adbfb43a-47a4-413c-a148-e7ddbdda1e67/d090b945-809e-4711-9d73-23d8c6c0a9c4/36a5aed9-a20e-449a-be05-833723ed35d5.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 04:38:16.668250", "modified": "2025-01-28 04:38:16.668261"}
16	{"name": "data", "value": "/public/MiSeq_SOP/F3D3_S191_L001_R1_001.fastq", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 07:35:57.089929", "modified": "2025-01-28 07:35:57.089943"}
17	{"value": "/users/testuser/temp/7708cffc-bea7-4965-ab71-635a15e08880/6754b7df-d9b2-4e05-ae0c-c04a6e71e50c/ead3e298-11f0-415e-8273-9ab6b45315d8.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 07:35:57.843708", "modified": "2025-01-28 07:35:57.843719"}
18	{"name": "data", "value": "/public/bioml/images", "type": "1", "datatype": "<class 'str'>", "created": "2025-01-28 07:35:57.935348", "modified": "2025-01-28 07:35:57.935357"}
19	{"value": "/users/testuser/temp/7708cffc-bea7-4965-ab71-635a15e08880/6754b7df-d9b2-4e05-ae0c-c04a6e71e50c/0a6beb75-bc63-4141-96e1-bbda2231a9f5.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 07:35:59.655235", "modified": "2025-01-28 07:35:59.655246"}
20	{"name": "data", "value": "/public/MiSeq_SOP/F3D3_S191_L001_R1_001.fastq", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 07:36:48.375941", "modified": "2025-01-28 07:36:48.375956"}
21	{"value": "/users/testuser/temp/3bee3bb2-b9d6-4fd9-9950-e8902c4a8afd/86780dd0-9515-4d36-9de4-5f9081d3cc89/6a7f0574-97ef-42ca-911f-1250dae7553b.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 07:36:49.102622", "modified": "2025-01-28 07:36:49.102634"}
22	{"name": "data", "value": "/public/bioml/images", "type": "1", "datatype": "<class 'str'>", "created": "2025-01-28 07:36:49.188580", "modified": "2025-01-28 07:36:49.188593"}
23	{"value": "/users/testuser/temp/3bee3bb2-b9d6-4fd9-9950-e8902c4a8afd/86780dd0-9515-4d36-9de4-5f9081d3cc89/6baf8109-d08f-4d49-af0a-6ff94edbf738.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 07:36:50.791577", "modified": "2025-01-28 07:36:50.791590"}
24	{"name": "data", "value": "/public/MiSeq_SOP/F3D3_S191_L001_R1_001.fastq", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 07:38:13.848771", "modified": "2025-01-28 07:38:13.848783"}
25	{"value": "/users/testuser/temp/9fd62dc8-b72a-470c-b7a1-3d92c7807839/1924ec54-80ee-4b74-b064-8cf929d4c925/40aeaf25-6a70-4e8c-a979-040e3dd366c4.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 07:38:14.814683", "modified": "2025-01-28 07:38:14.814699"}
26	{"name": "data", "value": "/public/bioml/images", "type": "1", "datatype": "<class 'str'>", "created": "2025-01-28 07:38:25.502596", "modified": "2025-01-28 07:38:25.502610"}
27	{"value": "/users/testuser/temp/9fd62dc8-b72a-470c-b7a1-3d92c7807839/1924ec54-80ee-4b74-b064-8cf929d4c925/5c28fbab-b5cf-4eba-ac16-137f4e5f4e84.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 07:38:27.375827", "modified": "2025-01-28 07:38:27.375840"}
28	{"name": "data", "value": "/public/MiSeq_SOP/F3D3_S191_L001_R1_001.fastq", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 07:39:48.643997", "modified": "2025-01-28 07:39:48.644021"}
29	{"value": "/users/testuser/temp/5e4e93a3-50d6-48ab-8302-25a6bf1da648/b73d5314-6c41-4120-9621-b07a99efc978/bb5fc47c-d0d1-497d-a4e7-3f71c8c1776c.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 07:39:49.401433", "modified": "2025-01-28 07:39:49.401445"}
30	{"name": "data", "value": "/public/bioml/images", "type": "1", "datatype": "<class 'str'>", "created": "2025-01-28 07:40:23.822569", "modified": "2025-01-28 07:40:23.822582"}
31	{"value": "/users/testuser/temp/5e4e93a3-50d6-48ab-8302-25a6bf1da648/b73d5314-6c41-4120-9621-b07a99efc978/3f75dc36-551d-46e4-8cb9-4ca90f44950d.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 07:40:25.400827", "modified": "2025-01-28 07:40:25.400843"}
32	{"name": "data", "value": "/public/MiSeq_SOP/F3D3_S191_L001_R1_001.fastq", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 07:40:46.895146", "modified": "2025-01-28 07:40:46.895158"}
34	{"name": "data", "value": "/public/bioml/images", "type": "1", "datatype": "<class 'str'>", "created": "2025-01-28 07:40:56.355242", "modified": "2025-01-28 07:40:56.355254"}
38	{"name": "data", "value": "/public/bioml/images", "type": "1", "datatype": "<class 'str'>", "created": "2025-01-28 07:43:19.722702", "modified": "2025-01-28 07:43:19.722713"}
43	{"value": "/users/testuser/temp/5c04ccea-09e5-4935-945f-14fce6a987c8/03dc9786-d629-40cb-bd47-6cdb2b366603/0d4048ff-ec2e-4097-92bb-73bb5ba1a7b9.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 07:45:59.562856", "modified": "2025-01-28 07:45:59.562870"}
47	{"value": "/users/testuser/temp/f821a17e-8f77-468e-96ec-baa9bcfae6d9/b538673c-88d7-41a9-805c-e4f1172c101e/76928617-2856-4b53-940a-83ad062406e5.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 07:47:30.974866", "modified": "2025-01-28 07:47:30.974877"}
50	{"name": "data", "value": "/public/MiSeq_SOP/F3D3_S191_L001_R1_001.fastq", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 07:48:16.902680", "modified": "2025-01-28 07:48:16.902693"}
33	{"value": "/users/testuser/temp/ab5875c1-772a-4994-9573-d04cd1437f51/fc2820ab-9b2b-4ee6-b1e6-3b888530e683/ef420828-87b8-49f3-9408-acbee67e42b2.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 07:40:47.678932", "modified": "2025-01-28 07:40:47.678942"}
36	{"name": "data", "value": "/public/MiSeq_SOP/F3D3_S191_L001_R1_001.fastq", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 07:42:49.010543", "modified": "2025-01-28 07:42:49.010556"}
35	{"value": "/users/testuser/temp/ab5875c1-772a-4994-9573-d04cd1437f51/fc2820ab-9b2b-4ee6-b1e6-3b888530e683/1d2c90b8-b58c-429f-8d26-3bbe54b68a15.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 07:40:58.009954", "modified": "2025-01-28 07:40:58.009971"}
39	{"value": "/users/testuser/temp/c110e017-d05a-42c0-9a80-9386f1bf604d/1a027143-1129-4916-ad31-610aa9130a40/a038b683-cb2d-40dd-af0b-e73d02fe42d9.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 07:43:21.126119", "modified": "2025-01-28 07:43:21.126132"}
41	{"value": "/users/testuser/temp/5c04ccea-09e5-4935-945f-14fce6a987c8/03dc9786-d629-40cb-bd47-6cdb2b366603/f35be643-0619-4837-9402-540c74e45aa9.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 07:45:49.112882", "modified": "2025-01-28 07:45:49.112900"}
37	{"value": "/users/testuser/temp/c110e017-d05a-42c0-9a80-9386f1bf604d/1a027143-1129-4916-ad31-610aa9130a40/2c200cee-af90-4f65-b666-0ed835836ed1.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 07:42:49.626441", "modified": "2025-01-28 07:42:49.626452"}
40	{"name": "data", "value": "/public/MiSeq_SOP/F3D3_S191_L001_R1_001.fastq", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 07:45:47.881198", "modified": "2025-01-28 07:45:47.881225"}
45	{"value": "/users/testuser/temp/f821a17e-8f77-468e-96ec-baa9bcfae6d9/b538673c-88d7-41a9-805c-e4f1172c101e/d0ac6a51-22c2-4a0b-bdfe-2555d5dfd731.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 07:47:27.360321", "modified": "2025-01-28 07:47:27.360331"}
48	{"name": "biodata", "value": "/users/testuser/temp/f821a17e-8f77-468e-96ec-baa9bcfae6d9/b538673c-88d7-41a9-805c-e4f1172c101e/d0ac6a51-22c2-4a0b-bdfe-2555d5dfd731.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 07:47:42.906233", "modified": "2025-01-28 07:47:42.906248"}
42	{"name": "data", "value": "/public/bioml/images", "type": "1", "datatype": "<class 'str'>", "created": "2025-01-28 07:45:56.764074", "modified": "2025-01-28 07:45:56.764088"}
44	{"name": "data", "value": "/public/MiSeq_SOP/F3D3_S191_L001_R1_001.fastq", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 07:47:26.739136", "modified": "2025-01-28 07:47:26.739147"}
46	{"name": "data", "value": "/public/bioml/images", "type": "1", "datatype": "<class 'str'>", "created": "2025-01-28 07:47:29.460169", "modified": "2025-01-28 07:47:29.460182"}
49	{"name": "imgdata", "value": "/users/testuser/temp/f821a17e-8f77-468e-96ec-baa9bcfae6d9/b538673c-88d7-41a9-805c-e4f1172c101e/76928617-2856-4b53-940a-83ad062406e5.csv", "type": "1", "datatype": "<class 'str'>", "created": "2025-01-28 07:47:42.937143", "modified": "2025-01-28 07:47:42.937156"}
51	{"value": "/users/testuser/temp/1a21197f-e506-460c-abde-c0d5763ab0c8/6602c13d-4b6a-4272-94e1-bda65d7af5bf/1514c4c3-4320-4e70-bf90-e0e0a197c632.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 07:48:17.542134", "modified": "2025-01-28 07:48:17.542146"}
52	{"name": "data", "value": "/public/bioml/images", "type": "1", "datatype": "<class 'str'>", "created": "2025-01-28 07:48:17.629284", "modified": "2025-01-28 07:48:17.629294"}
53	{"value": "/users/testuser/temp/1a21197f-e506-460c-abde-c0d5763ab0c8/6602c13d-4b6a-4272-94e1-bda65d7af5bf/9a9f9ba8-3dc1-4a4e-9b67-08d94a9640ec.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 07:48:19.129251", "modified": "2025-01-28 07:48:19.129263"}
54	{"name": "biodata", "value": "/users/testuser/temp/1a21197f-e506-460c-abde-c0d5763ab0c8/6602c13d-4b6a-4272-94e1-bda65d7af5bf/1514c4c3-4320-4e70-bf90-e0e0a197c632.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 07:48:19.213646", "modified": "2025-01-28 07:48:19.213660"}
55	{"name": "imgdata", "value": "/users/testuser/temp/1a21197f-e506-460c-abde-c0d5763ab0c8/6602c13d-4b6a-4272-94e1-bda65d7af5bf/9a9f9ba8-3dc1-4a4e-9b67-08d94a9640ec.csv", "type": "1", "datatype": "<class 'str'>", "created": "2025-01-28 07:48:19.232142", "modified": "2025-01-28 07:48:19.232156"}
56	{"name": "data", "value": "/public/MiSeq_SOP/F3D3_S191_L001_R1_001.fastq", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 08:00:53.776834", "modified": "2025-01-28 08:00:53.776845"}
57	{"value": "/users/testuser/temp/60afb348-f08c-49e1-b546-15991fd9dea8/df5913d2-cae2-4c76-a9c9-11ad13a9a7cd/875e9cc1-d15a-4a99-bdac-468a82511f05.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 08:00:54.603295", "modified": "2025-01-28 08:00:54.603311"}
58	{"name": "data", "value": "/public/bioml/images", "type": "1", "datatype": "<class 'str'>", "created": "2025-01-28 08:00:54.720640", "modified": "2025-01-28 08:00:54.720656"}
59	{"value": "/users/testuser/temp/60afb348-f08c-49e1-b546-15991fd9dea8/df5913d2-cae2-4c76-a9c9-11ad13a9a7cd/b6e1626b-a5d2-4237-bbf3-838ac9afe49f.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 08:00:56.327041", "modified": "2025-01-28 08:00:56.327054"}
60	{"name": "biodata", "value": "/users/testuser/temp/60afb348-f08c-49e1-b546-15991fd9dea8/df5913d2-cae2-4c76-a9c9-11ad13a9a7cd/875e9cc1-d15a-4a99-bdac-468a82511f05.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 08:00:56.420742", "modified": "2025-01-28 08:00:56.420754"}
61	{"name": "imgdata", "value": "/users/testuser/temp/60afb348-f08c-49e1-b546-15991fd9dea8/df5913d2-cae2-4c76-a9c9-11ad13a9a7cd/b6e1626b-a5d2-4237-bbf3-838ac9afe49f.csv", "type": "1", "datatype": "<class 'str'>", "created": "2025-01-28 08:00:56.435012", "modified": "2025-01-28 08:00:56.435024"}
62	{"name": "data", "value": "/public/MiSeq_SOP/F3D3_S191_L001_R1_001.fastq", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 09:21:33.260676", "modified": "2025-01-28 09:21:33.260687"}
63	{"value": "/users/testuser/temp/4ee3a53f-e50e-4716-9916-a2978fde9798/7eb99b49-fcdf-4645-b919-320d60a73ccc/442e8bc7-d19f-4183-81c3-8fca789e3ba0.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 09:21:34.121920", "modified": "2025-01-28 09:21:34.121931"}
64	{"name": "data", "value": "/public/bioml/images", "type": "1", "datatype": "<class 'str'>", "created": "2025-01-28 09:21:34.225237", "modified": "2025-01-28 09:21:34.225249"}
65	{"value": "/users/testuser/temp/4ee3a53f-e50e-4716-9916-a2978fde9798/7eb99b49-fcdf-4645-b919-320d60a73ccc/78cf981f-8021-48be-aafc-0feecd136b13.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 09:21:35.945251", "modified": "2025-01-28 09:21:35.945271"}
66	{"name": "biodata", "value": "/users/testuser/temp/4ee3a53f-e50e-4716-9916-a2978fde9798/7eb99b49-fcdf-4645-b919-320d60a73ccc/442e8bc7-d19f-4183-81c3-8fca789e3ba0.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 09:21:36.031112", "modified": "2025-01-28 09:21:36.031124"}
67	{"name": "imgdata", "value": "/users/testuser/temp/4ee3a53f-e50e-4716-9916-a2978fde9798/7eb99b49-fcdf-4645-b919-320d60a73ccc/78cf981f-8021-48be-aafc-0feecd136b13.csv", "type": "1", "datatype": "<class 'str'>", "created": "2025-01-28 09:21:36.044987", "modified": "2025-01-28 09:21:36.045001"}
68	{"name": "data", "value": "/public/MiSeq_SOP/F3D3_S191_L001_R1_001.fastq", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 09:46:16.763428", "modified": "2025-01-28 09:46:16.763441"}
69	{"value": "/users/testuser/temp/08c03c73-5120-46c7-ae31-ea5f80f28d1e/9a3d767a-6792-4e55-bda0-6752ec941809/00206e2f-7e4c-43dc-be13-4e641d8ee2e6.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 09:46:17.597742", "modified": "2025-01-28 09:46:17.597755"}
70	{"name": "data", "value": "/public/bioml/images", "type": "1", "datatype": "<class 'str'>", "created": "2025-01-28 09:46:17.690517", "modified": "2025-01-28 09:46:17.690526"}
71	{"value": "/users/testuser/temp/08c03c73-5120-46c7-ae31-ea5f80f28d1e/9a3d767a-6792-4e55-bda0-6752ec941809/00996d7c-fadb-4522-b9f9-df488058cbd6.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 09:46:19.609626", "modified": "2025-01-28 09:46:19.609640"}
72	{"name": "biodata", "value": "/users/testuser/temp/08c03c73-5120-46c7-ae31-ea5f80f28d1e/9a3d767a-6792-4e55-bda0-6752ec941809/00206e2f-7e4c-43dc-be13-4e641d8ee2e6.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 09:46:19.697573", "modified": "2025-01-28 09:46:19.697585"}
73	{"name": "imgdata", "value": "/users/testuser/temp/08c03c73-5120-46c7-ae31-ea5f80f28d1e/9a3d767a-6792-4e55-bda0-6752ec941809/00996d7c-fadb-4522-b9f9-df488058cbd6.csv", "type": "1", "datatype": "<class 'str'>", "created": "2025-01-28 09:46:19.713507", "modified": "2025-01-28 09:46:19.713521"}
74	{"name": "data", "value": "/public/MiSeq_SOP/F3D3_S191_L001_R1_001.fastq", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 09:51:47.457877", "modified": "2025-01-28 09:51:47.457887"}
75	{"value": "/users/testuser/temp/5253e95f-c9ca-4fe5-8b6e-7b4c9acd9e98/0aaed350-e340-45f3-adf8-fcb03587607d/32b660d9-7685-481b-a8a2-28a250e5eac6.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 09:51:48.186932", "modified": "2025-01-28 09:51:48.186943"}
76	{"name": "data", "value": "/public/bioml/images", "type": "1", "datatype": "<class 'str'>", "created": "2025-01-28 09:51:48.271471", "modified": "2025-01-28 09:51:48.271480"}
77	{"value": "/users/testuser/temp/5253e95f-c9ca-4fe5-8b6e-7b4c9acd9e98/0aaed350-e340-45f3-adf8-fcb03587607d/572905e2-205a-4494-b669-def394a8aff1.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 09:51:49.862031", "modified": "2025-01-28 09:51:49.862043"}
78	{"name": "biodata", "value": "/users/testuser/temp/5253e95f-c9ca-4fe5-8b6e-7b4c9acd9e98/0aaed350-e340-45f3-adf8-fcb03587607d/32b660d9-7685-481b-a8a2-28a250e5eac6.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 09:51:49.945213", "modified": "2025-01-28 09:51:49.945225"}
79	{"name": "imgdata", "value": "/users/testuser/temp/5253e95f-c9ca-4fe5-8b6e-7b4c9acd9e98/0aaed350-e340-45f3-adf8-fcb03587607d/572905e2-205a-4494-b669-def394a8aff1.csv", "type": "1", "datatype": "<class 'str'>", "created": "2025-01-28 09:51:49.961888", "modified": "2025-01-28 09:51:49.961899"}
80	{"name": "data", "value": "/public/MiSeq_SOP/F3D3_S191_L001_R1_001.fastq", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 10:08:42.340431", "modified": "2025-01-28 10:08:42.340445"}
81	{"value": "/users/testuser/temp/34c8c9a0-1b63-452a-9072-96f50430c98d/b11c4542-2302-46c9-baf3-c895eb7b7042/e0853ecc-3f36-439c-b1f6-f4e8ecbfc279.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 10:08:43.124642", "modified": "2025-01-28 10:08:43.124652"}
82	{"name": "data", "value": "/public/bioml/images", "type": "1", "datatype": "<class 'str'>", "created": "2025-01-28 10:08:43.214341", "modified": "2025-01-28 10:08:43.214352"}
83	{"value": "/users/testuser/temp/34c8c9a0-1b63-452a-9072-96f50430c98d/b11c4542-2302-46c9-baf3-c895eb7b7042/1a1b5b43-7087-4ada-b091-76a51cb5ade1.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 10:08:44.772904", "modified": "2025-01-28 10:08:44.772915"}
84	{"name": "biodata", "value": "/users/testuser/temp/34c8c9a0-1b63-452a-9072-96f50430c98d/b11c4542-2302-46c9-baf3-c895eb7b7042/e0853ecc-3f36-439c-b1f6-f4e8ecbfc279.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 10:08:44.855978", "modified": "2025-01-28 10:08:44.855990"}
85	{"name": "imgdata", "value": "/users/testuser/temp/34c8c9a0-1b63-452a-9072-96f50430c98d/b11c4542-2302-46c9-baf3-c895eb7b7042/1a1b5b43-7087-4ada-b091-76a51cb5ade1.csv", "type": "1", "datatype": "<class 'str'>", "created": "2025-01-28 10:08:44.871823", "modified": "2025-01-28 10:08:44.871836"}
86	{"name": "data", "value": "/public/MiSeq_SOP/F3D3_S191_L001_R1_001.fastq", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 10:09:34.242253", "modified": "2025-01-28 10:09:34.242267"}
87	{"value": "/users/testuser/temp/46f4f0c0-55c5-4245-997e-90af5827c57e/6a260ad4-4493-4218-8520-f270113298ae/68676607-3349-46b5-9662-1be4fb3f3f5e.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 10:09:34.980418", "modified": "2025-01-28 10:09:34.980430"}
88	{"name": "data", "value": "/public/bioml/images", "type": "1", "datatype": "<class 'str'>", "created": "2025-01-28 10:09:35.069582", "modified": "2025-01-28 10:09:35.069595"}
89	{"value": "/users/testuser/temp/46f4f0c0-55c5-4245-997e-90af5827c57e/6a260ad4-4493-4218-8520-f270113298ae/9f619976-342d-4ddb-b4f6-978eb52ce086.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 10:09:36.614780", "modified": "2025-01-28 10:09:36.614798"}
90	{"name": "biodata", "value": "/users/testuser/temp/46f4f0c0-55c5-4245-997e-90af5827c57e/6a260ad4-4493-4218-8520-f270113298ae/68676607-3349-46b5-9662-1be4fb3f3f5e.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 10:09:36.710993", "modified": "2025-01-28 10:09:36.711005"}
91	{"name": "imgdata", "value": "/users/testuser/temp/46f4f0c0-55c5-4245-997e-90af5827c57e/6a260ad4-4493-4218-8520-f270113298ae/9f619976-342d-4ddb-b4f6-978eb52ce086.csv", "type": "1", "datatype": "<class 'str'>", "created": "2025-01-28 10:09:36.732516", "modified": "2025-01-28 10:09:36.732528"}
92	{"name": "data", "value": "/public/MiSeq_SOP/F3D3_S191_L001_R1_001.fastq", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 10:12:50.922675", "modified": "2025-01-28 10:12:50.922687"}
93	{"value": "/users/testuser/temp/67189135-a7f7-42ae-9388-b362e05484cc/b45163f9-173b-4b49-80d1-a12efcc62592/944c20b3-f715-47e0-854e-090f7ea313c8.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 10:12:51.692816", "modified": "2025-01-28 10:12:51.692838"}
94	{"name": "data", "value": "/public/bioml/images", "type": "1", "datatype": "<class 'str'>", "created": "2025-01-28 10:12:51.812175", "modified": "2025-01-28 10:12:51.812188"}
95	{"value": "/users/testuser/temp/67189135-a7f7-42ae-9388-b362e05484cc/b45163f9-173b-4b49-80d1-a12efcc62592/adaee106-9426-41ab-b6c8-dfdc8e6e2124.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 10:12:53.428494", "modified": "2025-01-28 10:12:53.428503"}
96	{"name": "biodata", "value": "/users/testuser/temp/67189135-a7f7-42ae-9388-b362e05484cc/b45163f9-173b-4b49-80d1-a12efcc62592/944c20b3-f715-47e0-854e-090f7ea313c8.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 10:12:53.513132", "modified": "2025-01-28 10:12:53.513143"}
97	{"name": "imgdata", "value": "/users/testuser/temp/67189135-a7f7-42ae-9388-b362e05484cc/b45163f9-173b-4b49-80d1-a12efcc62592/adaee106-9426-41ab-b6c8-dfdc8e6e2124.csv", "type": "1", "datatype": "<class 'str'>", "created": "2025-01-28 10:12:53.529343", "modified": "2025-01-28 10:12:53.529354"}
98	{"value": "/users/testuser/temp/67189135-a7f7-42ae-9388-b362e05484cc/b45163f9-173b-4b49-80d1-a12efcc62592/d3dbaa03-c89d-4ddb-a372-e8b42160cc70.pkl", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 10:13:08.675399", "modified": "2025-01-28 10:13:08.675411"}
99	{"name": "data", "value": "/public/MiSeq_SOP/F3D149_S215_L001_R1_001.fastq", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 10:59:23.376121", "modified": "2025-01-28 10:59:23.376134"}
100	{"value": "/users/testuser/temp/74cf137b-7692-426c-806c-61e2eee6691f/e89516cd-e679-49a0-bb84-89f09cd9369b/463fdce1-a9a8-468b-b772-65e9deedc97a.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 10:59:24.319478", "modified": "2025-01-28 10:59:24.319487"}
101	{"name": "data", "value": "/public/MiSeq_SOP/F3D149_S215_L001_R1_001.fastq", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 10:59:49.380560", "modified": "2025-01-28 10:59:49.380577"}
148	{"name": "language", "value": "java", "type": "4096", "datatype": "<class 'str'>", "created": "2025-01-29 05:55:37.375340", "modified": "2025-01-29 05:55:37.375350"}
102	{"value": "/users/testuser/temp/7f070924-2710-4235-aa51-9702c3c09849/aacff1c0-124f-4fa4-82d9-417429e6a026/56684fc2-8b96-494c-9a18-762fd081f025.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 10:59:50.070984", "modified": "2025-01-28 10:59:50.070997"}
103	{"name": "data", "value": "/public/bioml/images", "type": "1", "datatype": "<class 'str'>", "created": "2025-01-28 10:59:50.149823", "modified": "2025-01-28 10:59:50.149835"}
104	{"value": "/users/testuser/temp/7f070924-2710-4235-aa51-9702c3c09849/aacff1c0-124f-4fa4-82d9-417429e6a026/de5acbf2-6b94-41f2-b975-6a8569456289.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 10:59:51.695529", "modified": "2025-01-28 10:59:51.695545"}
105	{"name": "biodata", "value": "/users/testuser/temp/7f070924-2710-4235-aa51-9702c3c09849/aacff1c0-124f-4fa4-82d9-417429e6a026/56684fc2-8b96-494c-9a18-762fd081f025.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 10:59:51.777316", "modified": "2025-01-28 10:59:51.777327"}
107	{"name": "model", "value": "/users/testuser/temp/67189135-a7f7-42ae-9388-b362e05484cc/b45163f9-173b-4b49-80d1-a12efcc62592/d3dbaa03-c89d-4ddb-a372-e8b42160cc70.pkl", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 10:59:51.809469", "modified": "2025-01-28 10:59:51.809480"}
108	{"value": "/users/testuser/temp/7f070924-2710-4235-aa51-9702c3c09849/aacff1c0-124f-4fa4-82d9-417429e6a026/csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 11:00:09.307127", "modified": "2025-01-28 11:00:09.307141"}
109	{"name": "data", "value": "/public/MiSeq_SOP/F3D149_S215_L001_R1_001.fastq", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 11:16:53.992577", "modified": "2025-01-28 11:16:53.992592"}
110	{"value": "/users/testuser/temp/760c934d-3e24-4ba3-9eba-0a3d648582ac/9662761a-fb24-4d58-ad4c-1708644e0e7d/daca631d-7197-43b0-a068-1afb964037ae.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 11:16:54.696215", "modified": "2025-01-28 11:16:54.696231"}
111	{"name": "data", "value": "/public/bioml/images", "type": "1", "datatype": "<class 'str'>", "created": "2025-01-28 11:16:54.774239", "modified": "2025-01-28 11:16:54.774250"}
112	{"value": "/users/testuser/temp/760c934d-3e24-4ba3-9eba-0a3d648582ac/9662761a-fb24-4d58-ad4c-1708644e0e7d/b18fb06f-bcdd-4879-b691-495218e96316.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 11:16:56.328836", "modified": "2025-01-28 11:16:56.328845"}
113	{"name": "biodata", "value": "/users/testuser/temp/760c934d-3e24-4ba3-9eba-0a3d648582ac/9662761a-fb24-4d58-ad4c-1708644e0e7d/daca631d-7197-43b0-a068-1afb964037ae.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 11:16:56.410079", "modified": "2025-01-28 11:16:56.410090"}
115	{"name": "model", "value": "/users/testuser/temp/67189135-a7f7-42ae-9388-b362e05484cc/b45163f9-173b-4b49-80d1-a12efcc62592/d3dbaa03-c89d-4ddb-a372-e8b42160cc70.pkl", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 11:16:56.438515", "modified": "2025-01-28 11:16:56.438533"}
106	{"name": "imgdata", "value": "/users/testuser/temp/7f070924-2710-4235-aa51-9702c3c09849/aacff1c0-124f-4fa4-82d9-417429e6a026/de5acbf2-6b94-41f2-b975-6a8569456289.csv", "type": "1", "datatype": "<class 'str'>", "created": "2025-01-28 10:59:51.793453", "modified": "2025-01-28 10:59:51.793464"}
114	{"name": "imgdata", "value": "/users/testuser/temp/760c934d-3e24-4ba3-9eba-0a3d648582ac/9662761a-fb24-4d58-ad4c-1708644e0e7d/b18fb06f-bcdd-4879-b691-495218e96316.csv", "type": "1", "datatype": "<class 'str'>", "created": "2025-01-28 11:16:56.424672", "modified": "2025-01-28 11:16:56.424682"}
116	{"value": "/users/testuser/temp/760c934d-3e24-4ba3-9eba-0a3d648582ac/9662761a-fb24-4d58-ad4c-1708644e0e7d/e4ae7264-4e6c-40d1-a686-419553b0264d.csv", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 11:18:47.397985", "modified": "2025-01-28 11:18:47.398005"}
117	{"name": "data", "value": "/public/swanalytics/luaj", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 12:07:07.592528", "modified": "2025-01-28 12:07:07.592541"}
118	{"value": "/public/swanalytics", "type": "1", "datatype": "<class 'str'>", "created": "2025-01-28 12:07:07.821703", "modified": "2025-01-28 12:07:07.821713"}
119	{"name": "data", "value": "/public/swanalytics", "type": "1", "datatype": "<class 'str'>", "created": "2025-01-28 12:07:07.917682", "modified": "2025-01-28 12:07:07.917696"}
120	{"value": "/public/swanalytics", "type": "1", "datatype": "<class 'str'>", "created": "2025-01-28 12:07:30.154174", "modified": "2025-01-28 12:07:30.154192"}
121	{"name": "data", "value": "/public/swanalytics/luaj", "type": "1", "datatype": "<class 'str'>", "created": "2025-01-28 12:07:30.251194", "modified": "2025-01-28 12:07:30.251213"}
122	{"name": "granularity", "value": "blocks", "type": "4096", "datatype": "<class 'str'>", "created": "2025-01-28 12:07:30.269419", "modified": "2025-01-28 12:07:30.269432"}
123	{"name": "language", "value": "java", "type": "4096", "datatype": "<class 'str'>", "created": "2025-01-28 12:07:30.292940", "modified": "2025-01-28 12:07:30.292957"}
124	{"value": "/public/swanalytics/luaj_blocks.xml", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 12:07:52.056254", "modified": "2025-01-28 12:07:52.056270"}
125	{"name": "data", "value": "/public/swanalytics/luaj_blocks.xml", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 12:07:52.165824", "modified": "2025-01-28 12:07:52.165836"}
126	{"name": "granularity", "value": "blocks", "type": "4096", "datatype": "<class 'str'>", "created": "2025-01-28 12:07:52.183801", "modified": "2025-01-28 12:07:52.183813"}
127	{"name": "language", "value": "java", "type": "4096", "datatype": "<class 'str'>", "created": "2025-01-28 12:07:52.200434", "modified": "2025-01-28 12:07:52.200447"}
128	{"name": "renaming", "value": "blind", "type": "4096", "datatype": "<class 'str'>", "created": "2025-01-28 12:07:52.228789", "modified": "2025-01-28 12:07:52.228803"}
129	{"value": "/public/swanalytics/luaj_blocks-blind.xml", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 12:07:53.018174", "modified": "2025-01-28 12:07:53.018186"}
130	{"name": "data", "value": "/public/swanalytics/luaj_blocks-blind.xml", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 12:07:53.156729", "modified": "2025-01-28 12:07:53.156748"}
131	{"name": "threshold", "value": "0.3", "type": "4096", "datatype": "<class 'str'>", "created": "2025-01-28 12:07:53.183641", "modified": "2025-01-28 12:07:53.184024"}
132	{"name": "minclonesize", "value": "10", "type": "4096", "datatype": "<class 'str'>", "created": "2025-01-28 12:07:53.204866", "modified": "2025-01-28 12:07:53.204879"}
133	{"name": "maxclonesize", "value": "2500", "type": "4096", "datatype": "<class 'str'>", "created": "2025-01-28 12:07:53.225846", "modified": "2025-01-28 12:07:53.225858"}
134	{"value": "/public/swanalytics/luaj_blocks-blind-clones/luaj_blocks-blind-clones-0.3.xml", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 12:07:53.447590", "modified": "2025-01-28 12:07:53.447608"}
135	{"name": "data", "value": "/public/swanalytics/luaj_blocks-blind-clones/luaj_blocks-blind-clones-0.3.xml", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 12:07:53.566879", "modified": "2025-01-28 12:07:53.566891"}
136	{"value": "/public/swanalytics/luaj_blocks-blind-clones/luaj_blocks-blind-clones-0.3-classes.xml", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 12:07:53.670790", "modified": "2025-01-28 12:07:53.670806"}
137	{"name": "data", "value": "/public/swanalytics/luaj_blocks-blind-clones/luaj_blocks-blind-clones-0.3-classes.xml", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 12:07:53.767628", "modified": "2025-01-28 12:07:53.767640"}
138	{"value": "/public/swanalytics/luaj_blocks-blind-clones/luaj_blocks-blind-clones-0.3-classes-withsource.xml", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 12:07:53.836100", "modified": "2025-01-28 12:07:53.836117"}
139	{"name": "data", "value": "/public/swanalytics/luaj_blocks-blind-clones/luaj_blocks-blind-clones-0.3-classes-withsource.xml", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 12:07:53.938507", "modified": "2025-01-28 12:07:53.938523"}
140	{"value": "/public/swanalytics/luaj_blocks-blind-clones/luaj_blocks-blind-clones-0.3-classes-withsource.html", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 12:07:54.029058", "modified": "2025-01-28 12:07:54.029071"}
141	{"value": "/public/swanalytics/luaj_blocks-blind-clones/luaj_blocks-blind-clones-0.3.xml", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-28 12:07:54.132061", "modified": "2025-01-28 12:07:54.132075"}
142	{"name": "data", "value": "/public/swanalytics/luaj", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-29 05:55:36.880175", "modified": "2025-01-29 05:55:36.880189"}
143	{"value": "/public/swanalytics", "type": "1", "datatype": "<class 'str'>", "created": "2025-01-29 05:55:36.940753", "modified": "2025-01-29 05:55:36.940765"}
144	{"name": "data", "value": "/public/swanalytics", "type": "1", "datatype": "<class 'str'>", "created": "2025-01-29 05:55:37.011695", "modified": "2025-01-29 05:55:37.011704"}
145	{"value": "/public/swanalytics", "type": "1", "datatype": "<class 'str'>", "created": "2025-01-29 05:55:37.268700", "modified": "2025-01-29 05:55:37.268711"}
146	{"name": "data", "value": "/public/swanalytics/luaj", "type": "1", "datatype": "<class 'str'>", "created": "2025-01-29 05:55:37.347141", "modified": "2025-01-29 05:55:37.347152"}
147	{"name": "granularity", "value": "blocks", "type": "4096", "datatype": "<class 'str'>", "created": "2025-01-29 05:55:37.362670", "modified": "2025-01-29 05:55:37.362681"}
149	{"value": "/public/swanalytics/luaj_blocks.xml", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-29 05:55:39.263970", "modified": "2025-01-29 05:55:39.263976"}
150	{"name": "data", "value": "/public/swanalytics/luaj_blocks.xml", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-29 05:55:39.312661", "modified": "2025-01-29 05:55:39.312671"}
152	{"name": "language", "value": "java", "type": "4096", "datatype": "<class 'str'>", "created": "2025-01-29 05:55:39.332069", "modified": "2025-01-29 05:55:39.332080"}
156	{"name": "threshold", "value": "0.3", "type": "4096", "datatype": "<class 'str'>", "created": "2025-01-29 05:55:39.995413", "modified": "2025-01-29 05:55:39.995423"}
158	{"name": "maxclonesize", "value": "2500", "type": "4096", "datatype": "<class 'str'>", "created": "2025-01-29 05:55:40.015265", "modified": "2025-01-29 05:55:40.015276"}
159	{"value": "/public/swanalytics/luaj_blocks-blind-clones/luaj_blocks-blind-clones-0.3.xml", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-29 05:55:40.111004", "modified": "2025-01-29 05:55:40.111013"}
160	{"name": "data", "value": "/public/swanalytics/luaj_blocks-blind-clones/luaj_blocks-blind-clones-0.3.xml", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-29 05:55:40.154429", "modified": "2025-01-29 05:55:40.154436"}
161	{"value": "/public/swanalytics/luaj_blocks-blind-clones/luaj_blocks-blind-clones-0.3-classes.xml", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-29 05:55:40.210882", "modified": "2025-01-29 05:55:40.210890"}
162	{"name": "data", "value": "/public/swanalytics/luaj_blocks-blind-clones/luaj_blocks-blind-clones-0.3-classes.xml", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-29 05:55:40.254336", "modified": "2025-01-29 05:55:40.254342"}
163	{"value": "/public/swanalytics/luaj_blocks-blind-clones/luaj_blocks-blind-clones-0.3-classes-withsource.xml", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-29 05:55:40.301781", "modified": "2025-01-29 05:55:40.301787"}
164	{"name": "data", "value": "/public/swanalytics/luaj_blocks-blind-clones/luaj_blocks-blind-clones-0.3-classes-withsource.xml", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-29 05:55:40.347882", "modified": "2025-01-29 05:55:40.347889"}
165	{"value": "/public/swanalytics/luaj_blocks-blind-clones/luaj_blocks-blind-clones-0.3-classes-withsource.html", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-29 05:55:40.392029", "modified": "2025-01-29 05:55:40.392041"}
151	{"name": "granularity", "value": "blocks", "type": "4096", "datatype": "<class 'str'>", "created": "2025-01-29 05:55:39.321317", "modified": "2025-01-29 05:55:39.321326"}
153	{"name": "renaming", "value": "blind", "type": "4096", "datatype": "<class 'str'>", "created": "2025-01-29 05:55:39.340321", "modified": "2025-01-29 05:55:39.340328"}
154	{"value": "/public/swanalytics/luaj_blocks-blind.xml", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-29 05:55:39.934346", "modified": "2025-01-29 05:55:39.934355"}
155	{"name": "data", "value": "/public/swanalytics/luaj_blocks-blind.xml", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-29 05:55:39.985201", "modified": "2025-01-29 05:55:39.985210"}
157	{"name": "minclonesize", "value": "10", "type": "4096", "datatype": "<class 'str'>", "created": "2025-01-29 05:55:40.004189", "modified": "2025-01-29 05:55:40.004199"}
166	{"name": "data", "value": "[1, 2, 3, 4, 5]", "type": "4096", "datatype": "<class 'str'>", "created": "2025-01-29 06:10:51.387373", "modified": "2025-01-29 06:10:51.387387"}
167	{"name": "data2", "value": "[100, 200, 150, 500, 400]", "type": "4096", "datatype": "<class 'str'>", "created": "2025-01-29 06:10:51.408300", "modified": "2025-01-29 06:10:51.408312"}
168	{"value": "/users/testuser/temp/3eff9190-3a50-4cb3-b56b-b11e0cc7c8b4/books_read.png", "type": "2", "datatype": "<class 'str'>", "created": "2025-01-29 06:10:52.372443", "modified": "2025-01-29 06:10:52.372454"}
\.


--
-- Data for Name: data_allocations; Type: TABLE DATA; Schema: public; Owner: phenodoop
--

COPY public.data_allocations (id, data_id, user_id, rights) FROM stdin;
1	1	46	1
2	2	46	1
3	3	46	1
4	4	46	1
5	5	46	7
6	6	46	1
7	7	46	1
8	8	46	7
9	9	46	1
10	10	46	7
11	11	46	1
12	12	46	1
13	13	46	7
14	14	46	1
15	15	46	7
16	16	46	1
17	17	46	7
18	18	46	1
19	19	46	7
20	20	46	1
21	21	46	7
22	22	46	1
23	23	46	7
24	24	46	1
25	25	46	7
26	26	46	1
27	27	46	7
28	28	46	1
29	29	46	7
30	30	46	1
31	31	46	7
32	32	46	1
33	33	46	7
34	34	46	1
35	35	46	7
36	36	46	1
37	37	46	7
38	38	46	1
39	39	46	7
40	40	46	1
41	41	46	7
42	42	46	1
43	43	46	7
44	44	46	1
45	45	46	7
46	46	46	1
47	47	46	7
48	48	46	1
49	49	46	1
50	50	46	1
51	51	46	7
52	52	46	1
53	53	46	7
54	54	46	1
55	55	46	1
56	56	46	1
57	57	46	7
58	58	46	1
59	59	46	7
60	60	46	1
61	61	46	1
62	62	46	1
63	63	46	7
64	64	46	1
65	65	46	7
66	66	46	1
67	67	46	1
68	68	46	1
69	69	46	7
70	70	46	1
71	71	46	7
72	72	46	1
73	73	46	1
74	74	46	1
75	75	46	7
76	76	46	1
77	77	46	7
78	78	46	1
79	79	46	1
80	80	46	1
81	81	46	7
82	82	46	1
83	83	46	7
84	84	46	1
85	85	46	1
86	86	46	1
87	87	46	7
88	88	46	1
89	89	46	7
90	90	46	1
91	91	46	1
92	92	46	1
93	93	46	7
94	94	46	1
95	95	46	7
96	96	46	1
97	97	46	1
98	98	46	7
99	99	46	1
100	100	46	7
101	101	46	1
102	102	46	7
103	103	46	1
104	104	46	7
105	105	46	1
106	106	46	1
107	107	46	1
108	108	46	7
109	109	46	1
110	110	46	7
111	111	46	1
112	112	46	7
113	113	46	1
114	114	46	1
115	115	46	1
116	116	46	7
117	117	46	1
118	118	46	7
119	119	46	1
120	120	46	7
121	121	46	1
122	122	46	1
123	123	46	1
124	124	46	7
125	125	46	1
126	126	46	1
127	127	46	1
128	128	46	1
129	129	46	7
130	130	46	1
131	131	46	1
132	132	46	1
133	133	46	1
134	134	46	7
135	135	46	1
136	136	46	7
137	137	46	1
138	138	46	7
139	139	46	1
140	140	46	7
141	141	46	7
142	142	46	1
143	143	46	7
144	144	46	1
145	145	46	7
146	146	46	1
147	147	46	1
148	148	46	1
149	149	46	7
150	150	46	1
151	151	46	1
152	152	46	1
153	153	46	1
154	154	46	7
155	155	46	1
156	156	46	1
157	157	46	1
158	158	46	1
159	159	46	7
160	160	46	1
161	161	46	7
162	162	46	1
163	163	46	7
164	164	46	1
165	165	46	7
166	166	46	1
167	167	46	1
168	168	46	7
\.


--
-- Data for Name: data_annotations; Type: TABLE DATA; Schema: public; Owner: phenodoop
--

COPY public.data_annotations (id, data_id, tag) FROM stdin;
\.


--
-- Data for Name: data_chunks; Type: TABLE DATA; Schema: public; Owner: phenodoop
--

COPY public.data_chunks (id, user_id, file_uuid, path, chunk, total_chunk, uploaded_size, total_size) FROM stdin;
\.


--
-- Data for Name: data_mimetypes; Type: TABLE DATA; Schema: public; Owner: phenodoop
--

COPY public.data_mimetypes (id, data_id, mimetype_id) FROM stdin;
\.


--
-- Data for Name: data_permissions; Type: TABLE DATA; Schema: public; Owner: phenodoop
--

COPY public.data_permissions (id, user_id, data_id, rights) FROM stdin;
\.


--
-- Data for Name: data_properties; Type: TABLE DATA; Schema: public; Owner: phenodoop
--

COPY public.data_properties (id, data_id, key, value) FROM stdin;
1	5	execution 4	{"workflow": {"task_id": 4, "job_id": 5, "workflow_id": 36, "inout": "out"}}
2	8	execution 6	{"workflow": {"task_id": 6, "job_id": 6, "workflow_id": 36, "inout": "out"}}
3	10	execution 7	{"workflow": {"task_id": 7, "job_id": 7, "workflow_id": 36, "inout": "out"}}
4	13	execution 9	{"workflow": {"task_id": 9, "job_id": 8, "workflow_id": 36, "inout": "out"}}
5	15	execution 10	{"workflow": {"task_id": 10, "job_id": 8, "workflow_id": 36, "inout": "out"}}
6	17	execution 11	{"workflow": {"task_id": 11, "job_id": 9, "workflow_id": 36, "inout": "out"}}
7	19	execution 12	{"workflow": {"task_id": 12, "job_id": 9, "workflow_id": 36, "inout": "out"}}
8	21	execution 13	{"workflow": {"task_id": 13, "job_id": 10, "workflow_id": 36, "inout": "out"}}
9	23	execution 14	{"workflow": {"task_id": 14, "job_id": 10, "workflow_id": 36, "inout": "out"}}
10	25	execution 15	{"workflow": {"task_id": 15, "job_id": 11, "workflow_id": 36, "inout": "out"}}
11	27	execution 16	{"workflow": {"task_id": 16, "job_id": 11, "workflow_id": 36, "inout": "out"}}
12	29	execution 17	{"workflow": {"task_id": 17, "job_id": 12, "workflow_id": 36, "inout": "out"}}
13	31	execution 18	{"workflow": {"task_id": 18, "job_id": 12, "workflow_id": 36, "inout": "out"}}
14	33	execution 19	{"workflow": {"task_id": 19, "job_id": 13, "workflow_id": 36, "inout": "out"}}
15	35	execution 20	{"workflow": {"task_id": 20, "job_id": 13, "workflow_id": 36, "inout": "out"}}
16	37	execution 21	{"workflow": {"task_id": 21, "job_id": 14, "workflow_id": 36, "inout": "out"}}
17	39	execution 22	{"workflow": {"task_id": 22, "job_id": 14, "workflow_id": 36, "inout": "out"}}
18	41	execution 23	{"workflow": {"task_id": 23, "job_id": 15, "workflow_id": 36, "inout": "out"}}
19	43	execution 24	{"workflow": {"task_id": 24, "job_id": 15, "workflow_id": 36, "inout": "out"}}
20	45	execution 25	{"workflow": {"task_id": 25, "job_id": 16, "workflow_id": 36, "inout": "out"}}
21	47	execution 26	{"workflow": {"task_id": 26, "job_id": 16, "workflow_id": 36, "inout": "out"}}
22	51	execution 28	{"workflow": {"task_id": 28, "job_id": 17, "workflow_id": 36, "inout": "out"}}
23	53	execution 29	{"workflow": {"task_id": 29, "job_id": 17, "workflow_id": 36, "inout": "out"}}
24	57	execution 31	{"workflow": {"task_id": 31, "job_id": 18, "workflow_id": 36, "inout": "out"}}
25	59	execution 32	{"workflow": {"task_id": 32, "job_id": 18, "workflow_id": 36, "inout": "out"}}
26	63	execution 34	{"workflow": {"task_id": 34, "job_id": 19, "workflow_id": 36, "inout": "out"}}
27	65	execution 35	{"workflow": {"task_id": 35, "job_id": 19, "workflow_id": 36, "inout": "out"}}
28	69	execution 37	{"workflow": {"task_id": 37, "job_id": 20, "workflow_id": 36, "inout": "out"}}
29	71	execution 38	{"workflow": {"task_id": 38, "job_id": 20, "workflow_id": 36, "inout": "out"}}
30	75	execution 40	{"workflow": {"task_id": 40, "job_id": 21, "workflow_id": 36, "inout": "out"}}
31	77	execution 41	{"workflow": {"task_id": 41, "job_id": 21, "workflow_id": 36, "inout": "out"}}
32	81	execution 43	{"workflow": {"task_id": 43, "job_id": 22, "workflow_id": 36, "inout": "out"}}
33	83	execution 44	{"workflow": {"task_id": 44, "job_id": 22, "workflow_id": 36, "inout": "out"}}
34	87	execution 46	{"workflow": {"task_id": 46, "job_id": 23, "workflow_id": 36, "inout": "out"}}
35	89	execution 47	{"workflow": {"task_id": 47, "job_id": 23, "workflow_id": 36, "inout": "out"}}
36	93	execution 49	{"workflow": {"task_id": 49, "job_id": 24, "workflow_id": 36, "inout": "out"}}
37	95	execution 50	{"workflow": {"task_id": 50, "job_id": 24, "workflow_id": 36, "inout": "out"}}
38	98	execution 51	{"workflow": {"task_id": 51, "job_id": 24, "workflow_id": 36, "inout": "out"}}
39	100	execution 52	{"workflow": {"task_id": 52, "job_id": 25, "workflow_id": 37, "inout": "out"}}
40	102	execution 53	{"workflow": {"task_id": 53, "job_id": 26, "workflow_id": 37, "inout": "out"}}
41	104	execution 54	{"workflow": {"task_id": 54, "job_id": 26, "workflow_id": 37, "inout": "out"}}
42	108	execution 55	{"workflow": {"task_id": 55, "job_id": 26, "workflow_id": 37, "inout": "out"}}
43	110	execution 56	{"workflow": {"task_id": 56, "job_id": 27, "workflow_id": 37, "inout": "out"}}
44	112	execution 57	{"workflow": {"task_id": 57, "job_id": 27, "workflow_id": 37, "inout": "out"}}
45	116	execution 58	{"workflow": {"task_id": 58, "job_id": 27, "workflow_id": 37, "inout": "out"}}
46	118	execution 59	{"workflow": {"task_id": 59, "job_id": 28, "workflow_id": 35, "inout": "out"}}
47	120	execution 60	{"workflow": {"task_id": 60, "job_id": 28, "workflow_id": 35, "inout": "out"}}
48	124	execution 61	{"workflow": {"task_id": 61, "job_id": 28, "workflow_id": 35, "inout": "out"}}
49	129	execution 62	{"workflow": {"task_id": 62, "job_id": 28, "workflow_id": 35, "inout": "out"}}
50	134	execution 63	{"workflow": {"task_id": 63, "job_id": 28, "workflow_id": 35, "inout": "out"}}
51	136	execution 64	{"workflow": {"task_id": 64, "job_id": 28, "workflow_id": 35, "inout": "out"}}
52	138	execution 65	{"workflow": {"task_id": 65, "job_id": 28, "workflow_id": 35, "inout": "out"}}
53	140	execution 66	{"workflow": {"task_id": 66, "job_id": 28, "workflow_id": 35, "inout": "out"}}
54	141	execution 28	{"workflow": {"job_id": 28, "workflow_id": 35, "inout": "out"}}
55	143	execution 67	{"workflow": {"task_id": 67, "job_id": 29, "workflow_id": 38, "inout": "out"}}
56	145	execution 68	{"workflow": {"task_id": 68, "job_id": 29, "workflow_id": 38, "inout": "out"}}
57	149	execution 69	{"workflow": {"task_id": 69, "job_id": 29, "workflow_id": 38, "inout": "out"}}
58	154	execution 70	{"workflow": {"task_id": 70, "job_id": 29, "workflow_id": 38, "inout": "out"}}
59	159	execution 71	{"workflow": {"task_id": 71, "job_id": 29, "workflow_id": 38, "inout": "out"}}
60	161	execution 72	{"workflow": {"task_id": 72, "job_id": 29, "workflow_id": 38, "inout": "out"}}
61	163	execution 73	{"workflow": {"task_id": 73, "job_id": 29, "workflow_id": 38, "inout": "out"}}
62	165	execution 74	{"workflow": {"task_id": 74, "job_id": 29, "workflow_id": 38, "inout": "out"}}
63	168	execution 75	{"workflow": {"task_id": 75, "job_id": 30, "workflow_id": 39, "inout": "out"}}
\.


--
-- Data for Name: data_visualizers; Type: TABLE DATA; Schema: public; Owner: phenodoop
--

COPY public.data_visualizers (id, data_id, visualizer_id) FROM stdin;
\.


--
-- Data for Name: datasets; Type: TABLE DATA; Schema: public; Owner: phenodoop
--

COPY public.datasets (id, schema) FROM stdin;
\.


--
-- Data for Name: datasource_allocations; Type: TABLE DATA; Schema: public; Owner: phenodoop
--

COPY public.datasource_allocations (id, datasource_id, url) FROM stdin;
\.


--
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
-- Data for Name: dockercontainers; Type: TABLE DATA; Schema: public; Owner: phenodoop
--

COPY public.dockercontainers (id, user_id, image_id, name, args, command) FROM stdin;
\.


--
-- Data for Name: dockerimages; Type: TABLE DATA; Schema: public; Owner: phenodoop
--

COPY public.dockerimages (id, user_id, name) FROM stdin;
\.


--
-- Data for Name: filter_history; Type: TABLE DATA; Schema: public; Owner: phenodoop
--

COPY public.filter_history (id, user_id, value, created_on) FROM stdin;
\.


--
-- Data for Name: filters; Type: TABLE DATA; Schema: public; Owner: phenodoop
--

COPY public.filters (id, user_id, name, value, created_on) FROM stdin;
\.


--
-- Data for Name: follows; Type: TABLE DATA; Schema: public; Owner: phenodoop
--

COPY public.follows (follower_id, followed_id, "timestamp") FROM stdin;
46	46	2025-01-25 01:03:47.310555
47	47	2025-01-25 01:04:12.963923
\.


--
-- Data for Name: indata; Type: TABLE DATA; Schema: public; Owner: phenodoop
--

COPY public.indata (id, task_id, data_id) FROM stdin;
\.


--
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
14	text/plain	\N	txt
15	text/plain	\N	sam
\.


--
-- Data for Name: params; Type: TABLE DATA; Schema: public; Owner: phenodoop
--

COPY public.params (id, service_id, value) FROM stdin;
298	133	{"name": "data", "type": "file"}
299	133	{"name": "barcode", "type": "file"}
300	133	{"name": "barcodeCol", "type": "str"}
301	134	{"name": "data", "type": "file"}
302	135	{"name": "data", "type": "file"}
303	135	{"name": "trimleft", "type": "int"}
304	135	{"name": "trunclen", "type": "int"}
305	136	{"name": "data", "type": "file"}
306	136	{"name": "trimlen", "type": "int"}
307	137	{"name": "data", "type": "file"}
308	138	{"name": "data", "type": "file"}
309	139	{"name": "data", "type": "file"}
310	140	{"name": "data", "type": "file"}
311	140	{"name": "metadata", "type": "file"}
312	141	{"name": "data", "type": "file"}
313	142	{"name": "data", "type": "file"}
314	143	{"name": "data", "type": "file"}
315	143	{"name": "table", "type": "file"}
316	143	{"name": "metadata", "type": "file"}
317	143	{"name": "sampling", "type": "int", "desc": "The sampling depth"}
318	143	{"name": "output", "type": "folder", "desc": "bray_curtis_distance_matrix.qza rarefied_table.qza bray_curtis_emperor.qzv shannon_vector.qza bray_curtis_pcoa_results.qza unweighted_unifrac_distance_matrix.qza evenness_vector.qza unweighted_unifrac_emperor.qzv faith_pd_vector.qza unweighted_unifrac_pcoa_results.qza jaccard_distance_matrix.qza weighted_unifrac_distance_matrix.qza jaccard_emperor.qzv weighted_unifrac_emperor.qzv jaccard_pcoa_results.qza weighted_unifrac_pcoa_results.qza observed_otus_vector.qza"}
319	144	{"name": "data", "type": "file"}
320	144	{"name": "metadata", "type": "file"}
321	144	{"name": "output", "type": "file"}
322	145	{"name": "data", "type": "file"}
323	145	{"name": "metadata", "type": "file"}
324	145	{"name": "metadataCol", "type": "str"}
325	145	{"name": "output", "type": "file"}
326	146	{"name": "data", "type": "file"}
327	146	{"name": "metadata", "type": "file"}
328	146	{"name": "customAxes", "type": "str"}
329	146	{"name": "output", "type": "file"}
330	147	{"name": "data", "type": "file"}
331	147	{"name": "metadata", "type": "file"}
332	147	{"name": "customAxes", "type": "str"}
333	147	{"name": "output", "type": "file"}
334	148	{"name": "data", "type": "file"}
335	148	{"name": "classifier", "type": "file"}
336	148	{"name": "output", "type": "file"}
337	149	{"name": "data", "type": "file"}
338	149	{"name": "table", "type": "file"}
339	149	{"name": "metadata", "type": "file"}
340	149	{"name": "output", "type": "file"}
341	150	{"name": "data", "type": "file"}
342	150	{"name": "metadata", "type": "file"}
343	150	{"name": "where", "type": "str"}
344	150	{"name": "output", "type": "file"}
345	151	{"name": "data", "type": "file"}
346	151	{"name": "output", "type": "file"}
347	152	{"name": "data", "type": "file"}
348	152	{"name": "metadata", "type": "file"}
349	152	{"name": "metadataCol", "type": "str"}
350	152	{"name": "output", "type": "file"}
351	153	{"name": "data", "type": "file"}
352	153	{"name": "table", "type": "file"}
353	153	{"name": "level", "type": "int"}
354	153	{"name": "output", "type": "file"}
355	154	{"name": "data", "type": "folder"}
356	154	{"name": "data", "type": "str"}
357	156	{"name": "command", "type": "str"}
358	156	{"name": "input", "type": "file"}
359	156	{"name": "outtype", "default": "fasta", "type": "str"}
360	157	{"name": "dag_file", "type": "file", "desc": "The output file generated by SynMap which includes Ks values"}
361	157	{"name": "xhead", "type": "file", "desc": "Header for labels of chromosomes from the genome on x-axis"}
362	157	{"name": "yhead", "type": "file", "desc": "Header for labels of chromosomes from the genome on y-axis"}
363	158	{"name": "data", "type": "file"}
364	158	{"name": "command", "type": "str"}
365	159	{"name": "data", "type": "file"}
366	160	{"name": "data", "type": "file"}
367	160	{"name": "sample", "type": "int"}
368	160	{"name": "seed", "type": "int"}
369	161	{"name": "data", "type": "folder"}
370	161	{"name": "granularity", "default": "'functions'", "type": "str", "desc": "functions|blocks"}
371	161	{"name": "language", "default": "'java'", "type": "str", "desc": "'java'|'python'|'c'|'php'"}
372	162	{"name": "data", "type": "file"}
373	162	{"name": "lines", "type": "int"}
374	162	{"name": "start", "type": "int"}
375	163	{"name": "data", "type": "str"}
376	163	{"name": "begin", "type": "int"}
377	163	{"name": "end", "type": "int"}
378	163	{"name": "quality", "type": "float"}
379	164	{"name": "query", "type": "file", "desc": "Query sequence file in FASTA format"}
380	164	{"name": "db", "type": "file", "desc": "Database sequence file in FASTA format"}
381	165	{"name": "data", "type": "folder"}
382	166	{"name": "data", "type": "file"}
383	166	{"name": "type", "default": "'fasta'", "type": "str"}
384	167	{"name": "data", "type": "file", "desc": "DAGChainer output file with genomic coordinates converted from gene order to nucleotide positions"}
385	167	{"name": "dsgid1", "default": "''", "type": "str", "desc": "CoGe's database id for query genome"}
386	167	{"name": "dsgid2", "default": "''", "type": "str", "desc": "CoGe's database id for subject genome"}
387	168	{"name": "blast", "type": "file", "desc": "Blast file to convert and/or process"}
388	168	{"name": "qbed", "type": "file", "desc": "BED file for query sequence"}
389	168	{"name": "sbed", "type": "file", "desc": "BED file for query sequence"}
390	168	{"name": "tandem_Nmax", "default": "10", "type": "int", "desc": "merge tandem genes within distance"}
391	168	{"name": "cscore", "default": "0", "type": "int", "desc": "retain hits that have good bitscore"}
392	169	{"name": "data", "type": "file"}
393	169	{"name": "data2", "default": "''", "type": "file"}
394	169	{"name": "adapter", "default": "'CTGTCTCTTATACACATCT'", "type": "str"}
395	169	{"name": "min_length", "default": "0", "type": "int", "desc": "Discard reads shorter than LEN"}
396	169	{"name": "quality", "default": "20", "type": "int", "desc": "Trim low-quality bases from 5' and/or 3' ends of each read before adapter removal."}
397	170	{"name": "data", "type": "file", "desc": "gcoords file"}
398	171	{"name": "data", "type": "folder", "desc": "The folder with clone pair files."}
399	171	{"name": "model", "type": "file", "desc": "Trained neural network."}
400	171	{"name": "language", "default": "'java'", "type": "str", "desc": "The language."}
401	171	{"name": "threshold", "default": 0.5, "type": "float", "desc": "The validation threshold."}
402	172	{"name": "data", "type": "file", "desc": "The clone file."}
403	172	{"name": "response", "type": "str", "desc": "The response of manual validation."}
404	172	{"name": "fragment1", "type": "file", "desc": "The path of fragment 1."}
405	172	{"name": "startline1", "type": "int", "desc": "The start line of fragment 1."}
406	172	{"name": "endline1", "type": "int", "desc": "The end line of fragment 1."}
407	172	{"name": "fragment2", "type": "file", "desc": "The path of fragment 2."}
408	172	{"name": "startLine2", "type": "int", "desc": "The start line of fragment 2."}
409	172	{"name": "endLine2", "type": "int", "desc": "The end line of fragment 2."}
410	173	{"name": "data", "type": "file", "desc": "The training dataset in csv file."}
411	174	{"name": "ref", "type": "file", "desc": "The reference genome."}
412	174	{"name": "data", "type": "file|folder", "desc": "If it is a folder name, all .fastq and .fq files are recursively collected from that folder."}
413	174	{"name": "data2", "default": "''", "type": "file|folder", "desc": "Reverse seq for pair-end read. If it is a folder, all .fastq and .fq files are recursively collected."}
414	175	{"name": "ref", "type": "file", "desc": "the reference genome."}
415	175	{"name": "data", "type": "file|folder", "desc": "Seq file for single read, forward seq file for pair-end. If folder, all .fastq/.fq files are recursively collected from that folder."}
416	175	{"name": "data2", "default": "''", "type": "file|folder", "desc": "Reverse seq file for pair-end. If folder, all .fastq/.fq files are recursively collected from that folder."}
417	176	{"name": "data", "type": "file"}
418	176	{"name": "txlfile", "default": "''", "type": "file"}
419	177	{"name": "data", "type": "file|folder", "desc": "forward fastq file"}
420	177	{"name": "data2", "type": "file|folder", "desc": "reverse fastq file"}
421	178	{"name": "data", "type": "str", "desc": "forward fastq file"}
422	178	{"name": "data2", "type": "str", "desc": "reverse fastq file"}
423	178	{"name": "max_overlap", "default": 50, "type": "int"}
424	179	{"name": "blast_file", "type": "file", "desc": "BLAST file to format"}
425	179	{"name": "query", "default": "'a'", "type": "str", "desc": "the name of the query organism"}
426	179	{"name": "subject", "default": "'b'", "type": "str", "desc": "the name of the subject organism"}
427	180	{"name": "dag", "type": "file", "desc": "dag file with format a_seqid<tab>a_accn<tab>a_start<tab>a_end<tab>b_seqid<tab>b_accn<tab>b_start<tab>b_end<tab>e-value"}
428	180	{"name": "gap_init", "default": "0", "type": "int", "desc": "gap open penalty"}
429	180	{"name": "gap_extend", "default": "-3", "type": "int", "desc": "gap extension penalty"}
430	180	{"name": "min_score", "default": "0", "type": "int", "desc": "minimum alignment score"}
431	180	{"name": "gap_dist", "default": "10.0", "type": "float", "desc": "average distance expected between 2 syntenic genes"}
432	180	{"name": "gap_max", "default": "20.0", "type": "float", "desc": "maximum distance between 2 matches"}
433	180	{"name": "e_value", "default": "0.05", "type": "float", "desc": "maximum e-value"}
434	180	{"name": "min_aligned_pairs", "default": "5", "type": "int", "desc": "minimum number of pairs to be considered a diagonal"}
435	181	{"name": "data", "type": "file", "desc": "sam file"}
436	181	{"name": "output", "type": "file", "desc": "[optional]. A .bam file."}
437	182	{"name": "data", "type": "file", "desc": "input bam file"}
438	183	{"name": "data", "type": "file"}
439	183	{"name": "data2", "type": "file"}
440	184	{"name": "data", "type": "folder"}
441	184	{"name": "granularity", "default": "'functions'", "type": "str"}
442	184	{"name": "language", "default": "'java'", "type": "str"}
443	185	{"name": "data", "type": "folder"}
444	185	{"name": "data2", "type": "folder"}
445	185	{"name": "granularity", "default": "'functions'", "type": "str"}
446	185	{"name": "language", "default": "'java'", "type": "str"}
447	186	{"name": "data", "type": "file"}
448	186	{"name": "granularity", "default": "'functions'", "type": "str", "desc": "functions|blocks"}
449	186	{"name": "language", "default": "'java'", "type": "str", "desc": "'java'|'cs'|'python'|'c'|'php'"}
450	186	{"name": "nonterminals", "default": "'none'", "type": "str", "desc": "'none'|'condition'|'expression'"}
451	187	{"name": "data", "type": "file"}
452	187	{"name": "granularity", "default": "'functions'", "type": "str", "desc": "'functions'|'blocks'"}
453	187	{"name": "language", "default": "'java'", "type": "str", "desc": "'java'|'cs'|'python'|'c'|php'"}
454	187	{"name": "nonterminals", "default": "'none'", "type": "str", "desc": "'none'|'declaration'"}
455	188	{"name": "data", "type": "file"}
456	188	{"name": "granularity", "default": "'functions'", "type": "str", "desc": "'functions'|'blocks'"}
457	188	{"name": "language", "default": "'java'", "type": "str", "desc": "'java'|'cs'|'python'|'c'|'php'"}
458	188	{"name": "transform", "default": "'none'", "type": "str", "desc": "'none'|'sort'"}
459	189	{"name": "data", "type": "file"}
460	189	{"name": "granularity", "default": "'functions'", "type": "str", "desc": "'functions'|'blocks'"}
461	189	{"name": "language", "default": "'java'", "type": "str", "desc": "'java'|'cs'|'python'|'c'|'php'"}
462	189	{"name": "renaming", "default": "'blind'", "type": "str", "desc": "'none'|'blind'|'consistent'"}
463	190	{"name": "data", "type": "file"}
464	190	{"name": "granularity", "default": "'functions'", "type": "str", "desc": "'functions'|'blocks'"}
465	190	{"name": "language", "default": "'java'", "type": "str", "desc": "'java'|'cs'|'python'|'c'|'php'"}
466	190	{"name": "normalizer", "default": "'java-normalize-ifconditions-functions'", "type": "str", "desc": "'none'|'java-normalize-ifconditions-functions'|'xmlsortblocks'|'cabstractifconditions'"}
467	191	{"name": "data", "type": "folder"}
468	192	{"name": "data", "type": "file"}
469	192	{"name": "threshold", "default": 0.3, "type": "float"}
470	192	{"name": "minclonesize", "default": "10", "type": "int"}
471	192	{"name": "maxclonesize", "default": "2500", "type": "int"}
472	192	{"name": "showsource", "type": "str", "desc": "showsource|none"}
473	193	{"name": "data", "type": "file"}
474	193	{"name": "threshold", "default": "0.3", "type": "float"}
475	193	{"name": "minclonesize", "default": "10", "type": "int"}
476	193	{"name": "maxclonesize", "default": "2500", "type": "int"}
477	193	{"name": "showsource", "type": "str", "desc": "showsource"}
478	194	{"name": "data", "type": "file"}
479	194	{"name": "threshold", "default": "0.3", "type": "float"}
480	194	{"name": "minclonesize", "default": "10", "type": "int"}
481	194	{"name": "maxclonesize", "default": "2500", "type": "int"}
482	194	{"name": "showsource", "type": "str", "desc": "showsource"}
483	195	{"name": "data", "type": "file"}
484	196	{"name": "data", "type": "file"}
485	197	{"name": "data", "type": "file", "desc": "The extracted functions or blocks in xml"}
486	197	{"name": "data2", "type": "file", "desc": "The clones in xml"}
487	198	{"name": "data", "type": "file", "desc": "Clone source file in xml."}
488	199	{"name": "data", "type": "file", "desc": "Clone source file in xml."}
489	200	{"name": "data", "type": "file", "desc": "basecalled nanopore reads or summary files generated by the basecallers Albacore, Guppy or MinKNOW"}
490	201	{"name": "data", "type": "file", "desc": "BLAST file to convert to BED"}
491	202	{"name": "url", "type": "str", "desc": "The repository path"}
492	202	{"name": "data", "type": "folder", "desc": "The local path"}
493	203	{"name": "data", "type": "file|folder", "desc": "if folder, all .fastq and .fq files are recursively collected from that folder."}
494	204	{"name": "input", "type": "file", "desc": "dag file to be ordered"}
495	204	{"name": "gid1", "default": "''", "type": "str", "desc": "first genome id"}
496	204	{"name": "gid2", "default": "''", "type": "str", "desc": "second genome id"}
497	204	{"name": "feature1", "default": "'CDS'", "type": "str", "desc": "feature of first genome"}
498	204	{"name": "feature2", "default": "'CDS'", "type": "str", "desc": "feature of second genome"}
499	205	{"name": "data", "type": "file[]"}
500	206	{"name": "data", "type": "str"}
501	206	{"name": "max_overlap", "default": 50, "type": "int"}
502	207	{"name": "data", "type": "int"}
503	208	{"name": "id", "type": "int", "desc": "Workflow ID."}
504	209	{"name": "data", "type": "file", "desc": "Query sequence to search for"}
505	209	{"name": "data2", "type": "file", "desc": "Subject sequence to search against"}
506	210	{"name": "x_seq", "type": "file"}
507	210	{"name": "y_seq", "type": "file"}
508	211	{"name": "data", "type": "file", "desc": "Multi-FASTA file of sequences to create database from"}
509	211	{"name": "dbtype", "default": "'nucl'", "type": "str", "desc": "Molecule type ('nucl', 'prot')"}
510	212	{"name": "query", "type": "file", "desc": "Nucleotide sequence(s) to search for."}
511	212	{"name": "db", "type": "str", "desc": "Nucleotide database to search into."}
512	212	{"name": "outfmt", "default": "0", "type": "int", "desc": "Format of BLAST result"}
513	212	{"name": "evalue", "default": "0.001", "type": "float", "desc": "Expected value cutoff"}
514	212	{"name": "task", "default": "'blastn'", "type": "str", "desc": "('blastn', 'blastn-short', 'dc-megablast', 'megablast', 'rmblastn')"}
515	213	{"name": "query", "type": "file", "desc": "Protein sequence(s) to search for."}
516	213	{"name": "db", "type": "str", "desc": "Protein database to search into."}
517	213	{"name": "outfmt", "default": "0", "type": "int", "desc": "Format of BLAST result"}
518	213	{"name": "evalue", "default": "0.001", "type": "float", "desc": "Expected value cutoff"}
519	213	{"name": "task", "default": "'blastp'", "type": "str", "desc": "('blastp', 'blastp-fast', 'blastp-short')"}
520	214	{"name": "query", "type": "file", "desc": "Protein sequence(s) to search for."}
521	214	{"name": "db", "type": "str", "desc": "Nucleotide database to search into."}
522	214	{"name": "outfmt", "default": "0", "type": "int", "desc": "Format of BLAST result"}
523	214	{"name": "evalue", "default": "0.001", "type": "float", "desc": "Expected value cutoff"}
524	214	{"name": "task", "default": "'tblastn'", "type": "str", "desc": "('tblastn', 'tblastn-fast')"}
525	215	{"name": "query", "type": "file", "desc": "Nucleotide sequence(s) to search for."}
526	215	{"name": "db", "type": "folder", "desc": "Protein database to search into."}
527	215	{"name": "outfmt", "default": "0", "type": "int", "desc": "Format of BLAST result"}
528	215	{"name": "evalue", "default": "0.001", "type": "float", "desc": "Expected value cutoff"}
529	215	{"name": "task", "default": "'blastx'", "type": "str", "desc": "('blastx', 'blastx-fast')"}
530	216	{"name": "query", "type": "file", "desc": "Nucleotide sequence(s) to search for."}
531	216	{"name": "db", "type": "str", "desc": "Nucleotide database to search into."}
532	216	{"name": "outfmt", "default": "0", "type": "int", "desc": "Format of BLAST result"}
533	216	{"name": "evalue", "default": "0.001", "type": "float", "desc": "Expected value cutoff"}
534	217	{"name": "data", "type": "int[]", "desc": "An array of integers."}
535	218	{"name": "data", "type": "int"}
536	219	{"name": "data", "type": "int[]"}
537	220	{"name": "data", "type": "int[]"}
538	221	{"name": "data", "type": "int[]", "desc": "The X-axis values."}
539	221	{"name": "data2", "type": "int[]", "desc": "The Y-axis values."}
540	222	{"name": "data", "type": "int[]"}
541	223	{"name": "data", "type": "file", "desc": "The fastq file to check quality for."}
542	224	{"name": "data", "type": "int[]"}
543	225	{"name": "data", "type": "int[]", "desc": "The X-axis values."}
544	225	{"name": "data2", "type": "int[]", "desc": "The Y-axis values."}
545	226	{"name": "data", "type": "int[]"}
546	227	{"name": "command", "type": "str"}
547	227	{"name": "input", "type": "file"}
548	227	{"name": "outtype", "default": "fasta", "type": "str"}
549	228	{"name": "data", "type": "file"}
550	228	{"name": "data2", "type": "file"}
551	229	{"name": "data", "type": "file"}
552	230	{"name": "data", "type": "file"}
553	230	{"name": "content", "type": "any"}
554	231	{"name": "data", "type": "folder"}
555	232	{"name": "data", "type": "folder"}
556	233	{"name": "data", "type": "file|folder"}
557	234	{"name": "data", "type": "folder"}
558	235	{"name": "data", "type": "file|folder"}
559	236	{"name": "data", "type": "file|folder"}
560	237	{"name": "data", "type": "file|folder"}
561	238	{"name": "data", "type": "file"}
562	239	{"name": "data", "type": "any"}
563	240	{"name": "data", "type": "str|list"}
564	241	{"name": "start", "default": 1, "type": "int"}
565	241	{"name": "end", "default": 10, "type": "int"}
566	242	{"name": "data", "type": "file", "desc": "File containing tandem duplicates"}
567	243	{"name": "data", "type": "file"}
568	244	{"name": "search str", "type": "str"}
569	244	{"name": "database", "type": "str"}
570	245	{"name": "search str", "type": "str"}
571	245	{"name": "database", "type": "str"}
572	246	{"name": "data", "type": "file", "desc": "data to assess"}
650	247	{"name": "bio_data", "type": "file"}
651	247	{"name": "image_data", "type": "file"}
652	248	{"name": "biodata", "type": "file"}
653	248	{"name": "imgdata", "type": "folder"}
654	248	{"name": "model", "type": "file"}
655	249	{"name": "biodata", "type": "file"}
656	249	{"name": "imgdata", "type": "folder"}
\.


--
-- Data for Name: posts; Type: TABLE DATA; Schema: public; Owner: phenodoop
--

COPY public.posts (id, body, body_html, "timestamp", author_id) FROM stdin;
\.


--
-- Data for Name: returns; Type: TABLE DATA; Schema: public; Owner: phenodoop
--

COPY public.returns (id, service_id, value) FROM stdin;
133	133	{"name": "data", "type": "file"}
134	134	{"name": "data", "type": "file"}
135	135	{"name": "data", "type": "file"}
136	136	{"name": "data", "type": "file[]"}
137	137	{"name": "data", "type": "file[]"}
138	138	{"name": "data", "type": "file"}
139	139	{"name": "data", "type": "file"}
140	140	{"name": "data", "type": "file"}
141	141	{"name": "data", "type": "file"}
142	142	{"name": "data", "type": "file[]"}
143	143	{"name": "data", "type": "folder"}
144	144	{"name": "data", "type": "file"}
145	145	{"name": "data", "type": "file"}
146	146	{"name": "data", "type": "file"}
147	147	{"name": "data", "type": "file"}
148	148	{"name": "data", "type": "file"}
149	149	{"name": "data", "type": "file"}
150	150	{"name": "data", "type": "file"}
151	151	{"name": "data", "type": "file"}
152	152	{"name": "data", "type": "file"}
153	153	{"name": "data", "type": "file"}
154	154	{"name": "data", "type": "file"}
155	155	{"name": "data", "type": "str"}
156	156	{"name": "data", "type": "file"}
157	157	{"name": "data", "type": "file"}
158	158	{"name": "data", "type": "str"}
159	159	{"name": "data", "type": "str"}
160	160	{"name": "data", "type": "str"}
161	161	{"name": "data", "type": "file"}
162	162	{"name": "data", "type": "file"}
163	163	{"name": "data", "type": "str"}
164	164	{"name": "data", "type": "file"}
165	165	{"name": "data", "type": "file"}
166	166	{"name": "data", "type": "file"}
167	167	{"name": "gevo_links", "type": "file"}
168	167	{"name": "condensed_links", "type": "file"}
169	168	{"name": "outputs", "type": "file[]"}
170	169	{"name": "output", "type": "file[]"}
171	170	{"name": "db", "type": "file"}
172	170	{"name": "ks", "type": "file"}
173	171	{"name": "data", "type": "folder", "desc": "The folder with validation statistics files (.mValidated)."}
174	172	{"name": "data", "type": "file", "desc": "The validation statistics."}
175	173	{"name": "data", "type": "file", "desc": "The trained model."}
176	174	{"name": "data", "type": "file|folder"}
177	175	{"name": "data", "type": "file|folder"}
178	176	{"name": "data", "type": "file"}
179	177	{"name": "data", "type": "file|folder"}
180	178	{"name": "data", "type": "file"}
181	179	{"name": "data", "type": "file"}
182	180	{"name": "data", "type": "file"}
183	181	{"name": "data", "type": "file|folder"}
184	182	{"name": "data", "type": "file"}
185	183	{"name": "data", "type": "file"}
186	184	{"name": "data", "type": "file"}
187	185	{"name": "data", "type": "file"}
188	185	{"name": "data", "type": "file"}
189	186	{"name": "data", "type": "file"}
190	187	{"name": "data", "type": "file"}
191	188	{"name": "data", "type": "file"}
192	189	{"name": "data", "type": "file"}
193	190	{"name": "data", "type": "file"}
194	191	{"name": "data", "type": "folder"}
195	192	{"name": "data", "type": "file"}
196	193	{"name": "data", "type": "file"}
197	194	{"name": "data", "type": "file"}
198	195	{"name": "data", "type": "file"}
199	196	{"name": "data", "type": "file"}
200	197	{"name": "data", "type": "file"}
201	198	{"name": "data", "type": "file"}
202	199	{"name": "data", "type": "folder"}
203	200	{"name": "data", "type": "file"}
204	201	{"name": "data", "type": "file[]"}
205	202	{"name": "data", "type": "folder"}
206	203	{"name": "html", "type": "file|folder"}
207	203	{"name": "zip", "type": "file|folder"}
208	204	{"name": "output", "type": "file"}
209	205	{"name": "data", "type": "file"}
210	206	{"name": "data", "type": "file"}
211	207	{"name": "data", "type": "int"}
212	209	{"name": "data", "type": "file"}
213	210	{"name": "map", "type": "file"}
214	211	{"name": "blastdb", "type": "str"}
215	212	{"name": "data", "type": "file"}
216	213	{"name": "data", "type": "file"}
217	214	{"name": "data", "type": "file"}
218	215	{"name": "data", "type": "file"}
219	216	{"name": "data", "type": "file"}
220	217	{"name": "data", "type": "int"}
221	218	{"name": "data", "type": "int"}
222	219	{"name": "data", "type": "int"}
223	220	{"name": "data", "type": "int"}
224	221	{"name": "data", "type": "file"}
225	222	{"name": "data", "type": "int"}
226	223	{"name": "html", "type": "file"}
227	223	{"name": "zip", "type": "file"}
228	224	{"name": "data", "type": "int"}
229	225	{"name": "data", "type": "file"}
230	226	{"name": "data", "type": "int"}
231	227	{"name": "data", "type": "file"}
232	228	{"name": "data", "type": "file"}
233	229	{"name": "data", "type": "byte[]"}
234	231	{"name": "data", "type": "file[]"}
235	232	{"name": "data", "type": "folder[]"}
236	234	{"name": "data", "type": "folder"}
237	235	{"name": "data", "type": "bool"}
238	236	{"name": "data", "type": "str"}
239	237	{"name": "data", "type": "folder"}
240	238	{"name": "data", "type": "str"}
241	240	{"name": "data", "type": "int"}
242	241	{"name": "data", "type": "int[]"}
243	242	{"name": "data", "type": "file"}
244	243	{"name": "data", "type": "file"}
245	244	{"name": "data", "type": "<str,str>"}
246	245	{"name": "data", "type": "file"}
247	246	{"name": "data", "type": "file"}
306	247	{"name": "data", "type": "file"}
307	248	{"name": "data", "type": "file"}
308	249	{"name": "data", "type": "file"}
\.


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: phenodoop
--

COPY public.roles (id, name, "default", permissions) FROM stdin;
1	User	t	15
2	Moderator	f	63
3	Administrator	f	255
\.


--
-- Data for Name: runnableargs; Type: TABLE DATA; Schema: public; Owner: phenodoop
--

COPY public.runnableargs (id, runnable_id, value) FROM stdin;
\.


--
-- Data for Name: runnablereturns; Type: TABLE DATA; Schema: public; Owner: phenodoop
--

COPY public.runnablereturns (id, runnable_id, value) FROM stdin;
\.


--
-- Data for Name: runnables; Type: TABLE DATA; Schema: public; Owner: phenodoop
--

COPY public.runnables (id, workflow_id, user_id, celery_id, status, script, "out", error, view, duration, started_on, created_on, modified_on) FROM stdin;
\.


--
-- Data for Name: serviceaccesses; Type: TABLE DATA; Schema: public; Owner: phenodoop
--

COPY public.serviceaccesses (id, service_id, user_id, rights) FROM stdin;
\.


--
-- Data for Name: services; Type: TABLE DATA; Schema: public; Owner: phenodoop
--

COPY public.services (id, user_id, value, public, active, pipenv, pippkgs, reqfile) FROM stdin;
133	2	{"org": "srlab", "name": "DemuxSingle", "internal": "run_qiime_demux_single", "package": "qiime", "module": "plugins.modules.qiime.adapter", "params": [{"name": "data", "type": "file"}, {"name": "barcode", "type": "file"}, {"name": "barcodeCol", "type": "str"}], "example": "data = qiime.DemuxSingle(data, barcode, barcodeCol)", "desc": "Demultiplex any number of single-end FASTA or a FASTQ files based on a list of barcodes.", "group": "Analysis", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
134	2	{"org": "srlab", "name": "DemuxSummarize", "internal": "run_qiime_demux_summarize", "package": "qiime", "module": "plugins.modules.qiime.adapter", "params": [{"name": "data", "type": "file"}], "example": "visual = qiime.DemuxSummarize(data)", "desc": "Generates a summary of the demultiplexing results.", "group": "Analysis", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
135	2	{"org": "srlab", "name": "Dada2DenoiseSingle", "internal": "run_qiime_dada2_denoise_single", "package": "qiime", "module": "plugins.modules.qiime.adapter", "params": [{"name": "data", "type": "file"}, {"name": "trimleft", "type": "int"}, {"name": "trunclen", "type": "int"}], "example": "data = qiime.Dada2DenoiseSingle(data, trimleft=0, trunclen=120)", "desc": "Detects and corrects Illumina amplicon sequence data.", "group": "Analysis", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
136	2	{"org": "srlab", "name": "DeblurDenoise16S", "internal": "run_qiime_deblur_denoise_16s", "package": "qiime", "module": "plugins.modules.qiime.adapter", "params": [{"name": "data", "type": "file"}, {"name": "trimlen", "type": "int"}], "example": "dataList = qiime.DeblurDenoise16S(data, trimlen=120)", "desc": "Detects and corrects Illumina amplicon sequence data.", "group": "Analysis", "returns": [{"name": "data", "type": "file[]"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
137	2	{"org": "srlab", "name": "FilterQScore", "internal": "run_qiime_quality_qscore", "package": "qiime", "module": "plugins.modules.qiime.adapter", "params": [{"name": "data", "type": "file"}], "example": "dataList = qiime.FilterQScore(data)", "desc": "Applies a quality filtering process based on quality score.", "group": "Analysis", "returns": [{"name": "data", "type": "file[]"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
138	2	{"org": "srlab", "name": "MetadataTabulate", "internal": "run_qiime_metadata_tabulate", "package": "qiime", "module": "plugins.modules.qiime.adapter", "params": [{"name": "data", "type": "file"}], "example": "visual = qiime.MetadataTabulate(data)", "desc": "Generate visualization for summary statistics.", "group": "Analysis", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
139	2	{"org": "srlab", "name": "DeblurVisualizeStats", "internal": "run_qiime_deblur_visualize_stats", "package": "qiime", "module": "plugins.modules.qiime.adapter", "params": [{"name": "data", "type": "file"}], "example": "visual = qiime.DeblurVisualizeStats(data)", "desc": "Generate visualization for summary statistics.", "group": "Analysis", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
140	2	{"org": "srlab", "name": "FeatureTableSummarize", "internal": "run_qiime_feature_table_summarize", "package": "qiime", "module": "plugins.modules.qiime.adapter", "params": [{"name": "data", "type": "file"}, {"name": "metadata", "type": "file"}], "example": "visual = qiime.FeatureTableSummarize(data, metadata)", "desc": "Generate visual summaries of the data.", "group": "Analysis", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
141	2	{"org": "srlab", "name": "FeatureTableTabulate", "internal": "run_qiime_feature_table_tabulate_seqs", "package": "qiime", "module": "plugins.modules.qiime.adapter", "params": [{"name": "data", "type": "file"}], "example": "visual = qiime.FeatureTableTabulate(data)", "desc": "Generate visual summaries of the data.", "group": "Analysis", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
142	2	{"org": "srlab", "name": "PhylogenyTree", "internal": "run_qiime_phylogeny_tree", "package": "qiime", "module": "plugins.modules.qiime.adapter", "params": [{"name": "data", "type": "file"}], "example": "dataList = qiime.PhylogenyTree(data)", "desc": "Generate a phylogenetic tree of the data.", "group": "Analysis", "returns": [{"name": "data", "type": "file[]"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
143	2	{"org": "srlab", "name": "DiversityCoreMetrics", "internal": "run_qiime_diversity_core_metrics", "package": "qiime", "module": "plugins.modules.qiime.adapter", "params": [{"name": "data", "type": "file"}, {"name": "table", "type": "file"}, {"name": "metadata", "type": "file"}, {"name": "sampling", "type": "int", "desc": "The sampling depth"}, {"name": "output", "type": "folder", "desc": "bray_curtis_distance_matrix.qza rarefied_table.qza bray_curtis_emperor.qzv shannon_vector.qza bray_curtis_pcoa_results.qza unweighted_unifrac_distance_matrix.qza evenness_vector.qza unweighted_unifrac_emperor.qzv faith_pd_vector.qza unweighted_unifrac_pcoa_results.qza jaccard_distance_matrix.qza weighted_unifrac_distance_matrix.qza jaccard_emperor.qzv weighted_unifrac_emperor.qzv jaccard_pcoa_results.qza weighted_unifrac_pcoa_results.qza observed_otus_vector.qza"}], "example": "outpath = qiime.DiversityCoreMetrics(data, table, metadata, sampling)", "desc": "Diversity core metrics analysis of phylogenetic tree.", "group": "Analysis", "returns": [{"name": "data", "type": "folder"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
144	2	{"org": "srlab", "name": "DiversityAlpha", "internal": "run_qiime_diversity_alpha_significance", "package": "qiime", "module": "plugins.modules.qiime.adapter", "params": [{"name": "data", "type": "file"}, {"name": "metadata", "type": "file"}, {"name": "output", "type": "file"}], "example": "visual = qiime.DiversityAlpha(data, metadata)", "desc": "Diversity alpha group significance.", "group": "Analysis", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
145	2	{"org": "srlab", "name": "DiversityBeta", "internal": "run_qiime_diversity_beta_significance", "package": "qiime", "module": "plugins.modules.qiime.adapter", "params": [{"name": "data", "type": "file"}, {"name": "metadata", "type": "file"}, {"name": "metadataCol", "type": "str"}, {"name": "output", "type": "file"}], "example": "visual = qiime.DiversityBeta(data, metadata, metaDataCol)", "desc": "Diversity beta group significance.", "group": "Analysis", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
146	2	{"org": "srlab", "name": "EmperorPlot", "internal": "run_qiime_emperor_plot", "package": "qiime", "module": "plugins.modules.qiime.adapter", "params": [{"name": "data", "type": "file"}, {"name": "metadata", "type": "file"}, {"name": "customAxes", "type": "str"}, {"name": "output", "type": "file"}], "example": "visual = qiime.EmperorPlot(data, metadata, customAxes)", "desc": "Explore principal coordinates (PCoA) plots in the context of sample metadata.", "group": "Analysis", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
147	2	{"org": "srlab", "name": "DiversityRarefaction", "internal": "run_qiime_diversity_alpha_rarefaction", "package": "qiime", "module": "plugins.modules.qiime.adapter", "params": [{"name": "data", "type": "file"}, {"name": "metadata", "type": "file"}, {"name": "customAxes", "type": "str"}, {"name": "output", "type": "file"}], "example": "visual = qiime.DiversityRarefaction(data, table, metadata, maxDepth)", "desc": "Explore alpha diversity as a function of sampling depth.", "group": "Analysis", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
148	2	{"org": "srlab", "name": "ClassifierSklearn", "internal": "run_qiime_feature_classifier_classify_sklearn", "package": "qiime", "module": "plugins.modules.qiime.adapter", "params": [{"name": "data", "type": "file"}, {"name": "classifier", "type": "file"}, {"name": "output", "type": "file"}], "example": "data = qiime.ClassifierSklearn(data, classifier)", "desc": "Generate taxonomy from sequence using a pre-trained Naive Bayes classifier.", "group": "Analysis", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
149	2	{"org": "srlab", "name": "TaxaBarPlot", "internal": "run_qiime_taxa_barplot", "package": "qiime", "module": "plugins.modules.qiime.adapter", "params": [{"name": "data", "type": "file"}, {"name": "table", "type": "file"}, {"name": "metadata", "type": "file"}, {"name": "output", "type": "file"}], "example": "visual = qiime.TaxaBarPlot(data, table, metadata)", "desc": "Generate bar plots to view the taxonomic composition of samples interactively.", "group": "Analysis", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
150	2	{"org": "srlab", "name": "FilterSamples", "internal": "run_qiime_feature_table_filter_samples", "package": "qiime", "module": "plugins.modules.qiime.adapter", "params": [{"name": "data", "type": "file"}, {"name": "metadata", "type": "file"}, {"name": "where", "type": "str"}, {"name": "output", "type": "file"}], "example": "data = qiime.FilterSamples(data, metadata, where)", "desc": "Create a feature table that contains specific samples.", "group": "Analysis", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
151	2	{"org": "srlab", "name": "ComposeAddPseudocount", "internal": "run_qiime_composition_add_pseudocount", "package": "qiime", "module": "plugins.modules.qiime.adapter", "params": [{"name": "data", "type": "file"}, {"name": "output", "type": "file"}], "example": "data = qiime.ComposeAddPseudocount(data)", "desc": "Create a composition artifact which is based on frequencies of features on a per-sample basis.", "group": "Analysis", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
152	2	{"org": "srlab", "name": "ComposeAncom", "internal": "run_qiime_composition_ancom", "package": "qiime", "module": "plugins.modules.qiime.adapter", "params": [{"name": "data", "type": "file"}, {"name": "metadata", "type": "file"}, {"name": "metadataCol", "type": "str"}, {"name": "output", "type": "file"}], "example": "visual = qiime.ComposeAncom(data, metadata, metaDataCol)", "desc": "Determine what features differ in abundance across the samples of the two subjects.", "group": "Analysis", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
153	2	{"org": "srlab", "name": "TaxaCollapse", "internal": "run_qiime_taxa_collapse", "package": "qiime", "module": "plugins.modules.qiime.adapter", "params": [{"name": "data", "type": "file"}, {"name": "table", "type": "file"}, {"name": "level", "type": "int"}, {"name": "output", "type": "file"}], "example": "data = qiime.TaxaCollapse(data, table, level)", "desc": "Collapse the features in feature table to perform a differential abundance test at a specific taxonomic level.", "group": "Analysis", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
154	2	{"org": "srlab", "name": "Import", "internal": "run_qiime_import", "package": "qiime", "module": "plugins.modules.qiime.adapter", "params": [{"name": "data", "type": "folder"}, {"name": "data", "type": "str"}], "example": "data = qiime.Import(data, type='EMPSingleEndSequences') # data is the input path for data file(s) and barcode, if needed for the type", "desc": "Import data files into qiime repository type.", "group": "Analysis", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
155	2	{"org": "srlab", "name": "ImportTypes", "internal": "run_qiime_import_types", "package": "qiime", "module": "plugins.modules.qiime.adapter", "params": [], "example": "data = qiime.ImportTypes()", "desc": "Importable types.", "group": "Analysis", "returns": [{"name": "data", "type": "str"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
156	2	{"org": "srlab", "name": "Vsearch", "internal": "run_usearch", "package": "vsearch", "module": "plugins.modules.vsearch.adapter", "params": [{"name": "command", "type": "str"}, {"name": "input", "type": "file"}, {"name": "outtype", "default": "fasta", "type": "str"}], "example": "", "desc": "Open source implementation of USEARCH, an ultra-fast bioinformatics search.", "group": "Search", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
157	2	{"org": "SynMap", "name": "DotPlot", "internal": "run_dotplot", "package": "CoGe", "module": "plugins.modules.dotplot.adapter", "params": [{"name": "dag_file", "type": "file", "desc": "The output file generated by SynMap which includes Ks values"}, {"name": "xhead", "type": "file", "desc": "Header for labels of chromosomes from the genome on x-axis"}, {"name": "yhead", "type": "file", "desc": "Header for labels of chromosomes from the genome on y-axis"}], "example": "", "desc": "Generate a .svg image of a dotplot between two species", "group": "Visualization", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
158	2	{"org": "srlab", "name": "Seqtk", "internal": "run_seqtk", "package": "seqtk", "module": "plugins.modules.seqtk.adapter", "params": [{"name": "data", "type": "file"}, {"name": "command", "type": "str"}], "example": "result = seqtk.Seqtk(data, command)", "desc": "Processing sequences in the FASTA or FASTQ format. https://github.com/lh3/seqtk", "group": "", "returns": [{"name": "data", "type": "str"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
159	2	{"org": "srlab", "name": "FastqToFasta", "internal": "seqtk_fastq_to_fasta", "package": "seqtk", "module": "plugins.modules.seqtk.adapter", "params": [{"name": "data", "type": "file"}], "example": "data = seqtk.FastqToFasta(data)", "desc": "Convert FASTQ to FASTA format. https://github.com/lh3/seqtk", "group": "Convert", "returns": [{"name": "data", "type": "str"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
160	2	{"org": "srlab", "name": "Extract", "internal": "seqtk_extract_sample", "package": "seqtk", "module": "plugins.modules.seqtk.adapter", "params": [{"name": "data", "type": "file"}, {"name": "sample", "type": "int"}, {"name": "seed", "type": "int"}], "example": "sample_file = seqtk.Extract(data)", "desc": "Extracts a random sample. Apply the seed if it's given. 'https://github.com/lh3/seqtk", "group": "Text", "returns": [{"name": "data", "type": "str"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
161	2	{"org": "", "name": "Extract", "internal": "run_extract", "package": "nicad", "module": "plugins.modules.nicad.adapter", "params": [{"name": "data", "type": "folder"}, {"name": "granularity", "default": "'functions'", "type": "str", "desc": "functions|blocks"}, {"name": "language", "default": "'java'", "type": "str", "desc": "'java'|'python'|'c'|'php'"}], "example": "", "desc": "", "group": "Software Analytics", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
162	2	{"org": "SRLAB", "name": "Extract", "internal": "raw_extract", "package": "io", "module": "plugins.modules.common.adapter", "params": [{"name": "data", "type": "file"}, {"name": "lines", "type": "int"}, {"name": "start", "type": "int"}], "example": "data = io.Extract(data)", "desc": "Extract text from a file", "group": "text", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
163	2	{"org": "srlab", "name": "Trim", "internal": "seqtk_trim", "package": "seqtk", "module": "plugins.modules.seqtk.adapter", "params": [{"name": "data", "type": "str"}, {"name": "begin", "type": "int"}, {"name": "end", "type": "int"}, {"name": "quality", "type": "float"}], "example": "trim_file = seqtk.Trim(data)", "desc": "Trim reads with the modified Mott trimming algorithm. https://github.com/lh3/seqtk", "group": "Text", "returns": [{"name": "data", "type": "str"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
164	2	{"org": "srlab", "name": "BlastZ", "internal": "demo_service", "package": "blast", "module": "plugins.modules.blastz.adapter", "params": [{"name": "query", "type": "file", "desc": "Query sequence file in FASTA format"}, {"name": "db", "type": "file", "desc": "Database sequence file in FASTA format"}], "example": "", "desc": "Run LASTZ similar to the BLAST interface, and generates -m8 tabular format", "group": "Alignment", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": "services.html#BlastZ"}	t	t	\N	\N	\N
165	2	{"org": "", "name": "BioMarkers", "internal": "demo_service", "package": "img", "module": "plugins.modules.vizimgflow.adapter", "params": [{"name": "data", "type": "folder"}], "example": "", "desc": "", "group": "Bioinformatics", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
166	2	{"org": "", "name": "BioMarkers", "internal": "demo_service", "package": "bio", "module": "plugins.modules.vizbioflow.adapter", "params": [{"name": "data", "type": "file"}, {"name": "type", "default": "'fasta'", "type": "str"}], "example": "", "desc": "", "group": "Bioinformatics", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
167	2	{"org": "srlab", "name": "GevoLink", "internal": "gevo_link", "package": "CoGe", "module": "plugins.modules.gevolink.adapter", "params": [{"name": "data", "type": "file", "desc": "DAGChainer output file with genomic coordinates converted from gene order to nucleotide positions"}, {"name": "dsgid1", "default": "''", "type": "str", "desc": "CoGe's database id for query genome"}, {"name": "dsgid2", "default": "''", "type": "str", "desc": "CoGe's database id for subject genome"}], "example": "", "desc": "Generate final syntenic gene-set output and condensed syntelog file with GEvo, FeatList, and FastaView links", "group": "SynMap", "returns": [{"name": "gevo_links", "type": "file"}, {"name": "condensed_links", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
168	2	{"org": "", "name": "BlastToRaw", "internal": "demo_service", "package": "blast", "module": "plugins.modules.blasttoraw.adapter", "params": [{"name": "blast", "type": "file", "desc": "Blast file to convert and/or process"}, {"name": "qbed", "type": "file", "desc": "BED file for query sequence"}, {"name": "sbed", "type": "file", "desc": "BED file for query sequence"}, {"name": "tandem_Nmax", "default": "10", "type": "int", "desc": "merge tandem genes within distance"}, {"name": "cscore", "default": "0", "type": "int", "desc": "retain hits that have good bitscore"}], "example": "", "desc": "", "group": "Bioinformatics", "returns": [{"name": "outputs", "type": "file[]"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
169	2	{"org": "srlab", "name": "CutAdapt", "internal": "run_cutadapt", "package": "cutadapt", "module": "plugins.modules.cutadapt.adapter", "params": [{"name": "data", "type": "file"}, {"name": "data2", "default": "''", "type": "file"}, {"name": "adapter", "default": "'CTGTCTCTTATACACATCT'", "type": "str"}, {"name": "min_length", "default": "0", "type": "int", "desc": "Discard reads shorter than LEN"}, {"name": "quality", "default": "20", "type": "int", "desc": "Trim low-quality bases from 5' and/or 3' ends of each read before adapter removal."}], "example": "", "desc": "Finds and removes adapter sequences, primers, poly-A tails and other types of unwanted sequence from high-throughput sequencing reads", "group": "Quality", "returns": [{"name": "output", "type": "file[]"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
170	2	{"org": "", "name": "KSCalc", "internal": "run_kscalc", "package": "CoGe", "module": "plugins.modules.kscalc.adapter", "params": [{"name": "data", "type": "file", "desc": "gcoords file"}], "example": "", "desc": "", "group": "", "returns": [{"name": "db", "type": "file"}, {"name": "ks", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
171	2	{"org": "srlab", "name": "ValidateClone", "internal": "run_validateclone", "package": "nicad", "module": "plugins.modules.clonevalidation.adapter", "params": [{"name": "data", "type": "folder", "desc": "The folder with clone pair files."}, {"name": "model", "type": "file", "desc": "Trained neural network."}, {"name": "language", "default": "'java'", "type": "str", "desc": "The language."}, {"name": "threshold", "default": 0.5, "type": "float", "desc": "The validation threshold."}], "example": "", "desc": "", "group": "", "returns": [{"name": "data", "type": "folder", "desc": "The folder with validation statistics files (.mValidated)."}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
172	2	{"org": "srlab", "name": "ValidateCloneManually", "internal": "run_validateclonemanually", "package": "nicad", "module": "plugins.modules.clonevalidation.adapter", "params": [{"name": "data", "type": "file", "desc": "The clone file."}, {"name": "response", "type": "str", "desc": "The response of manual validation."}, {"name": "fragment1", "type": "file", "desc": "The path of fragment 1."}, {"name": "startline1", "type": "int", "desc": "The start line of fragment 1."}, {"name": "endline1", "type": "int", "desc": "The end line of fragment 1."}, {"name": "fragment2", "type": "file", "desc": "The path of fragment 2."}, {"name": "startLine2", "type": "int", "desc": "The start line of fragment 2."}, {"name": "endLine2", "type": "int", "desc": "The end line of fragment 2."}], "example": "", "desc": "", "group": "", "returns": [{"name": "data", "type": "file", "desc": "The validation statistics."}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
173	2	{"org": "srlab", "name": "TrainModel", "internal": "run_trainmodel", "package": "nicad", "module": "plugins.modules.clonevalidation.adapter", "params": [{"name": "data", "type": "file", "desc": "The training dataset in csv file."}], "example": "", "desc": "Training on new dataset.", "group": "Software Analytics", "returns": [{"name": "data", "type": "file", "desc": "The trained model."}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
174	2	{"org": "srlab", "name": "Align", "internal": "run_bowtie2", "package": "bowtie2", "module": "plugins.modules.bowtie2.adapter", "params": [{"name": "ref", "type": "file", "desc": "The reference genome."}, {"name": "data", "type": "file|folder", "desc": "If it is a folder name, all .fastq and .fq files are recursively collected from that folder."}, {"name": "data2", "default": "''", "type": "file|folder", "desc": "Reverse seq for pair-end read. If it is a folder, all .fastq and .fq files are recursively collected."}], "example": "data = bowtie2.Align(ref, data, data2='') #if data2 is empty then single read; otherwise pair-read", "desc": "Align sequencing reads to long reference sequences using bowtie2 algorithm.", "group": "Alignment", "returns": [{"name": "data", "type": "file|folder"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
175	2	{"org": "srlab", "name": "Align", "internal": "run_bwa", "package": "bwa", "module": "plugins.modules.bwa.adapter", "params": [{"name": "ref", "type": "file", "desc": "the reference genome."}, {"name": "data", "type": "file|folder", "desc": "Seq file for single read, forward seq file for pair-end. If folder, all .fastq/.fq files are recursively collected from that folder."}, {"name": "data2", "default": "''", "type": "file|folder", "desc": "Reverse seq file for pair-end. If folder, all .fastq/.fq files are recursively collected from that folder."}], "example": "data = bwa.Align(ref, data, data2='', index='') #single-read. Give valid data2 value for pair-read.", "desc": "Map with BWA. Mapping low-divergent sequences against a large reference genome, such as the human genome and is designed for Illumina sequence reads up to 100bp.", "group": "Alignment", "returns": [{"name": "data", "type": "file|folder"}], "access": 0, "sharedusers": [], "href": "services.html#bwa-align"}	t	t	\N	\N	\N
176	2	{"org": "srlab", "name": "Txl", "internal": "run_txl", "package": "txl", "module": "plugins.modules.txl.adapter", "params": [{"name": "data", "type": "file"}, {"name": "txlfile", "default": "''", "type": "file"}], "example": "", "desc": "The txl command invokes the TXL interpreter to compile, load and execute a TXL program on an input file. Transformed output (only) is saved in an output file.", "group": "Software Analytics", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
177	2	{"org": "srlab", "name": "Merge", "internal": "run_pear", "package": "pear", "module": "plugins.modules.pear.adapter", "params": [{"name": "data", "type": "file|folder", "desc": "forward fastq file"}, {"name": "data2", "type": "file|folder", "desc": "reverse fastq file"}], "example": "data = pear.Merge(data, data2)", "desc": "Pair-end read merger for fastq files. It evaluates all possible paired-end read overlaps. In addition, it implements a statistical test for minimizing false-positive results.", "group": "Analysis", "returns": [{"name": "data", "type": "file|folder"}], "access": 0, "sharedusers": [], "href": "services.html#pear-merge"}	t	t	\N	\N	\N
178	2	{"org": "srlab", "name": "Merge", "internal": "run_flash", "package": "flash", "module": "plugins.modules.flash.adapter", "params": [{"name": "data", "type": "str", "desc": "forward fastq file"}, {"name": "data2", "type": "str", "desc": "reverse fastq file"}, {"name": "max_overlap", "default": 50, "type": "int"}], "example": "data = flash.Merge(data, data2)", "desc": "Merge mates from fragments that are shorter than twice the read length.", "group": "Analysis", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
179	2	{"org": "srlab", "name": "DAGFormatter", "internal": "demo_service", "package": "CoGe", "module": "plugins.modules.dagformatter.adapter", "params": [{"name": "blast_file", "type": "file", "desc": "BLAST file to format"}, {"name": "query", "default": "'a'", "type": "str", "desc": "the name of the query organism"}, {"name": "subject", "default": "'b'", "type": "str", "desc": "the name of the subject organism"}], "example": "", "desc": "Prepare BLAST file for DAGChainer", "group": "SynMap", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
180	2	{"org": "srlab", "name": "DagChainer", "internal": "dag_chainer", "package": "CoGe", "module": "plugins.modules.dagchainer.adapter", "params": [{"name": "dag", "type": "file", "desc": "dag file with format a_seqid<tab>a_accn<tab>a_start<tab>a_end<tab>b_seqid<tab>b_accn<tab>b_start<tab>b_end<tab>e-value"}, {"name": "gap_init", "default": "0", "type": "int", "desc": "gap open penalty"}, {"name": "gap_extend", "default": "-3", "type": "int", "desc": "gap extension penalty"}, {"name": "min_score", "default": "0", "type": "int", "desc": "minimum alignment score"}, {"name": "gap_dist", "default": "10.0", "type": "float", "desc": "average distance expected between 2 syntenic genes"}, {"name": "gap_max", "default": "20.0", "type": "float", "desc": "maximum distance between 2 matches"}, {"name": "e_value", "default": "0.05", "type": "float", "desc": "maximum e-value"}, {"name": "min_aligned_pairs", "default": "5", "type": "int", "desc": "minimum number of pairs to be considered a diagonal"}], "example": "", "desc": "Algorithm to identify syntenic regions between genomes", "group": "SynMap", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
181	2	{"org": "srlab", "name": "SamToBam", "internal": "run_sam_to_bam", "package": "pysam", "module": "plugins.modules.pysam.adapter", "params": [{"name": "data", "type": "file", "desc": "sam file"}, {"name": "output", "type": "file", "desc": "[optional]. A .bam file."}], "example": "data = pysam.SamToBam(data)", "desc": "Converts SAM data format to BAM binary data format.", "group": "Convert", "returns": [{"name": "data", "type": "file|folder"}], "access": 0, "sharedusers": [], "href": "services.html#pysam-samtobam"}	t	t	\N	\N	\N
182	2	{"org": "iselab", "name": "RMDUP", "internal": "run_rmdup", "package": "iselab", "module": "plugins.modules.samtools.adapter", "params": [{"name": "data", "type": "file", "desc": "input bam file"}], "example": "", "desc": "", "group": "", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
183	2	{"org": "srlab", "name": "MergeBam", "internal": "run_samtools_merge", "package": "samtools", "module": "plugins.modules.samtools.adapter", "params": [{"name": "data", "type": "file"}, {"name": "data2", "type": "file"}], "example": "data = samtools.MergeBam(data, data2) # add more .bam files if needed", "desc": ".bam file merger.", "group": "Analysis", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": "services.html#samtools-merge"}	t	t	\N	\N	\N
184	2	{"org": "srlab", "name": "NiCad", "internal": "run_nicad", "package": "nicad", "module": "plugins.modules.nicad.adapter", "params": [{"name": "data", "type": "folder"}, {"name": "granularity", "default": "'functions'", "type": "str"}, {"name": "language", "default": "'java'", "type": "str"}], "example": "", "desc": "Automated Detection of Near-Miss Intentional Clones. This tool will modify the parent of the source folder. Copy the source folder to a temporary folder and use it as data, if you do not want to modify its parent. For example, data = context.copyto(data, context.createoutdir(), '.git')", "group": "Software Analytics", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
185	2	{"org": "srlab", "name": "NiCadCross", "internal": "run_nicadcross", "package": "nicad", "module": "plugins.modules.nicad.adapter", "params": [{"name": "data", "type": "folder"}, {"name": "data2", "type": "folder"}, {"name": "granularity", "default": "'functions'", "type": "str"}, {"name": "language", "default": "'java'", "type": "str"}], "example": "", "desc": "Automated Detection of Near-Miss Intentional Clones. It does an cross-system test - that is, given two systems s1 and s2, it reports only clones of fragments of s1 in s2.  This is useful in incremental clone detection for new versions, or for detecting clones between two systems to be checked for cross-cloning.", "group": "Software Analytics", "returns": [{"name": "data", "type": "file"}, {"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
186	2	{"org": "", "name": "Abstract", "internal": "run_abstract", "package": "nicad", "module": "plugins.modules.nicad.adapter", "params": [{"name": "data", "type": "file"}, {"name": "granularity", "default": "'functions'", "type": "str", "desc": "functions|blocks"}, {"name": "language", "default": "'java'", "type": "str", "desc": "'java'|'cs'|'python'|'c'|'php'"}, {"name": "nonterminals", "default": "'none'", "type": "str", "desc": "'none'|'condition'|'expression'"}], "example": "", "desc": "", "group": "Software Analytics", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
187	2	{"org": "", "name": "Filter", "internal": "run_filter", "package": "nicad", "module": "plugins.modules.nicad.adapter", "params": [{"name": "data", "type": "file"}, {"name": "granularity", "default": "'functions'", "type": "str", "desc": "'functions'|'blocks'"}, {"name": "language", "default": "'java'", "type": "str", "desc": "'java'|'cs'|'python'|'c'|php'"}, {"name": "nonterminals", "default": "'none'", "type": "str", "desc": "'none'|'declaration'"}], "example": "", "desc": "", "group": "Software Analytics", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
188	2	{"org": "", "name": "Transform", "internal": "run_transform", "package": "nicad", "module": "plugins.modules.nicad.adapter", "params": [{"name": "data", "type": "file"}, {"name": "granularity", "default": "'functions'", "type": "str", "desc": "'functions'|'blocks'"}, {"name": "language", "default": "'java'", "type": "str", "desc": "'java'|'cs'|'python'|'c'|'php'"}, {"name": "transform", "default": "'none'", "type": "str", "desc": "'none'|'sort'"}], "example": "", "desc": "", "group": "Software Analytics", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
189	2	{"org": "", "name": "Rename", "internal": "run_rename", "package": "nicad", "module": "plugins.modules.nicad.adapter", "params": [{"name": "data", "type": "file"}, {"name": "granularity", "default": "'functions'", "type": "str", "desc": "'functions'|'blocks'"}, {"name": "language", "default": "'java'", "type": "str", "desc": "'java'|'cs'|'python'|'c'|'php'"}, {"name": "renaming", "default": "'blind'", "type": "str", "desc": "'none'|'blind'|'consistent'"}], "example": "", "desc": "", "group": "Software Analytics", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
190	2	{"org": "", "name": "Normalize", "internal": "run_normalize", "package": "nicad", "module": "plugins.modules.nicad.adapter", "params": [{"name": "data", "type": "file"}, {"name": "granularity", "default": "'functions'", "type": "str", "desc": "'functions'|'blocks'"}, {"name": "language", "default": "'java'", "type": "str", "desc": "'java'|'cs'|'python'|'c'|'php'"}, {"name": "normalizer", "default": "'java-normalize-ifconditions-functions'", "type": "str", "desc": "'none'|'java-normalize-ifconditions-functions'|'xmlsortblocks'|'cabstractifconditions'"}], "example": "", "desc": "", "group": "Software Analytics", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
191	2	{"org": "", "name": "CleanAll", "internal": "run_cleanall", "package": "nicad", "module": "plugins.modules.nicad.adapter", "params": [{"name": "data", "type": "folder"}], "example": "", "desc": "", "group": "Software Analytics", "returns": [{"name": "data", "type": "folder"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
192	2	{"org": "", "name": "FindClones", "internal": "run_findclones", "package": "nicad", "module": "plugins.modules.nicad.adapter", "params": [{"name": "data", "type": "file"}, {"name": "threshold", "default": 0.3, "type": "float"}, {"name": "minclonesize", "default": "10", "type": "int"}, {"name": "maxclonesize", "default": "2500", "type": "int"}, {"name": "showsource", "type": "str", "desc": "showsource|none"}], "example": "", "desc": "", "group": "Software Analytics", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
193	2	{"org": "", "name": "FindClonePairs", "internal": "run_findclonepairs", "package": "nicad", "module": "plugins.modules.nicad.adapter", "params": [{"name": "data", "type": "file"}, {"name": "threshold", "default": "0.3", "type": "float"}, {"name": "minclonesize", "default": "10", "type": "int"}, {"name": "maxclonesize", "default": "2500", "type": "int"}, {"name": "showsource", "type": "str", "desc": "showsource"}], "example": "", "desc": "", "group": "Software Analytics", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
194	2	{"org": "", "name": "FindClonePairs", "internal": "run_findclonepairs", "package": "demo", "module": "plugins.modules.demos.dockerexec.adapter", "params": [{"name": "data", "type": "file"}, {"name": "threshold", "default": "0.3", "type": "float"}, {"name": "minclonesize", "default": "10", "type": "int"}, {"name": "maxclonesize", "default": "2500", "type": "int"}, {"name": "showsource", "type": "str", "desc": "showsource"}], "example": "", "desc": "", "group": "Software Analytics", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
195	2	{"org": "", "name": "ClusterPairs", "internal": "run_clusterpairs", "package": "nicad", "module": "plugins.modules.nicad.adapter", "params": [{"name": "data", "type": "file"}], "example": "", "desc": "", "group": "Software Analytics", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
196	2	{"org": "", "name": "GetSource", "internal": "run_getsource", "package": "nicad", "module": "plugins.modules.nicad.adapter", "params": [{"name": "data", "type": "file"}], "example": "", "desc": "", "group": "Software Analytics", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
197	2	{"org": "", "name": "GetNormSource", "internal": "run_getnormsource", "package": "nicad", "module": "plugins.modules.nicad.adapter", "params": [{"name": "data", "type": "file", "desc": "The extracted functions or blocks in xml"}, {"name": "data2", "type": "file", "desc": "The clones in xml"}], "example": "", "desc": "", "group": "Software Analytics", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
198	2	{"org": "", "name": "MakePairHTML", "internal": "run_makepairhtml", "package": "nicad", "module": "plugins.modules.nicad.adapter", "params": [{"name": "data", "type": "file", "desc": "Clone source file in xml."}], "example": "", "desc": "", "group": "Software Analytics", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
199	2	{"org": "", "name": "SplitClasses", "internal": "run_splitclasses", "package": "nicad", "module": "plugins.modules.nicad.adapter", "params": [{"name": "data", "type": "file", "desc": "Clone source file in xml."}], "example": "", "desc": "", "group": "Software Analytics", "returns": [{"name": "data", "type": "folder"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
200	2	{"org": "srlab", "name": "PycoQC", "internal": "demo_service", "package": "pycoqc", "module": "plugins.modules.pycoqc.adapter", "params": [{"name": "data", "type": "file", "desc": "basecalled nanopore reads or summary files generated by the basecallers Albacore, Guppy or MinKNOW"}], "example": "", "desc": "Data visualisation and quality control tool for nanopore data", "group": "Visualization", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
201	2	{"org": "srlab", "name": "Blast2Bed", "internal": "demo_service", "package": "blast", "module": "plugins.modules.blast2bed.adapter", "params": [{"name": "data", "type": "file", "desc": "BLAST file to convert to BED"}], "example": "", "desc": "Convert a tabular blast output to a BED file", "group": "Bioinformatics", "returns": [{"name": "data", "type": "file[]"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
202	2	{"org": "", "name": "GitClone", "internal": "run_gitclone", "package": "git", "module": "plugins.modules.git.adapter", "params": [{"name": "url", "type": "str", "desc": "The repository path"}, {"name": "data", "type": "folder", "desc": "The local path"}], "example": "", "desc": "", "group": "", "returns": [{"name": "data", "type": "folder"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
203	2	{"org": "srlab", "name": "CheckQuality", "internal": "run_fastqc", "package": "fastqc", "module": "plugins.modules.fastqc.adapter", "params": [{"name": "data", "type": "file|folder", "desc": "if folder, all .fastq and .fq files are recursively collected from that folder."}], "example": "html, zip = fastqc.CheckQuality(data)", "desc": "Measure the quality of a fastq file using fastqc tool.", "group": "Quality", "returns": [{"name": "html", "type": "file|folder"}, {"name": "zip", "type": "file|folder"}], "access": 0, "sharedusers": [], "href": "services.html#fastqc-CheckQuality"}	t	t	\N	\N	\N
204	2	{"org": "srlab", "name": "GeneOrder", "internal": "gene_order", "package": "CoGe", "module": "plugins.modules.geneorder.adapter", "params": [{"name": "input", "type": "file", "desc": "dag file to be ordered"}, {"name": "gid1", "default": "''", "type": "str", "desc": "first genome id"}, {"name": "gid2", "default": "''", "type": "str", "desc": "second genome id"}, {"name": "feature1", "default": "'CDS'", "type": "str", "desc": "feature of first genome"}, {"name": "feature2", "default": "'CDS'", "type": "str", "desc": "feature of second genome"}], "example": "", "desc": "Reorders the genes contained in the dag file by ascending order", "group": "SynMap", "returns": [{"name": "output", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
205	2	{"org": "multiqc", "name": "MultiQC", "internal": "demo_service", "package": "fastqc", "module": "plugins.modules.multiqc.adapter", "params": [{"name": "data", "type": "file[]"}], "example": "", "desc": "Compare multiple FastQC files and generate one report", "group": "Quality", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
206	2	{"org": "srlab", "name": "MergeR", "internal": "run_flash_recursive", "package": "flash", "module": "plugins.modules.flash.adapter", "params": [{"name": "data", "type": "str"}, {"name": "max_overlap", "default": 50, "type": "int"}], "example": "mergedDir = MergeR(indir)", "desc": "Merge mates from fragments that are shorter than twice the read length.", "group": "Analysis", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
207	2	{"org": "", "name": "DemoService", "internal": "demo_service", "package": "", "module": "plugins.modules.demo.adapter", "params": [{"name": "data", "type": "int"}], "example": "", "desc": "", "group": "", "returns": [{"name": "data", "type": "int"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
208	2	{"org": "srlab", "name": "Workflow", "internal": "run_workflow", "package": "system", "module": "plugins.modules.workflow.adapter", "params": [{"name": "id", "type": "int", "desc": "Workflow ID."}], "example": "returnvals = system.Workflow(id)", "desc": "Run a subworkflow.", "group": "Quality", "returns": [], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
209	2	{"org": "srlab", "name": "Last", "internal": "run_last", "package": "CoGe", "module": "plugins.modules.last.adapter", "params": [{"name": "data", "type": "file", "desc": "Query sequence to search for"}, {"name": "data2", "type": "file", "desc": "Subject sequence to search against"}], "example": "", "desc": "Blast query sequence against LastDB using Last algorithm", "group": "SynMap", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
210	2	{"org": "", "name": "reDOTable", "internal": "demo_service", "package": "redotable", "module": "plugins.modules.redotable.adapter", "params": [{"name": "x_seq", "type": "file"}, {"name": "y_seq", "type": "file"}], "example": "", "desc": "", "group": "", "returns": [{"name": "map", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
211	2	{"org": "srlab", "name": "CreateBlastDB", "internal": "run_makeblastdb", "package": "blast", "module": "plugins.modules.blast.adapter", "params": [{"name": "data", "type": "file", "desc": "Multi-FASTA file of sequences to create database from"}, {"name": "dbtype", "default": "'nucl'", "type": "str", "desc": "Molecule type ('nucl', 'prot')"}], "example": "", "desc": "Create a custom database from a multi-FASTA file of sequences", "group": "Alignment", "returns": [{"name": "blastdb", "type": "str"}], "access": 0, "sharedusers": [], "href": "services.html#CreateBlastDB"}	t	t	\N	\N	\N
212	2	{"org": "srlab", "name": "BlastN", "internal": "run_blastn", "package": "blast", "module": "plugins.modules.blast.adapter", "params": [{"name": "query", "type": "file", "desc": "Nucleotide sequence(s) to search for."}, {"name": "db", "type": "str", "desc": "Nucleotide database to search into."}, {"name": "outfmt", "default": "0", "type": "int", "desc": "Format of BLAST result"}, {"name": "evalue", "default": "0.001", "type": "float", "desc": "Expected value cutoff"}, {"name": "task", "default": "'blastn'", "type": "str", "desc": "('blastn', 'blastn-short', 'dc-megablast', 'megablast', 'rmblastn')"}], "example": "", "desc": "Search a nucleotide database using a nucleotide query.", "group": "Alignment", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": "services.html#BlastN"}	t	t	\N	\N	\N
213	2	{"org": "srlab", "name": "BlastP", "internal": "run_blastp", "package": "blast", "module": "plugins.modules.blast.adapter", "params": [{"name": "query", "type": "file", "desc": "Protein sequence(s) to search for."}, {"name": "db", "type": "str", "desc": "Protein database to search into."}, {"name": "outfmt", "default": "0", "type": "int", "desc": "Format of BLAST result"}, {"name": "evalue", "default": "0.001", "type": "float", "desc": "Expected value cutoff"}, {"name": "task", "default": "'blastp'", "type": "str", "desc": "('blastp', 'blastp-fast', 'blastp-short')"}], "example": "", "desc": "Search protein database using a protein query.", "group": "Alignment", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": "services.html#BlastP"}	t	t	\N	\N	\N
214	2	{"org": "srlab", "name": "tBlastN", "internal": "run_tblastn", "package": "blast", "module": "plugins.modules.blast.adapter", "params": [{"name": "query", "type": "file", "desc": "Protein sequence(s) to search for."}, {"name": "db", "type": "str", "desc": "Nucleotide database to search into."}, {"name": "outfmt", "default": "0", "type": "int", "desc": "Format of BLAST result"}, {"name": "evalue", "default": "0.001", "type": "float", "desc": "Expected value cutoff"}, {"name": "task", "default": "'tblastn'", "type": "str", "desc": "('tblastn', 'tblastn-fast')"}], "example": "", "desc": "Search translated nucleotide database using a protein query.", "group": "Alignment", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": "services.html#tBlastN"}	t	t	\N	\N	\N
215	2	{"org": "srlab", "name": "BlastX", "internal": "run_blastx", "package": "blast", "module": "plugins.modules.blast.adapter", "params": [{"name": "query", "type": "file", "desc": "Nucleotide sequence(s) to search for."}, {"name": "db", "type": "folder", "desc": "Protein database to search into."}, {"name": "outfmt", "default": "0", "type": "int", "desc": "Format of BLAST result"}, {"name": "evalue", "default": "0.001", "type": "float", "desc": "Expected value cutoff"}, {"name": "task", "default": "'blastx'", "type": "str", "desc": "('blastx', 'blastx-fast')"}], "example": "", "desc": "Search protein database using a translated nucleotide query.", "group": "Alignment", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": "services.html#BlastX"}	t	t	\N	\N	\N
216	2	{"org": "srlab", "name": "tBlastX", "internal": "run_tblastx", "package": "blast", "module": "plugins.modules.blast.adapter", "params": [{"name": "query", "type": "file", "desc": "Nucleotide sequence(s) to search for."}, {"name": "db", "type": "str", "desc": "Nucleotide database to search into."}, {"name": "outfmt", "default": "0", "type": "int", "desc": "Format of BLAST result"}, {"name": "evalue", "default": "0.001", "type": "float", "desc": "Expected value cutoff"}], "example": "", "desc": "Translate query and database nucleotide sequences and blast them as proteins.", "group": "Alignment", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": "services.html#tBlastX"}	t	t	\N	\N	\N
217	2	{"org": "", "name": "SumInFunction", "internal": "demo_service", "package": "demo", "module": "plugins.modules.demos.function.adapter", "params": [{"name": "data", "type": "int[]", "desc": "An array of integers."}], "example": "", "desc": "Takes an array of integers as arguments and adapter calls sum python function.", "group": "", "returns": [{"name": "data", "type": "int"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
218	2	{"org": "", "name": "Identity", "internal": "demo_service", "package": "demo", "module": "plugins.modules.demos.adapter.adapter", "params": [{"name": "data", "type": "int"}], "example": "", "desc": "Takes an integer argument and returns it.", "group": "", "returns": [{"name": "data", "type": "int"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
219	2	{"org": "", "name": "SumInBashScript", "internal": "demo_service", "package": "demo", "module": "plugins.modules.demos.shellscript.adapter", "params": [{"name": "data", "type": "int[]"}], "example": "", "desc": "A bash script calculates the sum. You can call other program from the bash script.", "group": "", "returns": [{"name": "data", "type": "int"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
220	2	{"org": "", "name": "SumInNewVenv", "internal": "demo_service", "package": "demo", "module": "plugins.modules.demos.newvenvprogram.adapter", "params": [{"name": "data", "type": "int[]"}], "example": "", "desc": "A bash script first sets the python venv and then calls a python program.", "group": "", "returns": [{"name": "data", "type": "int"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
221	2	{"org": "", "name": "ChartTest2", "internal": "demo_service", "package": "demo", "module": "plugins.modules.demos.pipinstallreqfile.adapter", "params": [{"name": "data", "type": "int[]", "desc": "The X-axis values."}, {"name": "data2", "type": "int[]", "desc": "The Y-axis values."}], "example": "", "desc": "", "group": "", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
222	2	{"org": "", "name": "SumInVenv", "internal": "demo_service", "package": "demo", "module": "plugins.modules.demos.venvprogram.adapter", "params": [{"name": "data", "type": "int[]"}], "example": "", "desc": "A bash script first sets the python venv and then calls a python program.", "group": "", "returns": [{"name": "data", "type": "int"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
223	2	{"org": "", "name": "CheckQualityEx", "internal": "demo_service", "package": "demo", "module": "plugins.modules.demos.java.adapter", "params": [{"name": "data", "type": "file", "desc": "The fastq file to check quality for."}], "example": "", "desc": "Measure the quality of a fastq file using fastqc tool. Adapter calls the fastqc java program.", "group": "", "returns": [{"name": "html", "type": "file"}, {"name": "zip", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
224	2	{"org": "", "name": "SumInModule", "internal": "demo_service", "package": "demo", "module": "plugins.modules.demos.module.adapter", "params": [{"name": "data", "type": "int[]"}], "example": "", "desc": "A python module is called by adapter.", "group": "", "returns": [{"name": "data", "type": "int"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
225	2	{"org": "", "name": "ChartTest", "internal": "demo_service", "package": "demo", "module": "plugins.modules.demos.pipinstall.adapter", "params": [{"name": "data", "type": "int[]", "desc": "The X-axis values."}, {"name": "data2", "type": "int[]", "desc": "The Y-axis values."}], "example": "", "desc": "", "group": "", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
226	2	{"org": "", "name": "SumInProgram", "internal": "demo_service", "package": "demo", "module": "plugins.modules.demos.program.adapter", "params": [{"name": "data", "type": "int[]"}], "example": "", "desc": "A python program is called by adapter.", "group": "", "returns": [{"name": "data", "type": "int"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
227	2	{"org": "srlab", "name": "Usearch", "internal": "run_usearch", "package": "usearch", "module": "plugins.modules.usearch.adapter", "params": [{"name": "command", "type": "str"}, {"name": "input", "type": "file"}, {"name": "outtype", "default": "fasta", "type": "str"}], "example": "", "desc": "Ultra-fast bioinformatics search.", "group": "Search", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
228	2	{"org": "", "name": "JoinPath", "internal": "raw_joinpath", "package": "", "module": "plugins.modules.common.adapter", "params": [{"name": "data", "type": "file"}, {"name": "data2", "type": "file"}], "example": "", "desc": "", "group": "", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
229	2	{"org": "SRLAB", "name": "Read", "internal": "raw_read", "package": "io", "module": "plugins.modules.common.adapter", "params": [{"name": "data", "type": "file"}], "example": "data = Read(data)", "desc": "Reads a file as bytes.", "group": "system", "returns": [{"name": "data", "type": "byte[]"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
230	2	{"org": "SRLAB", "name": "Write", "internal": "raw_write", "package": "io", "module": "plugins.modules.common.adapter", "params": [{"name": "data", "type": "file"}, {"name": "content", "type": "any"}], "example": "Write(data, 'Text to write')", "desc": "Writes text data to a file.", "group": "system", "returns": [], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
231	2	{"org": "SRLAB", "name": "GetFiles", "internal": "raw_get_files", "package": "io", "module": "plugins.modules.common.adapter", "params": [{"name": "data", "type": "folder"}], "example": "files = GetFiles(data)", "desc": "Gets the names of files in a directory.", "group": "system", "returns": [{"name": "data", "type": "file[]"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
232	2	{"org": "SRLAB", "name": "GetFolders", "internal": "raw_get_folders", "package": "io", "module": "plugins.modules.common.adapter", "params": [{"name": "data", "type": "folder"}], "example": "folders = GetFolders(data)", "desc": "Gets the names of folders in a directory.", "group": "system", "returns": [{"name": "data", "type": "folder[]"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
233	2	{"org": "SRLAB", "name": "Remove", "internal": "raw_remove", "package": "io", "module": "plugins.modules.common.adapter", "params": [{"name": "data", "type": "file|folder"}], "example": "Remove(data)", "desc": "Removes a file or directory.", "group": "system", "returns": [], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
234	2	{"org": "SRLAB", "name": "CreateFolder", "internal": "raw_makedirs", "package": "io", "module": "plugins.modules.common.adapter", "params": [{"name": "data", "type": "folder"}], "example": "folder = CreateFolder(data)", "desc": "Creates a directory.", "group": "system", "returns": [{"name": "data", "type": "folder"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
235	2	{"org": "SRLAB", "name": "isfile", "internal": "raw_isfile", "package": "io", "module": "plugins.modules.common.adapter", "params": [{"name": "data", "type": "file|folder"}], "example": "isfile(data)", "desc": "Returns true if a specified path is a file; false if it's a directory.", "group": "system", "returns": [{"name": "data", "type": "bool"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
236	2	{"org": "SRLAB", "name": "basename", "internal": "raw_basename", "package": "io", "module": "plugins.modules.common.adapter", "params": [{"name": "data", "type": "file|folder"}], "example": "data = basename(data)", "desc": "Truncates the path and returns only the filename.", "group": "system", "returns": [{"name": "data", "type": "str"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
237	2	{"org": "SRLAB", "name": "dirname", "internal": "raw_dirname", "package": "io", "module": "plugins.modules.common.adapter", "params": [{"name": "data", "type": "file|folder"}], "example": "dirname(data)", "desc": "Truncates the file name and returns only the directory name.", "group": "system", "returns": [{"name": "data", "type": "folder"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
238	2	{"org": "SRLAB", "name": "GetDataType", "internal": "raw_getdatatype", "package": "io", "module": "plugins.modules.common.adapter", "params": [{"name": "data", "type": "file"}], "example": "datatype = GetDataType(data)", "desc": "Gets the datatype of a file", "group": "Convert", "returns": [{"name": "data", "type": "str"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
239	2	{"org": "Python", "name": "print", "internal": "raw_print", "package": "Python", "module": "plugins.modules.common.adapter", "params": [{"name": "data", "type": "any"}], "example": "print(data)", "desc": "Prints one or more things.", "group": "system", "returns": [], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
240	2	{"org": "Python", "name": "len", "internal": "raw_len", "package": "Python", "module": "plugins.modules.common.adapter", "params": [{"name": "data", "type": "str|list"}], "example": "len(data)", "desc": "Gets length of a list or str.", "group": "system", "returns": [{"name": "data", "type": "int"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
241	2	{"org": "Python", "name": "range", "internal": "raw_range", "package": "Python", "module": "plugins.modules.common.adapter", "params": [{"name": "start", "default": 1, "type": "int"}, {"name": "end", "default": 10, "type": "int"}], "example": "range(1, 10)", "desc": "Generates a range of numbers.", "group": "system", "returns": [{"name": "data", "type": "int[]"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
242	2	{"org": "srlab", "name": "ProcessDups", "internal": "process_dups", "package": "CoGe", "module": "plugins.modules.processdups.adapter", "params": [{"name": "data", "type": "file", "desc": "File containing tandem duplicates"}], "example": "", "desc": "Read in a file containing tandem duplicates and generate CoGe links to FeatList, GEvo, and FastaView for further analysis", "group": "SynMap", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
243	2	{"org": "srlab", "name": "NanoPlot", "internal": "demo_service", "package": "nanoplot", "module": "plugins.modules.nanoplot.adapter", "params": [{"name": "data", "type": "file"}], "example": "", "desc": "Plotting tool for long read sequencing data and alignments", "group": "Visualization", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
244	2	{"org": "srlab", "name": "SearchEntrez", "internal": "run_search_entrez", "package": "biopython", "module": "plugins.modules.biopython.adapter", "params": [{"name": "search str", "type": "str"}, {"name": "database", "type": "str"}], "example": "SearchEntrez('Myb AND txid3702[ORGN] AND 0:6000[SLEN]', 'nucleotide')", "desc": "Get information with a search str", "group": "Search", "returns": [{"name": "data", "type": "<str,str>"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
245	2	{"org": "srlab", "name": "DownloadBySearch", "internal": "run_search_and_download", "package": "biopython", "module": "plugins.modules.biopython.adapter", "params": [{"name": "search str", "type": "str"}, {"name": "database", "type": "str"}], "example": "DownloadBySearch('Myb AND txid3702[ORGN] AND 0:6000[SLEN]', 'nucleotide')", "desc": "Search and download", "group": "Search", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
246	2	{"org": "srlab", "name": "FastQE", "internal": "demo_service", "package": "fastqc", "module": "plugins.modules.fastqe.adapter", "params": [{"name": "data", "type": "file", "desc": "data to assess"}], "example": "", "desc": "Read one or more FASTQ files, fastqe will compute quality stats for each file and print those stats as emoji", "group": "Quality", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
247	2	{"org": "", "name": "ClassifyCloneMarker", "internal": "demo_service", "package": "ml", "module": "plugins.modules.vizmlflow.ccdml.adapter", "params": [{"name": "bio_data", "type": "file"}, {"name": "image_data", "type": "file"}], "example": "", "desc": "", "group": "Clone", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
248	2	{"org": "", "name": "PredictBioMarker", "internal": "demo_service", "package": "ml", "module": "plugins.modules.vizmlflow.bioml.adapter", "params": [{"name": "biodata", "type": "file"}, {"name": "imgdata", "type": "folder"}, {"name": "model", "type": "file"}], "example": "", "desc": "", "group": "Bioinformatics", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
249	2	{"org": "", "name": "ClassifyBioMarker", "internal": "demo_service_classifier", "package": "ml", "module": "plugins.modules.vizmlflow.bioml.adapter", "params": [{"name": "biodata", "type": "file"}, {"name": "imgdata", "type": "folder"}], "example": "", "desc": "", "group": "Bioinformatics", "returns": [{"name": "data", "type": "file"}], "access": 0, "sharedusers": [], "href": ""}	t	t	\N	\N	\N
\.


--
-- Data for Name: taskdata; Type: TABLE DATA; Schema: public; Owner: phenodoop
--

COPY public.taskdata (id, task_id, data_id) FROM stdin;
\.


--
-- Data for Name: tasklogs; Type: TABLE DATA; Schema: public; Owner: phenodoop
--

COPY public.tasklogs (id, task_id, "time", type, log) FROM stdin;
\.


--
-- Data for Name: tasks; Type: TABLE DATA; Schema: public; Owner: phenodoop
--

COPY public.tasks (id, runnable_id, service_id, started_on, ended_on, status, comment, duration) FROM stdin;
\.


--
-- Data for Name: taskstatus; Type: TABLE DATA; Schema: public; Owner: phenodoop
--

COPY public.taskstatus (id, name) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: phenodoop
--

COPY public.users (id, email, username, role_id, password_hash, confirmed, name, location, about_me, member_since, last_seen, avatar_hash, oid) FROM stdin;
2	admin@gmail.com	admin	1	pbkdf2:sha256:150000$dtFD7Hkz$ae6767f5a4ef70799981a777d67653c1b0da81d297898ebab8a7c93af0ab4bf1	t	\N	\N	\N	2022-08-31 16:44:26.121673	2022-08-31 16:44:26.121676	75d23af433e0cea4c0e45a56dba18b30	0
46	testuser@gmail.com	testuser	1	pbkdf2:sha256:260000$Zzr0RpE0lSJseC06$94060cc858d20816fdec87c97ceb937060bc3e915c6c45e6a270bd39d9d896ce	t	\N	\N	\N	2025-01-25 01:03:47.308674	2025-02-13 05:59:51.696612	a18bf786efb76a3d56ee69a3b343952a	0
47	anonymous1@gmail.com	anonymous1	1	pbkdf2:sha256:260000$iWpvGUKp9ZGX7LNy$3bcbe1036221f2122dca71d3518234307e4a2fa3a8191300f0bebdc5ac32925a	t	\N	\N	\N	2025-01-25 01:04:12.962787	2025-02-13 05:58:36.472786	82d2b2196bf4a0069ca3f8c52633d579	0
\.


--
-- Data for Name: visualizers; Type: TABLE DATA; Schema: public; Owner: phenodoop
--

COPY public.visualizers (id, name, "desc") FROM stdin;
\.


--
-- Data for Name: workflow_annotations; Type: TABLE DATA; Schema: public; Owner: phenodoop
--

COPY public.workflow_annotations (id, workflow_id, tag) FROM stdin;
\.


--
-- Data for Name: workflowaccesses; Type: TABLE DATA; Schema: public; Owner: phenodoop
--

COPY public.workflowaccesses (id, workflow_id, user_id, rights) FROM stdin;
\.


--
-- Data for Name: workflowparams; Type: TABLE DATA; Schema: public; Owner: phenodoop
--

COPY public.workflowparams (id, workflow_id, value) FROM stdin;
3	1	{"name": "data", "type": "file", "desc": "fastq/fasta file", "default": ""}
4	1	{"name": "ref", "type": "file", "desc": "reference genome", "default": ""}
21	35	{"name": "data", "type": "folder", "desc": "Path to the source system", "default": ""}
22	35	{"name": "threshold", "type": "float", "desc": "Similarity threshold", "default": "0.30"}
23	35	{"name": "granularity", "type": "str", "desc": "The granularity of code for clone detection. 'functions'|'blocks'", "default": "'blocks'"}
24	35	{"name": "language", "type": "str", "desc": "The source language. Supported languages are: C(.c), C#(.cs), Java (.java), Python (.py), PHP(.php), Ruby(.rb), WSDL(.wsdl) and ATL(.atl)", "default": "'java'"}
25	35	{"name": "transform", "type": "str", "desc": "Transformation to apply. 'none'|'sort'", "default": "'none'"}
26	35	{"name": "rename", "type": "str", "desc": "Renaming. 'blind'|'consistent'", "default": "'blind'"}
27	35	{"name": "filter", "type": "str", "desc": "Filter to apply. 'none'|'declaration'", "default": "'none'"}
28	35	{"name": "abstract", "type": "str", "desc": "'none'|'condition'|'expression'", "default": "'none'"}
29	35	{"name": "cluster", "type": "str", "desc": "'yes'|'no'", "default": "'yes'"}
30	35	{"name": "report", "type": "str", "desc": "'yes'|'no'", "default": "'yes'"}
31	35	{"name": "include", "type": "str", "desc": "", "default": "''"}
32	35	{"name": "exclude", "type": "str", "desc": "", "default": "''"}
33	35	{"name": "minclonesize", "type": "int", "desc": "Minimum clone size", "default": "10"}
34	35	{"name": "maxclonesize", "type": "int", "desc": "Maximum clone size", "default": "2500"}
35	35	{"name": "normalize", "type": "str", "desc": "'none'|'java-normalize-ifconditions-functions'|'xmlsortblocks','cabstractifconditions'", "default": "'none'"}
58	2	{"name": "", "type": "int", "desc": "", "default": ""}
61	36	{"name": "fasta", "type": "file", "desc": "A fasta file", "default": ""}
62	36	{"name": "imgs", "type": "folder", "desc": "The image folder", "default": ""}
63	37	{"name": "fasta", "type": "file", "desc": "FASTA file", "default": ""}
64	37	{"name": "imgs", "type": "folder", "desc": "Image folders", "default": ""}
65	37	{"name": "model", "type": "file", "desc": "Classifier model", "default": ""}
\.


--
-- Data for Name: workflowreturns; Type: TABLE DATA; Schema: public; Owner: phenodoop
--

COPY public.workflowreturns (id, workflow_id, value) FROM stdin;
2	1	{"name": "data", "type": "file", "desc": "alignment result"}
5	35	{"name": "clones", "type": "file", "desc": "The result clones"}
46	36	{"name": "data", "type": "file", "desc": "The classifier model for bio markers"}
47	37	{"name": "data", "type": "file", "desc": "The prediction in a .csv file"}
\.


--
-- Data for Name: workflows; Type: TABLE DATA; Schema: public; Owner: phenodoop
--

COPY public.workflows (id, user_id, created_on, modified_on, name, "desc", script, public, temp, derived) FROM stdin;
2	46	2025-01-25 01:35:42.440151	2025-01-29 04:49:02.732915	Check Quality and Sequence Alignment (No Parameter)	Check quality of a fasta/fastq file and align with a reference Genome. Constant paths are used for fasta/fastq file and reference genome.	data = '/public/MiSeq_SOP/F3D3_S191_L001_R1_001.fastq'\r\nref = '/public/genomes/Chr1.cdna'\r\nhtml,zip = fastqc.CheckQuality(data)\r\ndata = bwa.Align(ref, data)	t	f	0
1	46	2025-01-25 01:30:22.063266	2025-01-25 01:34:19.644784	Check Quality and Sequence Alignment	Check quality of a fasta/fastq file and align with a reference Genome	html,zip = fastqc.CheckQuality(data)\r\ndata = bwa.Align(ref, data)\r\nreturn data	t	f	0
38	46	2025-01-29 05:54:11.823966	2025-01-29 05:55:36.604428	NiCad clone detection No Parameter	NiCad clone detection workflow	data = '/public/swanalytics/luaj'\r\nthreshold = 0.30\r\ngranularity = 'blocks'\r\nlanguage = 'java'\r\ntransform = 'none'\r\nrename = 'blind'\r\nabstract = 'none'\r\ncluster = 'yes'\r\nreport = 'yes'\r\ninclude = ''\r\nexcluse = ''\r\nminiclonesize = 10\r\nmaxclonesize = 2500\r\nnormalize = 'none'\r\n\r\nnicad.CleanAll(dirname(data))\r\n\r\ndata = nicad.Extract(data,granularity=granularity,language=language)\r\n\r\n# transform doesn't work for java\r\nif transform != 'none':\r\n    data = nicad.Transform(data,granularity=granularity,language=language,transform=transform)\r\n\r\ndata = nicad.Rename(data,granularity=granularity,language=language,renaming=rename)\r\n\r\nif filter != 'none':\r\n    data = nicad.Filter(data,granularity=granularity,language=language,nonterminals=filter)\r\n\r\nif abstract != 'none':\r\n    data = nicad.Abstract(data,granularity=granularity,language=language,nonterminals=abstract)\r\n\r\n# normalize=none, so don't call it\r\nif normalize != 'none':\r\n    data = nicad.Normalize(data,granularity=granularity,language=language,normalizer=normalize)\r\ndata = nicad.FindClonePairs(data,threshold=threshold,minclonesize=minclonesize,maxclonesize=maxclonesize)\r\nclones=data\r\n\r\nif cluster == 'yes':\r\n    data = nicad.ClusterPairs(data)\r\n\r\nif report == 'yes':\r\n    data = nicad.GetSource(data)\r\n    data = nicad.MakePairHTML(data)	t	f	0
36	46	2025-01-28 02:11:10.38026	2025-01-29 05:17:17.400808	Biomarker Classifier Workflow	This is a small workflow to classify biomarkers	fasta = '/public/MiSeq_SOP/F3D3_S191_L001_R1_001.fastq'\r\nfa_markers = bio.BioMarkers(fasta)\r\n\r\nimgs = '/public/bioml/images'\r\nimg_markers = img.BioMarkers(imgs)\r\n\r\ndata = ml.ClassifyBioMarker(fa_markers, img_markers)\r\nreturn data	t	f	0
37	46	2025-01-28 10:59:23.026267	2025-01-28 10:59:48.749198	Biomarker Predictor Workflow	A workflow to predict biomarkers using a model	fasta = '/public/MiSeq_SOP/F3D149_S215_L001_R1_001.fastq'\r\nfa_markers = bio.BioMarkers(fasta)\r\n\r\nimgs = '/public/bioml/images'\r\nimg_markers = img.BioMarkers(imgs)\r\n\r\nmodel = '/users/testuser/temp/67189135-a7f7-42ae-9388-b362e05484cc/b45163f9-173b-4b49-80d1-a12efcc62592/d3dbaa03-c89d-4ddb-a372-e8b42160cc70.pkl'\r\ndata = ml.PredictBioMarker(fa_markers,img_markers,model)\r\nreturn data	t	f	0
35	46	2025-01-25 12:46:20.58381	2025-01-28 12:07:06.666131	NiCad clone detection	NiCad clone detection workflow	data = '/public/swanalytics/luaj'\r\n\r\nnicad.CleanAll(dirname(data))\r\n\r\ndata = nicad.Extract(data,granularity=granularity,language=language)\r\n\r\n# transform doesn't work for java\r\nif transform != 'none':\r\n    data = nicad.Transform(data,granularity=granularity,language=language,transform=transform)\r\n\r\ndata = nicad.Rename(data,granularity=granularity,language=language,renaming=rename)\r\n\r\nif filter != 'none':\r\n    data = nicad.Filter(data,granularity=granularity,language=language,nonterminals=filter)\r\n\r\nif abstract != 'none':\r\n    data = nicad.Abstract(data,granularity=granularity,language=language,nonterminals=abstract)\r\n\r\n# normalize=none, so don't call it\r\nif normalize != 'none':\r\n    data = nicad.Normalize(data,granularity=granularity,language=language,normalizer=normalize)\r\ndata = nicad.FindClonePairs(data,threshold=threshold,minclonesize=minclonesize,maxclonesize=maxclonesize)\r\nclones=data\r\n\r\nif cluster == 'yes':\r\n    data = nicad.ClusterPairs(data)\r\n\r\nif report == 'yes':\r\n    data = nicad.GetSource(data)\r\n    data = nicad.MakePairHTML(data)\r\n\r\nreturn clones	t	f	0
\.


--
-- Name: activities_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.activities_id_seq', 136, true);


--
-- Name: activitylogs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.activitylogs_id_seq', 351, true);


--
-- Name: comments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.comments_id_seq', 1, false);


--
-- Name: data_allocations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.data_allocations_id_seq', 168, true);


--
-- Name: data_annotations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.data_annotations_id_seq', 1, false);


--
-- Name: data_chunks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.data_chunks_id_seq', 1, false);


--
-- Name: data_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.data_id_seq', 168, true);


--
-- Name: data_mimetypes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.data_mimetypes_id_seq', 1, false);


--
-- Name: data_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.data_permissions_id_seq', 1, false);


--
-- Name: data_properties_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.data_properties_id_seq', 63, true);


--
-- Name: data_visualizers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.data_visualizers_id_seq', 1, false);


--
-- Name: datasets_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.datasets_id_seq', 1, false);


--
-- Name: datasource_allocations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.datasource_allocations_id_seq', 1, false);


--
-- Name: datasources_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.datasources_id_seq', 5, true);


--
-- Name: dockercontainers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.dockercontainers_id_seq', 1, false);


--
-- Name: dockerimages_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.dockerimages_id_seq', 1, false);


--
-- Name: filter_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.filter_history_id_seq', 1, false);


--
-- Name: filters_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.filters_id_seq', 1, false);


--
-- Name: indata_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.indata_id_seq', 105, true);


--
-- Name: mimetypes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.mimetypes_id_seq', 15, true);


--
-- Name: params_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.params_id_seq', 684, true);


--
-- Name: posts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.posts_id_seq', 1, false);


--
-- Name: returns_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.returns_id_seq', 339, true);


--
-- Name: roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.roles_id_seq', 3, true);


--
-- Name: runnableargs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.runnableargs_id_seq', 78, true);


--
-- Name: runnablereturns_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.runnablereturns_id_seq', 1, false);


--
-- Name: runnables_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.runnables_id_seq', 30, true);


--
-- Name: serviceaccesses_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.serviceaccesses_id_seq', 1, false);


--
-- Name: services_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.services_id_seq', 265, true);


--
-- Name: taskdata_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.taskdata_id_seq', 62, true);


--
-- Name: tasklogs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.tasklogs_id_seq', 320, true);


--
-- Name: tasks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.tasks_id_seq', 75, true);


--
-- Name: taskstatus_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.taskstatus_id_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.users_id_seq', 78, true);


--
-- Name: visualizers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.visualizers_id_seq', 1, false);


--
-- Name: workflow_annotations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.workflow_annotations_id_seq', 1, false);


--
-- Name: workflowaccesses_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.workflowaccesses_id_seq', 1, false);


--
-- Name: workflowparams_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.workflowparams_id_seq', 80, true);


--
-- Name: workflowreturns_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.workflowreturns_id_seq', 48, true);


--
-- Name: workflows_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.workflows_id_seq', 39, true);


--
-- Name: activities activities_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.activities
    ADD CONSTRAINT activities_pkey PRIMARY KEY (id);


--
-- Name: activitylogs activitylogs_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.activitylogs
    ADD CONSTRAINT activitylogs_pkey PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: comments comments_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_pkey PRIMARY KEY (id);


--
-- Name: data_allocations data_allocations_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_allocations
    ADD CONSTRAINT data_allocations_pkey PRIMARY KEY (id);


--
-- Name: data_annotations data_annotations_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_annotations
    ADD CONSTRAINT data_annotations_pkey PRIMARY KEY (id);


--
-- Name: data_mimetypes data_mimetypes_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_mimetypes
    ADD CONSTRAINT data_mimetypes_pkey PRIMARY KEY (id);


--
-- Name: data_permissions data_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_permissions
    ADD CONSTRAINT data_permissions_pkey PRIMARY KEY (id);


--
-- Name: data data_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data
    ADD CONSTRAINT data_pkey PRIMARY KEY (id);


--
-- Name: data_properties data_properties_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_properties
    ADD CONSTRAINT data_properties_pkey PRIMARY KEY (id);


--
-- Name: data_visualizers data_visualizers_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_visualizers
    ADD CONSTRAINT data_visualizers_pkey PRIMARY KEY (id);


--
-- Name: datasets datasets_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.datasets
    ADD CONSTRAINT datasets_pkey PRIMARY KEY (id);


--
-- Name: datasource_allocations datasource_allocations_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.datasource_allocations
    ADD CONSTRAINT datasource_allocations_pkey PRIMARY KEY (id);


--
-- Name: datasources datasources_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.datasources
    ADD CONSTRAINT datasources_pkey PRIMARY KEY (id);


--
-- Name: dockercontainers dockercontainers_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.dockercontainers
    ADD CONSTRAINT dockercontainers_pkey PRIMARY KEY (id);


--
-- Name: dockerimages dockerimages_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.dockerimages
    ADD CONSTRAINT dockerimages_pkey PRIMARY KEY (id);


--
-- Name: filter_history filter_history_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.filter_history
    ADD CONSTRAINT filter_history_pkey PRIMARY KEY (id);


--
-- Name: filters filters_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.filters
    ADD CONSTRAINT filters_pkey PRIMARY KEY (id);


--
-- Name: follows follows_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.follows
    ADD CONSTRAINT follows_pkey PRIMARY KEY (follower_id, followed_id);


--
-- Name: indata indata_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.indata
    ADD CONSTRAINT indata_pkey PRIMARY KEY (id);


--
-- Name: mimetypes mimetypes_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.mimetypes
    ADD CONSTRAINT mimetypes_pkey PRIMARY KEY (id);


--
-- Name: params params_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.params
    ADD CONSTRAINT params_pkey PRIMARY KEY (id);


--
-- Name: posts posts_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_pkey PRIMARY KEY (id);


--
-- Name: returns returns_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.returns
    ADD CONSTRAINT returns_pkey PRIMARY KEY (id);


--
-- Name: roles roles_name_key; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_name_key UNIQUE (name);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- Name: runnableargs runnableargs_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.runnableargs
    ADD CONSTRAINT runnableargs_pkey PRIMARY KEY (id);


--
-- Name: runnablereturns runnablereturns_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.runnablereturns
    ADD CONSTRAINT runnablereturns_pkey PRIMARY KEY (id);


--
-- Name: runnables runnables_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.runnables
    ADD CONSTRAINT runnables_pkey PRIMARY KEY (id);


--
-- Name: serviceaccesses serviceaccesses_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.serviceaccesses
    ADD CONSTRAINT serviceaccesses_pkey PRIMARY KEY (id);


--
-- Name: services services_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.services
    ADD CONSTRAINT services_pkey PRIMARY KEY (id);


--
-- Name: taskdata taskdata_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.taskdata
    ADD CONSTRAINT taskdata_pkey PRIMARY KEY (id);


--
-- Name: tasklogs tasklogs_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.tasklogs
    ADD CONSTRAINT tasklogs_pkey PRIMARY KEY (id);


--
-- Name: tasks tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_pkey PRIMARY KEY (id);


--
-- Name: taskstatus taskstatus_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.taskstatus
    ADD CONSTRAINT taskstatus_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: visualizers visualizers_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.visualizers
    ADD CONSTRAINT visualizers_pkey PRIMARY KEY (id);


--
-- Name: workflow_annotations workflow_annotations_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.workflow_annotations
    ADD CONSTRAINT workflow_annotations_pkey PRIMARY KEY (id);


--
-- Name: workflowaccesses workflowaccesses_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.workflowaccesses
    ADD CONSTRAINT workflowaccesses_pkey PRIMARY KEY (id);


--
-- Name: workflowparams workflowparams_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.workflowparams
    ADD CONSTRAINT workflowparams_pkey PRIMARY KEY (id);


--
-- Name: workflowreturns workflowreturns_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.workflowreturns
    ADD CONSTRAINT workflowreturns_pkey PRIMARY KEY (id);


--
-- Name: workflows workflows_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.workflows
    ADD CONSTRAINT workflows_pkey PRIMARY KEY (id);


--
-- Name: ix_comments_timestamp; Type: INDEX; Schema: public; Owner: phenodoop
--

CREATE INDEX ix_comments_timestamp ON public.comments USING btree ("timestamp");


--
-- Name: ix_posts_timestamp; Type: INDEX; Schema: public; Owner: phenodoop
--

CREATE INDEX ix_posts_timestamp ON public.posts USING btree ("timestamp");


--
-- Name: ix_roles_default; Type: INDEX; Schema: public; Owner: phenodoop
--

CREATE INDEX ix_roles_default ON public.roles USING btree ("default");


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: phenodoop
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: ix_users_username; Type: INDEX; Schema: public; Owner: phenodoop
--

CREATE UNIQUE INDEX ix_users_username ON public.users USING btree (username);


--
-- Name: activities activities_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.activities
    ADD CONSTRAINT activities_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: activitylogs activitylogs_activity_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.activitylogs
    ADD CONSTRAINT activitylogs_activity_id_fkey FOREIGN KEY (activity_id) REFERENCES public.activities(id);


--
-- Name: comments comments_author_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_author_id_fkey FOREIGN KEY (author_id) REFERENCES public.users(id);


--
-- Name: comments comments_post_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_post_id_fkey FOREIGN KEY (post_id) REFERENCES public.posts(id);


--
-- Name: data_allocations data_allocations_data_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_allocations
    ADD CONSTRAINT data_allocations_data_id_fkey FOREIGN KEY (data_id) REFERENCES public.data(id);


--
-- Name: data_allocations data_allocations_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_allocations
    ADD CONSTRAINT data_allocations_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: data_annotations data_annotations_data_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_annotations
    ADD CONSTRAINT data_annotations_data_id_fkey FOREIGN KEY (data_id) REFERENCES public.datasource_allocations(id);


--
-- Name: data_mimetypes data_mimetypes_data_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_mimetypes
    ADD CONSTRAINT data_mimetypes_data_id_fkey FOREIGN KEY (data_id) REFERENCES public.datasource_allocations(id);


--
-- Name: data_mimetypes data_mimetypes_mimetype_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_mimetypes
    ADD CONSTRAINT data_mimetypes_mimetype_id_fkey FOREIGN KEY (mimetype_id) REFERENCES public.mimetypes(id);


--
-- Name: data_permissions data_permissions_data_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_permissions
    ADD CONSTRAINT data_permissions_data_id_fkey FOREIGN KEY (data_id) REFERENCES public.datasource_allocations(id);


--
-- Name: data_permissions data_permissions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_permissions
    ADD CONSTRAINT data_permissions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: data_properties data_properties_data_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_properties
    ADD CONSTRAINT data_properties_data_id_fkey FOREIGN KEY (data_id) REFERENCES public.data(id);


--
-- Name: data_visualizers data_visualizers_data_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_visualizers
    ADD CONSTRAINT data_visualizers_data_id_fkey FOREIGN KEY (data_id) REFERENCES public.datasource_allocations(id);


--
-- Name: data_visualizers data_visualizers_visualizer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.data_visualizers
    ADD CONSTRAINT data_visualizers_visualizer_id_fkey FOREIGN KEY (visualizer_id) REFERENCES public.visualizers(id);


--
-- Name: datasource_allocations datasource_allocations_datasource_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.datasource_allocations
    ADD CONSTRAINT datasource_allocations_datasource_id_fkey FOREIGN KEY (datasource_id) REFERENCES public.datasources(id);


--
-- Name: filter_history filter_history_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.filter_history
    ADD CONSTRAINT filter_history_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: filters filters_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.filters
    ADD CONSTRAINT filters_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: dockercontainers fk_dockerimages_dockercontainers; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.dockercontainers
    ADD CONSTRAINT fk_dockerimages_dockercontainers FOREIGN KEY (image_id) REFERENCES public.dockerimages(id);


--
-- Name: dockercontainers fk_users_dockercontainers; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.dockercontainers
    ADD CONSTRAINT fk_users_dockercontainers FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: follows follows_followed_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.follows
    ADD CONSTRAINT follows_followed_id_fkey FOREIGN KEY (followed_id) REFERENCES public.users(id);


--
-- Name: follows follows_follower_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.follows
    ADD CONSTRAINT follows_follower_id_fkey FOREIGN KEY (follower_id) REFERENCES public.users(id);


--
-- Name: indata indata_data_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.indata
    ADD CONSTRAINT indata_data_id_fkey FOREIGN KEY (data_id) REFERENCES public.data(id);


--
-- Name: indata indata_task_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.indata
    ADD CONSTRAINT indata_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.tasks(id);


--
-- Name: params params_service_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.params
    ADD CONSTRAINT params_service_id_fkey FOREIGN KEY (service_id) REFERENCES public.services(id);


--
-- Name: posts posts_author_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_author_id_fkey FOREIGN KEY (author_id) REFERENCES public.users(id);


--
-- Name: returns returns_service_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.returns
    ADD CONSTRAINT returns_service_id_fkey FOREIGN KEY (service_id) REFERENCES public.services(id);


--
-- Name: runnableargs runnableargs_runnable_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.runnableargs
    ADD CONSTRAINT runnableargs_runnable_id_fkey FOREIGN KEY (runnable_id) REFERENCES public.runnables(id);


--
-- Name: runnablereturns runnablereturns_runnable_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.runnablereturns
    ADD CONSTRAINT runnablereturns_runnable_id_fkey FOREIGN KEY (runnable_id) REFERENCES public.runnables(id);


--
-- Name: runnables runnables_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.runnables
    ADD CONSTRAINT runnables_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: runnables runnables_workflow_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.runnables
    ADD CONSTRAINT runnables_workflow_id_fkey FOREIGN KEY (workflow_id) REFERENCES public.workflows(id) ON DELETE CASCADE;


--
-- Name: serviceaccesses serviceaccesses_service_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.serviceaccesses
    ADD CONSTRAINT serviceaccesses_service_id_fkey FOREIGN KEY (service_id) REFERENCES public.services(id) ON DELETE CASCADE;


--
-- Name: serviceaccesses serviceaccesses_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.serviceaccesses
    ADD CONSTRAINT serviceaccesses_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: services services_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.services
    ADD CONSTRAINT services_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: taskdata taskdata_data_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.taskdata
    ADD CONSTRAINT taskdata_data_id_fkey FOREIGN KEY (data_id) REFERENCES public.data(id);


--
-- Name: taskdata taskdata_task_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.taskdata
    ADD CONSTRAINT taskdata_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.tasks(id);


--
-- Name: tasklogs tasklogs_task_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.tasklogs
    ADD CONSTRAINT tasklogs_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.tasks(id);


--
-- Name: tasks tasks_runnable_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_runnable_id_fkey FOREIGN KEY (runnable_id) REFERENCES public.runnables(id);


--
-- Name: tasks tasks_service_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_service_id_fkey FOREIGN KEY (service_id) REFERENCES public.services(id);


--
-- Name: users users_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id);


--
-- Name: workflow_annotations workflow_annotations_workflow_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.workflow_annotations
    ADD CONSTRAINT workflow_annotations_workflow_id_fkey FOREIGN KEY (workflow_id) REFERENCES public.workflows(id);


--
-- Name: workflowaccesses workflowaccesses_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.workflowaccesses
    ADD CONSTRAINT workflowaccesses_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: workflowaccesses workflowaccesses_workflow_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.workflowaccesses
    ADD CONSTRAINT workflowaccesses_workflow_id_fkey FOREIGN KEY (workflow_id) REFERENCES public.workflows(id);


--
-- Name: workflowparams workflowparams_workflow_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.workflowparams
    ADD CONSTRAINT workflowparams_workflow_id_fkey FOREIGN KEY (workflow_id) REFERENCES public.workflows(id);


--
-- Name: workflowreturns workflowreturns_workflow_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.workflowreturns
    ADD CONSTRAINT workflowreturns_workflow_id_fkey FOREIGN KEY (workflow_id) REFERENCES public.workflows(id);


--
-- Name: workflows workflows_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.workflows
    ADD CONSTRAINT workflows_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

