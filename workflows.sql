--
-- PostgreSQL database dump
--

-- Dumped from database version 13.18 (Debian 13.18-0+deb11u1)
-- Dumped by pg_dump version 13.18 (Debian 13.18-0+deb11u1)

-- Started on 2025-01-29 06:49:50 UTC

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
-- TOC entry 280 (class 1259 OID 24861)
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
-- TOC entry 281 (class 1259 OID 24867)
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
-- TOC entry 3221 (class 0 OID 0)
-- Dependencies: 281
-- Name: workflows_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: phenodoop
--

ALTER SEQUENCE public.workflows_id_seq OWNED BY public.workflows.id;


--
-- TOC entry 3080 (class 2604 OID 24908)
-- Name: workflows id; Type: DEFAULT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.workflows ALTER COLUMN id SET DEFAULT nextval('public.workflows_id_seq'::regclass);


--
-- TOC entry 3214 (class 0 OID 24861)
-- Dependencies: 280
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
-- TOC entry 3222 (class 0 OID 0)
-- Dependencies: 281
-- Name: workflows_id_seq; Type: SEQUENCE SET; Schema: public; Owner: phenodoop
--

SELECT pg_catalog.setval('public.workflows_id_seq', 39, true);


--
-- TOC entry 3082 (class 2606 OID 24992)
-- Name: workflows workflows_pkey; Type: CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.workflows
    ADD CONSTRAINT workflows_pkey PRIMARY KEY (id);


--
-- TOC entry 3083 (class 2606 OID 25218)
-- Name: workflows workflows_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: phenodoop
--

ALTER TABLE ONLY public.workflows
    ADD CONSTRAINT workflows_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


-- Completed on 2025-01-29 06:49:53 UTC

--
-- PostgreSQL database dump complete
--

