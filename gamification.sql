--
-- gamification data storage
--

\restrict vp5AOohTfP0QlBHRKlwLxgU0ZvJIIGcfIRifX0CRPw6P5tWG5nRdSyv6LBOCUyC

--
-- Name: game_points; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.game_points (
    id integer NOT NULL,
    user_id integer NOT NULL,
    points integer NOT NULL,
    title text,
    record_time timestamp without time zone
);

ALTER TABLE public.game_points OWNER TO phenodoop;

--
-- Name: game_usage_history; Type: TABLE; Schema: public; Owner: phenodoop
--

CREATE TABLE public.game_usage_history (
    id integer NOT NULL,
    user_id integer NOT NULL,
    record_time date
);

ALTER TABLE public.game_points OWNER TO phenodoop;

\unrestrict vp5AOohTfP0QlBHRKlwLxgU0ZvJIIGcfIRifX0CRPw6P5tWG5nRdSyv6LBOCUyC

