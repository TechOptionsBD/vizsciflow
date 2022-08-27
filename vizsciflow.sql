--
-- PostgreSQL database dump
--

-- Dumped from database version 13.6
-- Dumped by pg_dump version 13.6

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
    active boolean
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
    comment text
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
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
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
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
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

