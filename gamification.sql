--
-- gamification data storage
--

\restrict vp5AOohTfP0QlBHRKlwLxgU0ZvJIIGcfIRifX0CRPw6P5tWG5nRdSyv6LBOCUyC

--
-- Name: game_points; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.game_points (
    id integer PRIMARY KEY,
    user_id integer,
    mission_id integer,
    cumulative_points integer,
    record_time timestamp without time zone
);

ALTER TABLE public.game_points OWNER TO phenodoop;

--
-- Name: game_usage_history; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.game_usage_history (
    id integer PRIMARY KEY,
    user_id integer,
    record_time date
);

ALTER TABLE public.game_usage_history OWNER TO phenodoop;

--
-- Name: game_missions; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.game_missions (
    id integer PRIMARY KEY,
    completed boolean,
    points int,
    title text,
    description text,
    tutorial text
);

ALTER TABLE public.game_missions OWNER TO phenodoop;

\unrestrict vp5AOohTfP0QlBHRKlwLxgU0ZvJIIGcfIRifX0CRPw6P5tWG5nRdSyv6LBOCUyC

