--
-- PostgreSQL database dump
--

-- Dumped from database version 12.1
-- Dumped by pg_dump version 12.0

-- Started on 2020-02-17 15:53:27 CST

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
-- TOC entry 209 (class 1259 OID 113496)
-- Name: auth_group; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO postgres;

--
-- TOC entry 208 (class 1259 OID 113494)
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO postgres;

--
-- TOC entry 4056 (class 0 OID 0)
-- Dependencies: 208
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- TOC entry 211 (class 1259 OID 113506)
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO postgres;

--
-- TOC entry 210 (class 1259 OID 113504)
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO postgres;

--
-- TOC entry 4057 (class 0 OID 0)
-- Dependencies: 210
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- TOC entry 207 (class 1259 OID 113488)
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO postgres;

--
-- TOC entry 206 (class 1259 OID 113486)
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO postgres;

--
-- TOC entry 4058 (class 0 OID 0)
-- Dependencies: 206
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- TOC entry 219 (class 1259 OID 113595)
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 113593)
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO postgres;

--
-- TOC entry 4059 (class 0 OID 0)
-- Dependencies: 218
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- TOC entry 205 (class 1259 OID 113478)
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO postgres;

--
-- TOC entry 204 (class 1259 OID 113476)
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO postgres;

--
-- TOC entry 4060 (class 0 OID 0)
-- Dependencies: 204
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- TOC entry 203 (class 1259 OID 113467)
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO postgres;

--
-- TOC entry 202 (class 1259 OID 113465)
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_migrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO postgres;

--
-- TOC entry 4061 (class 0 OID 0)
-- Dependencies: 202
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- TOC entry 323 (class 1259 OID 114817)
-- Name: django_session; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO postgres;

--
-- TOC entry 248 (class 1259 OID 113855)
-- Name: mccr_changelog; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mccr_changelog (
    id integer NOT NULL,
    date timestamp with time zone NOT NULL,
    previous_status character varying(100),
    current_status character varying(100) NOT NULL,
    mccr_id uuid NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.mccr_changelog OWNER TO postgres;

--
-- TOC entry 247 (class 1259 OID 113853)
-- Name: mccr_changelog_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mccr_changelog_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mccr_changelog_id_seq OWNER TO postgres;

--
-- TOC entry 4062 (class 0 OID 0)
-- Dependencies: 247
-- Name: mccr_changelog_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mccr_changelog_id_seq OWNED BY public.mccr_changelog.id;


--
-- TOC entry 239 (class 1259 OID 113761)
-- Name: mccr_mccrfile; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mccr_mccrfile (
    id uuid NOT NULL,
    file character varying(100) NOT NULL,
    mccr_id uuid NOT NULL,
    user_id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL
);


ALTER TABLE public.mccr_mccrfile OWNER TO postgres;

--
-- TOC entry 240 (class 1259 OID 113766)
-- Name: mccr_mccrregistry; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mccr_mccrregistry (
    id uuid NOT NULL,
    user_type_id integer NOT NULL,
    mitigation_id uuid NOT NULL,
    user_id integer NOT NULL,
    status character varying(50) NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    fsm_state character varying(50) NOT NULL
);


ALTER TABLE public.mccr_mccrregistry OWNER TO postgres;

--
-- TOC entry 244 (class 1259 OID 113825)
-- Name: mccr_mccrregistryovvrelation; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mccr_mccrregistryovvrelation (
    id integer NOT NULL,
    status character varying(100),
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    mccr_id uuid NOT NULL,
    ovv_id integer NOT NULL
);


ALTER TABLE public.mccr_mccrregistryovvrelation OWNER TO postgres;

--
-- TOC entry 243 (class 1259 OID 113823)
-- Name: mccr_mccrregistryovvrelation_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mccr_mccrregistryovvrelation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mccr_mccrregistryovvrelation_id_seq OWNER TO postgres;

--
-- TOC entry 4063 (class 0 OID 0)
-- Dependencies: 243
-- Name: mccr_mccrregistryovvrelation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mccr_mccrregistryovvrelation_id_seq OWNED BY public.mccr_mccrregistryovvrelation.id;


--
-- TOC entry 242 (class 1259 OID 113798)
-- Name: mccr_mccrusertype; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mccr_mccrusertype (
    id integer NOT NULL,
    name character varying(100) NOT NULL
);


ALTER TABLE public.mccr_mccrusertype OWNER TO postgres;

--
-- TOC entry 241 (class 1259 OID 113796)
-- Name: mccr_mccrusertype_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mccr_mccrusertype_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mccr_mccrusertype_id_seq OWNER TO postgres;

--
-- TOC entry 4064 (class 0 OID 0)
-- Dependencies: 241
-- Name: mccr_mccrusertype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mccr_mccrusertype_id_seq OWNED BY public.mccr_mccrusertype.id;


--
-- TOC entry 250 (class 1259 OID 113863)
-- Name: mccr_mccrworkflowstep; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mccr_mccrworkflowstep (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    entry_name character varying(100) NOT NULL,
    status character varying(50) NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    mccr_id uuid NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.mccr_mccrworkflowstep OWNER TO postgres;

--
-- TOC entry 249 (class 1259 OID 113861)
-- Name: mccr_mccrworkflowstep_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mccr_mccrworkflowstep_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mccr_mccrworkflowstep_id_seq OWNER TO postgres;

--
-- TOC entry 4065 (class 0 OID 0)
-- Dependencies: 249
-- Name: mccr_mccrworkflowstep_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mccr_mccrworkflowstep_id_seq OWNED BY public.mccr_mccrworkflowstep.id;


--
-- TOC entry 252 (class 1259 OID 113871)
-- Name: mccr_mccrworkflowstepfile; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mccr_mccrworkflowstepfile (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    file character varying(100) NOT NULL,
    user_id integer NOT NULL,
    workflow_step_id integer NOT NULL
);


ALTER TABLE public.mccr_mccrworkflowstepfile OWNER TO postgres;

--
-- TOC entry 251 (class 1259 OID 113869)
-- Name: mccr_mccrworkflowstepfile_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mccr_mccrworkflowstepfile_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mccr_mccrworkflowstepfile_id_seq OWNER TO postgres;

--
-- TOC entry 4066 (class 0 OID 0)
-- Dependencies: 251
-- Name: mccr_mccrworkflowstepfile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mccr_mccrworkflowstepfile_id_seq OWNED BY public.mccr_mccrworkflowstepfile.id;


--
-- TOC entry 246 (class 1259 OID 113833)
-- Name: mccr_ovv; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mccr_ovv (
    id integer NOT NULL,
    name character varying(200) NOT NULL,
    email character varying(50) NOT NULL,
    phone character varying(30) NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL
);


ALTER TABLE public.mccr_ovv OWNER TO postgres;

--
-- TOC entry 245 (class 1259 OID 113831)
-- Name: mccr_ovv_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mccr_ovv_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mccr_ovv_id_seq OWNER TO postgres;

--
-- TOC entry 4067 (class 0 OID 0)
-- Dependencies: 245
-- Name: mccr_ovv_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mccr_ovv_id_seq OWNED BY public.mccr_ovv.id;


--
-- TOC entry 260 (class 1259 OID 113960)
-- Name: mitigation_action_changelog; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitigation_action_changelog (
    id integer NOT NULL,
    date timestamp with time zone NOT NULL,
    current_status character varying(100) NOT NULL,
    mitigation_action_id uuid NOT NULL,
    previous_status character varying(100),
    user_id integer NOT NULL
);


ALTER TABLE public.mitigation_action_changelog OWNER TO postgres;

--
-- TOC entry 259 (class 1259 OID 113958)
-- Name: mitigation_action_changelog_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mitigation_action_changelog_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mitigation_action_changelog_id_seq OWNER TO postgres;

--
-- TOC entry 4068 (class 0 OID 0)
-- Dependencies: 259
-- Name: mitigation_action_changelog_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitigation_action_changelog_id_seq OWNED BY public.mitigation_action_changelog.id;


--
-- TOC entry 221 (class 1259 OID 113620)
-- Name: mitigation_action_contact; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitigation_action_contact (
    id integer NOT NULL,
    full_name character varying(100) NOT NULL,
    job_title character varying(100) NOT NULL,
    email character varying(254) NOT NULL,
    phone character varying(100) NOT NULL
);


ALTER TABLE public.mitigation_action_contact OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 113618)
-- Name: mitigation_action_contact_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mitigation_action_contact_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mitigation_action_contact_id_seq OWNER TO postgres;

--
-- TOC entry 4069 (class 0 OID 0)
-- Dependencies: 220
-- Name: mitigation_action_contact_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitigation_action_contact_id_seq OWNED BY public.mitigation_action_contact.id;


--
-- TOC entry 223 (class 1259 OID 113631)
-- Name: mitigation_action_finance; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitigation_action_finance (
    id integer NOT NULL,
    source character varying(100),
    status_id integer NOT NULL
);


ALTER TABLE public.mitigation_action_finance OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 113629)
-- Name: mitigation_action_finance_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mitigation_action_finance_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mitigation_action_finance_id_seq OWNER TO postgres;

--
-- TOC entry 4070 (class 0 OID 0)
-- Dependencies: 222
-- Name: mitigation_action_finance_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitigation_action_finance_id_seq OWNED BY public.mitigation_action_finance.id;


--
-- TOC entry 264 (class 1259 OID 114023)
-- Name: mitigation_action_financesourcetype; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitigation_action_financesourcetype (
    id integer NOT NULL,
    name_en character varying(100) NOT NULL,
    name_es character varying(100) NOT NULL
);


ALTER TABLE public.mitigation_action_financesourcetype OWNER TO postgres;

--
-- TOC entry 263 (class 1259 OID 114021)
-- Name: mitigation_action_financesourcetype_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mitigation_action_financesourcetype_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mitigation_action_financesourcetype_id_seq OWNER TO postgres;

--
-- TOC entry 4071 (class 0 OID 0)
-- Dependencies: 263
-- Name: mitigation_action_financesourcetype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitigation_action_financesourcetype_id_seq OWNED BY public.mitigation_action_financesourcetype.id;


--
-- TOC entry 270 (class 1259 OID 114189)
-- Name: mitigation_action_financestatus; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitigation_action_financestatus (
    id integer NOT NULL,
    name_es character varying(100) NOT NULL,
    name_en character varying(100) NOT NULL
);


ALTER TABLE public.mitigation_action_financestatus OWNER TO postgres;

--
-- TOC entry 269 (class 1259 OID 114187)
-- Name: mitigation_action_financestatus_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mitigation_action_financestatus_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mitigation_action_financestatus_id_seq OWNER TO postgres;

--
-- TOC entry 4072 (class 0 OID 0)
-- Dependencies: 269
-- Name: mitigation_action_financestatus_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitigation_action_financestatus_id_seq OWNED BY public.mitigation_action_financestatus.id;


--
-- TOC entry 225 (class 1259 OID 113639)
-- Name: mitigation_action_geographicscale; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitigation_action_geographicscale (
    id integer NOT NULL,
    name_en character varying(100) NOT NULL,
    name_es character varying(100) NOT NULL
);


ALTER TABLE public.mitigation_action_geographicscale OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 113637)
-- Name: mitigation_action_geographicscale_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mitigation_action_geographicscale_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mitigation_action_geographicscale_id_seq OWNER TO postgres;

--
-- TOC entry 4073 (class 0 OID 0)
-- Dependencies: 224
-- Name: mitigation_action_geographicscale_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitigation_action_geographicscale_id_seq OWNED BY public.mitigation_action_geographicscale.id;


--
-- TOC entry 227 (class 1259 OID 113647)
-- Name: mitigation_action_ingeicompliance; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitigation_action_ingeicompliance (
    id integer NOT NULL,
    name_en character varying(100) NOT NULL,
    name_es character varying(100) NOT NULL
);


ALTER TABLE public.mitigation_action_ingeicompliance OWNER TO postgres;

--
-- TOC entry 226 (class 1259 OID 113645)
-- Name: mitigation_action_ingeicompliance_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mitigation_action_ingeicompliance_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mitigation_action_ingeicompliance_id_seq OWNER TO postgres;

--
-- TOC entry 4074 (class 0 OID 0)
-- Dependencies: 226
-- Name: mitigation_action_ingeicompliance_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitigation_action_ingeicompliance_id_seq OWNED BY public.mitigation_action_ingeicompliance.id;


--
-- TOC entry 272 (class 1259 OID 114197)
-- Name: mitigation_action_initiative; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitigation_action_initiative (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    objective character varying(400) NOT NULL,
    description character varying(400) NOT NULL,
    goal character varying(400) NOT NULL,
    entity_responsible character varying(100) NOT NULL,
    budget numeric(20,2),
    contact_id integer NOT NULL,
    finance_id integer NOT NULL,
    initiative_type_id integer NOT NULL,
    status_id integer NOT NULL
);


ALTER TABLE public.mitigation_action_initiative OWNER TO postgres;

--
-- TOC entry 271 (class 1259 OID 114195)
-- Name: mitigation_action_initiative_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mitigation_action_initiative_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mitigation_action_initiative_id_seq OWNER TO postgres;

--
-- TOC entry 4075 (class 0 OID 0)
-- Dependencies: 271
-- Name: mitigation_action_initiative_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitigation_action_initiative_id_seq OWNED BY public.mitigation_action_initiative.id;


--
-- TOC entry 274 (class 1259 OID 114208)
-- Name: mitigation_action_initiativefinance; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitigation_action_initiativefinance (
    id integer NOT NULL,
    finance_source_type_id integer NOT NULL,
    status_id integer NOT NULL,
    source character varying(500)
);


ALTER TABLE public.mitigation_action_initiativefinance OWNER TO postgres;

--
-- TOC entry 273 (class 1259 OID 114206)
-- Name: mitigation_action_initiativefinance_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mitigation_action_initiativefinance_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mitigation_action_initiativefinance_id_seq OWNER TO postgres;

--
-- TOC entry 4076 (class 0 OID 0)
-- Dependencies: 273
-- Name: mitigation_action_initiativefinance_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitigation_action_initiativefinance_id_seq OWNED BY public.mitigation_action_initiativefinance.id;


--
-- TOC entry 276 (class 1259 OID 114216)
-- Name: mitigation_action_initiativetype; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitigation_action_initiativetype (
    id integer NOT NULL,
    initiative_type_es character varying(100) NOT NULL,
    initiative_type_en character varying(100) NOT NULL
);


ALTER TABLE public.mitigation_action_initiativetype OWNER TO postgres;

--
-- TOC entry 275 (class 1259 OID 114214)
-- Name: mitigation_action_initiativetype_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mitigation_action_initiativetype_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mitigation_action_initiativetype_id_seq OWNER TO postgres;

--
-- TOC entry 4077 (class 0 OID 0)
-- Dependencies: 275
-- Name: mitigation_action_initiativetype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitigation_action_initiativetype_id_seq OWNED BY public.mitigation_action_initiativetype.id;


--
-- TOC entry 229 (class 1259 OID 113655)
-- Name: mitigation_action_institution; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitigation_action_institution (
    id integer NOT NULL,
    name character varying(100) NOT NULL
);


ALTER TABLE public.mitigation_action_institution OWNER TO postgres;

--
-- TOC entry 228 (class 1259 OID 113653)
-- Name: mitigation_action_institution_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mitigation_action_institution_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mitigation_action_institution_id_seq OWNER TO postgres;

--
-- TOC entry 4078 (class 0 OID 0)
-- Dependencies: 228
-- Name: mitigation_action_institution_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitigation_action_institution_id_seq OWNED BY public.mitigation_action_institution.id;


--
-- TOC entry 231 (class 1259 OID 113663)
-- Name: mitigation_action_location; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitigation_action_location (
    id integer NOT NULL,
    geographical_site character varying(100) NOT NULL,
    is_gis_annexed boolean NOT NULL
);


ALTER TABLE public.mitigation_action_location OWNER TO postgres;

--
-- TOC entry 230 (class 1259 OID 113661)
-- Name: mitigation_action_location_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mitigation_action_location_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mitigation_action_location_id_seq OWNER TO postgres;

--
-- TOC entry 4079 (class 0 OID 0)
-- Dependencies: 230
-- Name: mitigation_action_location_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitigation_action_location_id_seq OWNED BY public.mitigation_action_location.id;


--
-- TOC entry 266 (class 1259 OID 114129)
-- Name: mitigation_action_maworkflowstep; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitigation_action_maworkflowstep (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    entry_name character varying(100) NOT NULL,
    status character varying(50) NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    mitigation_action_id uuid NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.mitigation_action_maworkflowstep OWNER TO postgres;

--
-- TOC entry 265 (class 1259 OID 114127)
-- Name: mitigation_action_maworkflowstep_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mitigation_action_maworkflowstep_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mitigation_action_maworkflowstep_id_seq OWNER TO postgres;

--
-- TOC entry 4080 (class 0 OID 0)
-- Dependencies: 265
-- Name: mitigation_action_maworkflowstep_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitigation_action_maworkflowstep_id_seq OWNED BY public.mitigation_action_maworkflowstep.id;


--
-- TOC entry 268 (class 1259 OID 114137)
-- Name: mitigation_action_maworkflowstepfile; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitigation_action_maworkflowstepfile (
    id integer NOT NULL,
    file character varying(100) NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    user_id integer NOT NULL,
    workflow_step_id integer NOT NULL
);


ALTER TABLE public.mitigation_action_maworkflowstepfile OWNER TO postgres;

--
-- TOC entry 267 (class 1259 OID 114135)
-- Name: mitigation_action_maworkflowstepfile_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mitigation_action_maworkflowstepfile_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mitigation_action_maworkflowstepfile_id_seq OWNER TO postgres;

--
-- TOC entry 4081 (class 0 OID 0)
-- Dependencies: 267
-- Name: mitigation_action_maworkflowstepfile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitigation_action_maworkflowstepfile_id_seq OWNED BY public.mitigation_action_maworkflowstepfile.id;


--
-- TOC entry 232 (class 1259 OID 113669)
-- Name: mitigation_action_mitigation; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitigation_action_mitigation (
    id uuid NOT NULL,
    strategy_name character varying(100),
    name character varying(100),
    purpose character varying(500),
    start_date date,
    end_date date,
    gas_inventory character varying(100),
    emissions_source character varying(100),
    carbon_sinks character varying(100),
    impact_plan character varying(500),
    impact character varying(500),
    calculation_methodology character varying(500),
    is_international boolean,
    international_participation character varying(100),
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    contact_id integer,
    finance_id integer,
    geographic_scale_id integer,
    institution_id integer,
    location_id integer,
    progress_indicator_id integer,
    registration_type_id integer,
    status_id integer,
    user_id integer NOT NULL,
    review_count integer,
    fsm_state character varying(100) NOT NULL,
    initiative_id integer
);


ALTER TABLE public.mitigation_action_mitigation OWNER TO postgres;

--
-- TOC entry 262 (class 1259 OID 113968)
-- Name: mitigation_action_mitigation_comments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitigation_action_mitigation_comments (
    id integer NOT NULL,
    mitigation_id uuid NOT NULL,
    comment_id integer NOT NULL
);


ALTER TABLE public.mitigation_action_mitigation_comments OWNER TO postgres;

--
-- TOC entry 261 (class 1259 OID 113966)
-- Name: mitigation_action_mitigation_comments_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mitigation_action_mitigation_comments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mitigation_action_mitigation_comments_id_seq OWNER TO postgres;

--
-- TOC entry 4082 (class 0 OID 0)
-- Dependencies: 261
-- Name: mitigation_action_mitigation_comments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitigation_action_mitigation_comments_id_seq OWNED BY public.mitigation_action_mitigation_comments.id;


--
-- TOC entry 258 (class 1259 OID 113938)
-- Name: mitigation_action_mitigation_ingei_compliances; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitigation_action_mitigation_ingei_compliances (
    id integer NOT NULL,
    mitigation_id uuid NOT NULL,
    ingeicompliance_id integer NOT NULL
);


ALTER TABLE public.mitigation_action_mitigation_ingei_compliances OWNER TO postgres;

--
-- TOC entry 257 (class 1259 OID 113936)
-- Name: mitigation_action_mitigation_ingei_compliances_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mitigation_action_mitigation_ingei_compliances_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mitigation_action_mitigation_ingei_compliances_id_seq OWNER TO postgres;

--
-- TOC entry 4083 (class 0 OID 0)
-- Dependencies: 257
-- Name: mitigation_action_mitigation_ingei_compliances_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitigation_action_mitigation_ingei_compliances_id_seq OWNED BY public.mitigation_action_mitigation_ingei_compliances.id;


--
-- TOC entry 234 (class 1259 OID 113679)
-- Name: mitigation_action_progressindicator; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitigation_action_progressindicator (
    id integer NOT NULL,
    type character varying(100) NOT NULL,
    unit character varying(100) NOT NULL,
    start_date date NOT NULL,
    name character varying(100) NOT NULL
);


ALTER TABLE public.mitigation_action_progressindicator OWNER TO postgres;

--
-- TOC entry 233 (class 1259 OID 113677)
-- Name: mitigation_action_progressindicator_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mitigation_action_progressindicator_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mitigation_action_progressindicator_id_seq OWNER TO postgres;

--
-- TOC entry 4084 (class 0 OID 0)
-- Dependencies: 233
-- Name: mitigation_action_progressindicator_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitigation_action_progressindicator_id_seq OWNED BY public.mitigation_action_progressindicator.id;


--
-- TOC entry 236 (class 1259 OID 113687)
-- Name: mitigation_action_registrationtype; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitigation_action_registrationtype (
    id integer NOT NULL,
    type_en character varying(100) NOT NULL,
    type_es character varying(100) NOT NULL,
    type_key character varying(20) NOT NULL
);


ALTER TABLE public.mitigation_action_registrationtype OWNER TO postgres;

--
-- TOC entry 235 (class 1259 OID 113685)
-- Name: mitigation_action_registrationtype_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mitigation_action_registrationtype_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mitigation_action_registrationtype_id_seq OWNER TO postgres;

--
-- TOC entry 4085 (class 0 OID 0)
-- Dependencies: 235
-- Name: mitigation_action_registrationtype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitigation_action_registrationtype_id_seq OWNED BY public.mitigation_action_registrationtype.id;


--
-- TOC entry 238 (class 1259 OID 113695)
-- Name: mitigation_action_status; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitigation_action_status (
    id integer NOT NULL,
    status_en character varying(100) NOT NULL,
    status_es character varying(100) NOT NULL
);


ALTER TABLE public.mitigation_action_status OWNER TO postgres;

--
-- TOC entry 237 (class 1259 OID 113693)
-- Name: mitigation_action_status_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mitigation_action_status_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mitigation_action_status_id_seq OWNER TO postgres;

--
-- TOC entry 4086 (class 0 OID 0)
-- Dependencies: 237
-- Name: mitigation_action_status_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitigation_action_status_id_seq OWNED BY public.mitigation_action_status.id;


--
-- TOC entry 310 (class 1259 OID 114597)
-- Name: ppcn_changelog; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ppcn_changelog (
    id integer NOT NULL,
    date timestamp with time zone NOT NULL,
    previous_status character varying(100),
    current_status character varying(100) NOT NULL,
    ppcn_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.ppcn_changelog OWNER TO postgres;

--
-- TOC entry 309 (class 1259 OID 114595)
-- Name: ppcn_changelog_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ppcn_changelog_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ppcn_changelog_id_seq OWNER TO postgres;

--
-- TOC entry 4087 (class 0 OID 0)
-- Dependencies: 309
-- Name: ppcn_changelog_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ppcn_changelog_id_seq OWNED BY public.ppcn_changelog.id;


--
-- TOC entry 278 (class 1259 OID 114318)
-- Name: ppcn_emissionfactor; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ppcn_emissionfactor (
    id integer NOT NULL,
    name character varying(200) NOT NULL
);


ALTER TABLE public.ppcn_emissionfactor OWNER TO postgres;

--
-- TOC entry 277 (class 1259 OID 114316)
-- Name: ppcn_emissionfactor_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ppcn_emissionfactor_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ppcn_emissionfactor_id_seq OWNER TO postgres;

--
-- TOC entry 4088 (class 0 OID 0)
-- Dependencies: 277
-- Name: ppcn_emissionfactor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ppcn_emissionfactor_id_seq OWNED BY public.ppcn_emissionfactor.id;


--
-- TOC entry 314 (class 1259 OID 114658)
-- Name: ppcn_geiactivitytype; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ppcn_geiactivitytype (
    id integer NOT NULL,
    activity_type character varying(500) NOT NULL,
    sector_id integer NOT NULL,
    sub_sector_id integer NOT NULL
);


ALTER TABLE public.ppcn_geiactivitytype OWNER TO postgres;

--
-- TOC entry 313 (class 1259 OID 114656)
-- Name: ppcn_geiactivitytype_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ppcn_geiactivitytype_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ppcn_geiactivitytype_id_seq OWNER TO postgres;

--
-- TOC entry 4089 (class 0 OID 0)
-- Dependencies: 313
-- Name: ppcn_geiactivitytype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ppcn_geiactivitytype_id_seq OWNED BY public.ppcn_geiactivitytype.id;


--
-- TOC entry 292 (class 1259 OID 114403)
-- Name: ppcn_geiorganization; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ppcn_geiorganization (
    id integer NOT NULL,
    ovv_id integer NOT NULL,
    emission_ovv_date date NOT NULL,
    report_year integer NOT NULL,
    base_year integer NOT NULL
);


ALTER TABLE public.ppcn_geiorganization OWNER TO postgres;

--
-- TOC entry 316 (class 1259 OID 114679)
-- Name: ppcn_geiorganization_gei_activity_types; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ppcn_geiorganization_gei_activity_types (
    id integer NOT NULL,
    geiorganization_id integer NOT NULL,
    geiactivitytype_id integer NOT NULL
);


ALTER TABLE public.ppcn_geiorganization_gei_activity_types OWNER TO postgres;

--
-- TOC entry 315 (class 1259 OID 114677)
-- Name: ppcn_geiorganization_gei_activity_types_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ppcn_geiorganization_gei_activity_types_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ppcn_geiorganization_gei_activity_types_id_seq OWNER TO postgres;

--
-- TOC entry 4090 (class 0 OID 0)
-- Dependencies: 315
-- Name: ppcn_geiorganization_gei_activity_types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ppcn_geiorganization_gei_activity_types_id_seq OWNED BY public.ppcn_geiorganization_gei_activity_types.id;


--
-- TOC entry 291 (class 1259 OID 114401)
-- Name: ppcn_geiorganization_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ppcn_geiorganization_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ppcn_geiorganization_id_seq OWNER TO postgres;

--
-- TOC entry 4091 (class 0 OID 0)
-- Dependencies: 291
-- Name: ppcn_geiorganization_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ppcn_geiorganization_id_seq OWNED BY public.ppcn_geiorganization.id;


--
-- TOC entry 282 (class 1259 OID 114334)
-- Name: ppcn_geographiclevel; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ppcn_geographiclevel (
    id integer NOT NULL,
    level_es character varying(200) NOT NULL,
    level_en character varying(200) NOT NULL
);


ALTER TABLE public.ppcn_geographiclevel OWNER TO postgres;

--
-- TOC entry 280 (class 1259 OID 114326)
-- Name: ppcn_inventorymethodology; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ppcn_inventorymethodology (
    id integer NOT NULL,
    name character varying(200) NOT NULL
);


ALTER TABLE public.ppcn_inventorymethodology OWNER TO postgres;

--
-- TOC entry 279 (class 1259 OID 114324)
-- Name: ppcn_inventorymethodology_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ppcn_inventorymethodology_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ppcn_inventorymethodology_id_seq OWNER TO postgres;

--
-- TOC entry 4092 (class 0 OID 0)
-- Dependencies: 279
-- Name: ppcn_inventorymethodology_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ppcn_inventorymethodology_id_seq OWNED BY public.ppcn_inventorymethodology.id;


--
-- TOC entry 281 (class 1259 OID 114332)
-- Name: ppcn_level_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ppcn_level_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ppcn_level_id_seq OWNER TO postgres;

--
-- TOC entry 4093 (class 0 OID 0)
-- Dependencies: 281
-- Name: ppcn_level_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ppcn_level_id_seq OWNED BY public.ppcn_geographiclevel.id;


--
-- TOC entry 284 (class 1259 OID 114342)
-- Name: ppcn_organization; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ppcn_organization (
    id integer NOT NULL,
    name character varying(200) NOT NULL,
    representative_name character varying(200) NOT NULL,
    postal_code character varying(200),
    fax character varying(200),
    address character varying(200) NOT NULL,
    ciiu character varying(200),
    contact_id integer NOT NULL,
    phone_organization character varying(200)
);


ALTER TABLE public.ppcn_organization OWNER TO postgres;

--
-- TOC entry 283 (class 1259 OID 114340)
-- Name: ppcn_organization_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ppcn_organization_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ppcn_organization_id_seq OWNER TO postgres;

--
-- TOC entry 4094 (class 0 OID 0)
-- Dependencies: 283
-- Name: ppcn_organization_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ppcn_organization_id_seq OWNED BY public.ppcn_organization.id;


--
-- TOC entry 286 (class 1259 OID 114353)
-- Name: ppcn_plusaction; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ppcn_plusaction (
    id integer NOT NULL,
    name character varying(200) NOT NULL
);


ALTER TABLE public.ppcn_plusaction OWNER TO postgres;

--
-- TOC entry 285 (class 1259 OID 114351)
-- Name: ppcn_plusaction_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ppcn_plusaction_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ppcn_plusaction_id_seq OWNER TO postgres;

--
-- TOC entry 4095 (class 0 OID 0)
-- Dependencies: 285
-- Name: ppcn_plusaction_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ppcn_plusaction_id_seq OWNED BY public.ppcn_plusaction.id;


--
-- TOC entry 288 (class 1259 OID 114361)
-- Name: ppcn_potentialglobalwarming; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ppcn_potentialglobalwarming (
    id integer NOT NULL,
    name character varying(200) NOT NULL
);


ALTER TABLE public.ppcn_potentialglobalwarming OWNER TO postgres;

--
-- TOC entry 287 (class 1259 OID 114359)
-- Name: ppcn_potentialglobalwarming_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ppcn_potentialglobalwarming_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ppcn_potentialglobalwarming_id_seq OWNER TO postgres;

--
-- TOC entry 4096 (class 0 OID 0)
-- Dependencies: 287
-- Name: ppcn_potentialglobalwarming_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ppcn_potentialglobalwarming_id_seq OWNED BY public.ppcn_potentialglobalwarming.id;


--
-- TOC entry 304 (class 1259 OID 114469)
-- Name: ppcn_ppcn; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ppcn_ppcn (
    id integer NOT NULL,
    organization_id integer,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    user_id integer NOT NULL,
    fsm_state character varying(50) NOT NULL,
    review_count integer,
    gei_organization_id integer,
    geographic_level_id integer,
    recognition_type_id integer,
    required_level_id integer
);


ALTER TABLE public.ppcn_ppcn OWNER TO postgres;

--
-- TOC entry 312 (class 1259 OID 114605)
-- Name: ppcn_ppcn_comments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ppcn_ppcn_comments (
    id integer NOT NULL,
    ppcn_id integer NOT NULL,
    comment_id integer NOT NULL
);


ALTER TABLE public.ppcn_ppcn_comments OWNER TO postgres;

--
-- TOC entry 311 (class 1259 OID 114603)
-- Name: ppcn_ppcn_comments_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ppcn_ppcn_comments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ppcn_ppcn_comments_id_seq OWNER TO postgres;

--
-- TOC entry 4097 (class 0 OID 0)
-- Dependencies: 311
-- Name: ppcn_ppcn_comments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ppcn_ppcn_comments_id_seq OWNED BY public.ppcn_ppcn_comments.id;


--
-- TOC entry 303 (class 1259 OID 114467)
-- Name: ppcn_ppcn_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ppcn_ppcn_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ppcn_ppcn_id_seq OWNER TO postgres;

--
-- TOC entry 4098 (class 0 OID 0)
-- Dependencies: 303
-- Name: ppcn_ppcn_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ppcn_ppcn_id_seq OWNED BY public.ppcn_ppcn.id;


--
-- TOC entry 302 (class 1259 OID 114461)
-- Name: ppcn_ppcnfile; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ppcn_ppcnfile (
    id integer NOT NULL,
    file character varying(100) NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    ppcn_form_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.ppcn_ppcnfile OWNER TO postgres;

--
-- TOC entry 301 (class 1259 OID 114459)
-- Name: ppcn_ppcnfile_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ppcn_ppcnfile_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ppcn_ppcnfile_id_seq OWNER TO postgres;

--
-- TOC entry 4099 (class 0 OID 0)
-- Dependencies: 301
-- Name: ppcn_ppcnfile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ppcn_ppcnfile_id_seq OWNED BY public.ppcn_ppcnfile.id;


--
-- TOC entry 306 (class 1259 OID 114557)
-- Name: ppcn_ppcnworkflowstep; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ppcn_ppcnworkflowstep (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    entry_name character varying(100) NOT NULL,
    status character varying(50) NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    ppcn_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.ppcn_ppcnworkflowstep OWNER TO postgres;

--
-- TOC entry 305 (class 1259 OID 114555)
-- Name: ppcn_ppcnworkflowstep_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ppcn_ppcnworkflowstep_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ppcn_ppcnworkflowstep_id_seq OWNER TO postgres;

--
-- TOC entry 4100 (class 0 OID 0)
-- Dependencies: 305
-- Name: ppcn_ppcnworkflowstep_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ppcn_ppcnworkflowstep_id_seq OWNED BY public.ppcn_ppcnworkflowstep.id;


--
-- TOC entry 308 (class 1259 OID 114565)
-- Name: ppcn_ppcnworkflowstepfile; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ppcn_ppcnworkflowstepfile (
    id integer NOT NULL,
    file character varying(100) NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    user_id integer NOT NULL,
    workflow_step_id integer NOT NULL
);


ALTER TABLE public.ppcn_ppcnworkflowstepfile OWNER TO postgres;

--
-- TOC entry 307 (class 1259 OID 114563)
-- Name: ppcn_ppcnworkflowstepfile_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ppcn_ppcnworkflowstepfile_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ppcn_ppcnworkflowstepfile_id_seq OWNER TO postgres;

--
-- TOC entry 4101 (class 0 OID 0)
-- Dependencies: 307
-- Name: ppcn_ppcnworkflowstepfile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ppcn_ppcnworkflowstepfile_id_seq OWNED BY public.ppcn_ppcnworkflowstepfile.id;


--
-- TOC entry 290 (class 1259 OID 114369)
-- Name: ppcn_quantifiedgas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ppcn_quantifiedgas (
    id integer NOT NULL,
    name character varying(200) NOT NULL
);


ALTER TABLE public.ppcn_quantifiedgas OWNER TO postgres;

--
-- TOC entry 289 (class 1259 OID 114367)
-- Name: ppcn_quantifiedgas_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ppcn_quantifiedgas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ppcn_quantifiedgas_id_seq OWNER TO postgres;

--
-- TOC entry 4102 (class 0 OID 0)
-- Dependencies: 289
-- Name: ppcn_quantifiedgas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ppcn_quantifiedgas_id_seq OWNED BY public.ppcn_quantifiedgas.id;


--
-- TOC entry 294 (class 1259 OID 114411)
-- Name: ppcn_recognitiontype; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ppcn_recognitiontype (
    id integer NOT NULL,
    recognition_type_es character varying(200) NOT NULL,
    recognition_type_en character varying(200) NOT NULL
);


ALTER TABLE public.ppcn_recognitiontype OWNER TO postgres;

--
-- TOC entry 293 (class 1259 OID 114409)
-- Name: ppcn_recognitiontype_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ppcn_recognitiontype_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ppcn_recognitiontype_id_seq OWNER TO postgres;

--
-- TOC entry 4103 (class 0 OID 0)
-- Dependencies: 293
-- Name: ppcn_recognitiontype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ppcn_recognitiontype_id_seq OWNED BY public.ppcn_recognitiontype.id;


--
-- TOC entry 296 (class 1259 OID 114419)
-- Name: ppcn_requiredlevel; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ppcn_requiredlevel (
    id integer NOT NULL,
    level_type_es character varying(200) NOT NULL,
    level_type_en character varying(200) NOT NULL
);


ALTER TABLE public.ppcn_requiredlevel OWNER TO postgres;

--
-- TOC entry 295 (class 1259 OID 114417)
-- Name: ppcn_requiredlevel_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ppcn_requiredlevel_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ppcn_requiredlevel_id_seq OWNER TO postgres;

--
-- TOC entry 4104 (class 0 OID 0)
-- Dependencies: 295
-- Name: ppcn_requiredlevel_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ppcn_requiredlevel_id_seq OWNED BY public.ppcn_requiredlevel.id;


--
-- TOC entry 298 (class 1259 OID 114427)
-- Name: ppcn_sector; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ppcn_sector (
    id integer NOT NULL,
    name_es character varying(200) NOT NULL,
    name_en character varying(200) NOT NULL,
    "geographicLevel_id" integer NOT NULL
);


ALTER TABLE public.ppcn_sector OWNER TO postgres;

--
-- TOC entry 297 (class 1259 OID 114425)
-- Name: ppcn_sector_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ppcn_sector_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ppcn_sector_id_seq OWNER TO postgres;

--
-- TOC entry 4105 (class 0 OID 0)
-- Dependencies: 297
-- Name: ppcn_sector_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ppcn_sector_id_seq OWNED BY public.ppcn_sector.id;


--
-- TOC entry 300 (class 1259 OID 114435)
-- Name: ppcn_subsector; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ppcn_subsector (
    id integer NOT NULL,
    name_es character varying(200) NOT NULL,
    name_en character varying(200) NOT NULL,
    sector_id integer NOT NULL
);


ALTER TABLE public.ppcn_subsector OWNER TO postgres;

--
-- TOC entry 299 (class 1259 OID 114433)
-- Name: ppcn_subsector_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ppcn_subsector_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ppcn_subsector_id_seq OWNER TO postgres;

--
-- TOC entry 4106 (class 0 OID 0)
-- Dependencies: 299
-- Name: ppcn_subsector_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ppcn_subsector_id_seq OWNED BY public.ppcn_subsector.id;


--
-- TOC entry 318 (class 1259 OID 114736)
-- Name: report_data_reportfile; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.report_data_reportfile (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.report_data_reportfile OWNER TO postgres;

--
-- TOC entry 317 (class 1259 OID 114734)
-- Name: report_data_reportfile_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.report_data_reportfile_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.report_data_reportfile_id_seq OWNER TO postgres;

--
-- TOC entry 4107 (class 0 OID 0)
-- Dependencies: 317
-- Name: report_data_reportfile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.report_data_reportfile_id_seq OWNED BY public.report_data_reportfile.id;


--
-- TOC entry 322 (class 1259 OID 114805)
-- Name: report_data_reportfilemetadata; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.report_data_reportfilemetadata (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    value character varying(100) NOT NULL,
    report_file_id integer NOT NULL
);


ALTER TABLE public.report_data_reportfilemetadata OWNER TO postgres;

--
-- TOC entry 321 (class 1259 OID 114803)
-- Name: report_data_reportfilemetadata_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.report_data_reportfilemetadata_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.report_data_reportfilemetadata_id_seq OWNER TO postgres;

--
-- TOC entry 4108 (class 0 OID 0)
-- Dependencies: 321
-- Name: report_data_reportfilemetadata_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.report_data_reportfilemetadata_id_seq OWNED BY public.report_data_reportfilemetadata.id;


--
-- TOC entry 320 (class 1259 OID 114748)
-- Name: report_data_reportfileversion; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.report_data_reportfileversion (
    id integer NOT NULL,
    active boolean NOT NULL,
    version character varying(100) NOT NULL,
    file character varying(100) NOT NULL,
    report_file_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.report_data_reportfileversion OWNER TO postgres;

--
-- TOC entry 319 (class 1259 OID 114746)
-- Name: report_data_reportfileversion_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.report_data_reportfileversion_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.report_data_reportfileversion_id_seq OWNER TO postgres;

--
-- TOC entry 4109 (class 0 OID 0)
-- Dependencies: 319
-- Name: report_data_reportfileversion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.report_data_reportfileversion_id_seq OWNED BY public.report_data_reportfileversion.id;


--
-- TOC entry 213 (class 1259 OID 113537)
-- Name: users_customuser; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users_customuser (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL,
    is_administrador_dcc boolean NOT NULL,
    is_provider boolean NOT NULL,
    phone character varying(50)
);


ALTER TABLE public.users_customuser OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 113550)
-- Name: users_customuser_groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users_customuser_groups (
    id integer NOT NULL,
    customuser_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.users_customuser_groups OWNER TO postgres;

--
-- TOC entry 214 (class 1259 OID 113548)
-- Name: users_customuser_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_customuser_groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_customuser_groups_id_seq OWNER TO postgres;

--
-- TOC entry 4110 (class 0 OID 0)
-- Dependencies: 214
-- Name: users_customuser_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_customuser_groups_id_seq OWNED BY public.users_customuser_groups.id;


--
-- TOC entry 212 (class 1259 OID 113535)
-- Name: users_customuser_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_customuser_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_customuser_id_seq OWNER TO postgres;

--
-- TOC entry 4111 (class 0 OID 0)
-- Dependencies: 212
-- Name: users_customuser_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_customuser_id_seq OWNED BY public.users_customuser.id;


--
-- TOC entry 217 (class 1259 OID 113558)
-- Name: users_customuser_user_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users_customuser_user_permissions (
    id integer NOT NULL,
    customuser_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.users_customuser_user_permissions OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 113556)
-- Name: users_customuser_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_customuser_user_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_customuser_user_permissions_id_seq OWNER TO postgres;

--
-- TOC entry 4112 (class 0 OID 0)
-- Dependencies: 216
-- Name: users_customuser_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_customuser_user_permissions_id_seq OWNED BY public.users_customuser_user_permissions.id;


--
-- TOC entry 254 (class 1259 OID 113921)
-- Name: workflow_comment; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.workflow_comment (
    id integer NOT NULL,
    comment character varying(3000) NOT NULL
);


ALTER TABLE public.workflow_comment OWNER TO postgres;

--
-- TOC entry 253 (class 1259 OID 113919)
-- Name: workflow_comment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.workflow_comment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.workflow_comment_id_seq OWNER TO postgres;

--
-- TOC entry 4113 (class 0 OID 0)
-- Dependencies: 253
-- Name: workflow_comment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.workflow_comment_id_seq OWNED BY public.workflow_comment.id;


--
-- TOC entry 256 (class 1259 OID 113929)
-- Name: workflow_reviewstatus; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.workflow_reviewstatus (
    id integer NOT NULL,
    status character varying(100) NOT NULL
);


ALTER TABLE public.workflow_reviewstatus OWNER TO postgres;

--
-- TOC entry 255 (class 1259 OID 113927)
-- Name: workflow_reviewstatus_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.workflow_reviewstatus_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.workflow_reviewstatus_id_seq OWNER TO postgres;

--
-- TOC entry 4114 (class 0 OID 0)
-- Dependencies: 255
-- Name: workflow_reviewstatus_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.workflow_reviewstatus_id_seq OWNED BY public.workflow_reviewstatus.id;


--
-- TOC entry 3437 (class 2604 OID 113499)
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- TOC entry 3438 (class 2604 OID 113509)
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- TOC entry 3436 (class 2604 OID 113491)
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- TOC entry 3442 (class 2604 OID 113598)
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- TOC entry 3435 (class 2604 OID 113481)
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- TOC entry 3434 (class 2604 OID 113470)
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- TOC entry 3456 (class 2604 OID 113858)
-- Name: mccr_changelog id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_changelog ALTER COLUMN id SET DEFAULT nextval('public.mccr_changelog_id_seq'::regclass);


--
-- TOC entry 3454 (class 2604 OID 113828)
-- Name: mccr_mccrregistryovvrelation id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_mccrregistryovvrelation ALTER COLUMN id SET DEFAULT nextval('public.mccr_mccrregistryovvrelation_id_seq'::regclass);


--
-- TOC entry 3453 (class 2604 OID 113801)
-- Name: mccr_mccrusertype id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_mccrusertype ALTER COLUMN id SET DEFAULT nextval('public.mccr_mccrusertype_id_seq'::regclass);


--
-- TOC entry 3457 (class 2604 OID 113866)
-- Name: mccr_mccrworkflowstep id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_mccrworkflowstep ALTER COLUMN id SET DEFAULT nextval('public.mccr_mccrworkflowstep_id_seq'::regclass);


--
-- TOC entry 3458 (class 2604 OID 113874)
-- Name: mccr_mccrworkflowstepfile id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_mccrworkflowstepfile ALTER COLUMN id SET DEFAULT nextval('public.mccr_mccrworkflowstepfile_id_seq'::regclass);


--
-- TOC entry 3455 (class 2604 OID 113836)
-- Name: mccr_ovv id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_ovv ALTER COLUMN id SET DEFAULT nextval('public.mccr_ovv_id_seq'::regclass);


--
-- TOC entry 3462 (class 2604 OID 113963)
-- Name: mitigation_action_changelog id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_changelog ALTER COLUMN id SET DEFAULT nextval('public.mitigation_action_changelog_id_seq'::regclass);


--
-- TOC entry 3444 (class 2604 OID 113623)
-- Name: mitigation_action_contact id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_contact ALTER COLUMN id SET DEFAULT nextval('public.mitigation_action_contact_id_seq'::regclass);


--
-- TOC entry 3445 (class 2604 OID 113634)
-- Name: mitigation_action_finance id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_finance ALTER COLUMN id SET DEFAULT nextval('public.mitigation_action_finance_id_seq'::regclass);


--
-- TOC entry 3464 (class 2604 OID 114026)
-- Name: mitigation_action_financesourcetype id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_financesourcetype ALTER COLUMN id SET DEFAULT nextval('public.mitigation_action_financesourcetype_id_seq'::regclass);


--
-- TOC entry 3467 (class 2604 OID 114192)
-- Name: mitigation_action_financestatus id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_financestatus ALTER COLUMN id SET DEFAULT nextval('public.mitigation_action_financestatus_id_seq'::regclass);


--
-- TOC entry 3446 (class 2604 OID 113642)
-- Name: mitigation_action_geographicscale id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_geographicscale ALTER COLUMN id SET DEFAULT nextval('public.mitigation_action_geographicscale_id_seq'::regclass);


--
-- TOC entry 3447 (class 2604 OID 113650)
-- Name: mitigation_action_ingeicompliance id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_ingeicompliance ALTER COLUMN id SET DEFAULT nextval('public.mitigation_action_ingeicompliance_id_seq'::regclass);


--
-- TOC entry 3468 (class 2604 OID 114200)
-- Name: mitigation_action_initiative id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_initiative ALTER COLUMN id SET DEFAULT nextval('public.mitigation_action_initiative_id_seq'::regclass);


--
-- TOC entry 3469 (class 2604 OID 114211)
-- Name: mitigation_action_initiativefinance id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_initiativefinance ALTER COLUMN id SET DEFAULT nextval('public.mitigation_action_initiativefinance_id_seq'::regclass);


--
-- TOC entry 3470 (class 2604 OID 114219)
-- Name: mitigation_action_initiativetype id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_initiativetype ALTER COLUMN id SET DEFAULT nextval('public.mitigation_action_initiativetype_id_seq'::regclass);


--
-- TOC entry 3448 (class 2604 OID 113658)
-- Name: mitigation_action_institution id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_institution ALTER COLUMN id SET DEFAULT nextval('public.mitigation_action_institution_id_seq'::regclass);


--
-- TOC entry 3449 (class 2604 OID 113666)
-- Name: mitigation_action_location id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_location ALTER COLUMN id SET DEFAULT nextval('public.mitigation_action_location_id_seq'::regclass);


--
-- TOC entry 3465 (class 2604 OID 114132)
-- Name: mitigation_action_maworkflowstep id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_maworkflowstep ALTER COLUMN id SET DEFAULT nextval('public.mitigation_action_maworkflowstep_id_seq'::regclass);


--
-- TOC entry 3466 (class 2604 OID 114140)
-- Name: mitigation_action_maworkflowstepfile id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_maworkflowstepfile ALTER COLUMN id SET DEFAULT nextval('public.mitigation_action_maworkflowstepfile_id_seq'::regclass);


--
-- TOC entry 3463 (class 2604 OID 113971)
-- Name: mitigation_action_mitigation_comments id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_mitigation_comments ALTER COLUMN id SET DEFAULT nextval('public.mitigation_action_mitigation_comments_id_seq'::regclass);


--
-- TOC entry 3461 (class 2604 OID 113941)
-- Name: mitigation_action_mitigation_ingei_compliances id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_mitigation_ingei_compliances ALTER COLUMN id SET DEFAULT nextval('public.mitigation_action_mitigation_ingei_compliances_id_seq'::regclass);


--
-- TOC entry 3450 (class 2604 OID 113682)
-- Name: mitigation_action_progressindicator id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_progressindicator ALTER COLUMN id SET DEFAULT nextval('public.mitigation_action_progressindicator_id_seq'::regclass);


--
-- TOC entry 3451 (class 2604 OID 113690)
-- Name: mitigation_action_registrationtype id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_registrationtype ALTER COLUMN id SET DEFAULT nextval('public.mitigation_action_registrationtype_id_seq'::regclass);


--
-- TOC entry 3452 (class 2604 OID 113698)
-- Name: mitigation_action_status id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_status ALTER COLUMN id SET DEFAULT nextval('public.mitigation_action_status_id_seq'::regclass);


--
-- TOC entry 3487 (class 2604 OID 114600)
-- Name: ppcn_changelog id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_changelog ALTER COLUMN id SET DEFAULT nextval('public.ppcn_changelog_id_seq'::regclass);


--
-- TOC entry 3471 (class 2604 OID 114321)
-- Name: ppcn_emissionfactor id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_emissionfactor ALTER COLUMN id SET DEFAULT nextval('public.ppcn_emissionfactor_id_seq'::regclass);


--
-- TOC entry 3489 (class 2604 OID 114661)
-- Name: ppcn_geiactivitytype id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_geiactivitytype ALTER COLUMN id SET DEFAULT nextval('public.ppcn_geiactivitytype_id_seq'::regclass);


--
-- TOC entry 3478 (class 2604 OID 114406)
-- Name: ppcn_geiorganization id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_geiorganization ALTER COLUMN id SET DEFAULT nextval('public.ppcn_geiorganization_id_seq'::regclass);


--
-- TOC entry 3490 (class 2604 OID 114682)
-- Name: ppcn_geiorganization_gei_activity_types id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_geiorganization_gei_activity_types ALTER COLUMN id SET DEFAULT nextval('public.ppcn_geiorganization_gei_activity_types_id_seq'::regclass);


--
-- TOC entry 3473 (class 2604 OID 114337)
-- Name: ppcn_geographiclevel id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_geographiclevel ALTER COLUMN id SET DEFAULT nextval('public.ppcn_level_id_seq'::regclass);


--
-- TOC entry 3472 (class 2604 OID 114329)
-- Name: ppcn_inventorymethodology id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_inventorymethodology ALTER COLUMN id SET DEFAULT nextval('public.ppcn_inventorymethodology_id_seq'::regclass);


--
-- TOC entry 3474 (class 2604 OID 114345)
-- Name: ppcn_organization id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_organization ALTER COLUMN id SET DEFAULT nextval('public.ppcn_organization_id_seq'::regclass);


--
-- TOC entry 3475 (class 2604 OID 114356)
-- Name: ppcn_plusaction id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_plusaction ALTER COLUMN id SET DEFAULT nextval('public.ppcn_plusaction_id_seq'::regclass);


--
-- TOC entry 3476 (class 2604 OID 114364)
-- Name: ppcn_potentialglobalwarming id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_potentialglobalwarming ALTER COLUMN id SET DEFAULT nextval('public.ppcn_potentialglobalwarming_id_seq'::regclass);


--
-- TOC entry 3484 (class 2604 OID 114472)
-- Name: ppcn_ppcn id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcn ALTER COLUMN id SET DEFAULT nextval('public.ppcn_ppcn_id_seq'::regclass);


--
-- TOC entry 3488 (class 2604 OID 114608)
-- Name: ppcn_ppcn_comments id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcn_comments ALTER COLUMN id SET DEFAULT nextval('public.ppcn_ppcn_comments_id_seq'::regclass);


--
-- TOC entry 3483 (class 2604 OID 114464)
-- Name: ppcn_ppcnfile id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcnfile ALTER COLUMN id SET DEFAULT nextval('public.ppcn_ppcnfile_id_seq'::regclass);


--
-- TOC entry 3485 (class 2604 OID 114560)
-- Name: ppcn_ppcnworkflowstep id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcnworkflowstep ALTER COLUMN id SET DEFAULT nextval('public.ppcn_ppcnworkflowstep_id_seq'::regclass);


--
-- TOC entry 3486 (class 2604 OID 114568)
-- Name: ppcn_ppcnworkflowstepfile id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcnworkflowstepfile ALTER COLUMN id SET DEFAULT nextval('public.ppcn_ppcnworkflowstepfile_id_seq'::regclass);


--
-- TOC entry 3477 (class 2604 OID 114372)
-- Name: ppcn_quantifiedgas id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_quantifiedgas ALTER COLUMN id SET DEFAULT nextval('public.ppcn_quantifiedgas_id_seq'::regclass);


--
-- TOC entry 3479 (class 2604 OID 114414)
-- Name: ppcn_recognitiontype id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_recognitiontype ALTER COLUMN id SET DEFAULT nextval('public.ppcn_recognitiontype_id_seq'::regclass);


--
-- TOC entry 3480 (class 2604 OID 114422)
-- Name: ppcn_requiredlevel id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_requiredlevel ALTER COLUMN id SET DEFAULT nextval('public.ppcn_requiredlevel_id_seq'::regclass);


--
-- TOC entry 3481 (class 2604 OID 114430)
-- Name: ppcn_sector id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_sector ALTER COLUMN id SET DEFAULT nextval('public.ppcn_sector_id_seq'::regclass);


--
-- TOC entry 3482 (class 2604 OID 114438)
-- Name: ppcn_subsector id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_subsector ALTER COLUMN id SET DEFAULT nextval('public.ppcn_subsector_id_seq'::regclass);


--
-- TOC entry 3491 (class 2604 OID 114739)
-- Name: report_data_reportfile id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_data_reportfile ALTER COLUMN id SET DEFAULT nextval('public.report_data_reportfile_id_seq'::regclass);


--
-- TOC entry 3493 (class 2604 OID 114808)
-- Name: report_data_reportfilemetadata id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_data_reportfilemetadata ALTER COLUMN id SET DEFAULT nextval('public.report_data_reportfilemetadata_id_seq'::regclass);


--
-- TOC entry 3492 (class 2604 OID 114751)
-- Name: report_data_reportfileversion id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_data_reportfileversion ALTER COLUMN id SET DEFAULT nextval('public.report_data_reportfileversion_id_seq'::regclass);


--
-- TOC entry 3439 (class 2604 OID 113540)
-- Name: users_customuser id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_customuser ALTER COLUMN id SET DEFAULT nextval('public.users_customuser_id_seq'::regclass);


--
-- TOC entry 3440 (class 2604 OID 113553)
-- Name: users_customuser_groups id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_customuser_groups ALTER COLUMN id SET DEFAULT nextval('public.users_customuser_groups_id_seq'::regclass);


--
-- TOC entry 3441 (class 2604 OID 113561)
-- Name: users_customuser_user_permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_customuser_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.users_customuser_user_permissions_id_seq'::regclass);


--
-- TOC entry 3459 (class 2604 OID 113924)
-- Name: workflow_comment id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflow_comment ALTER COLUMN id SET DEFAULT nextval('public.workflow_comment_id_seq'::regclass);


--
-- TOC entry 3460 (class 2604 OID 113932)
-- Name: workflow_reviewstatus id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflow_reviewstatus ALTER COLUMN id SET DEFAULT nextval('public.workflow_reviewstatus_id_seq'::regclass);


--
-- TOC entry 3936 (class 0 OID 113496)
-- Dependencies: 209
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group (id, name) FROM stdin;
1	admin
2	reviewer
3	information_provider
\.


--
-- TOC entry 3938 (class 0 OID 113506)
-- Dependencies: 211
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- TOC entry 3934 (class 0 OID 113488)
-- Dependencies: 207
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	user DCC permision MCCR	1	user_dcc_permission
2	user executive secretary permission MCCR	1	user_executive_secretary_permission
3	User Validating Organizations MCCR	1	user_validating_organizations_permission
4	Can provide information MCCR	1	can_provide_information
5	User Executive Committee MCCR	1	user_executive_committee_permissions
6	Can Provide Information MA	2	can_provide_information
7	User DCC Permission MA	2	user_dcc_permission
8	User Executive Secretary Permission MA	2	user_executive_secretary_permission
9	user executive secretary permission PPCN	3	user_executive_secretary_permission
10	user DCC permision PPCN	3	user_dcc_permission
11	user CA permission PPCN	3	user_ca_permission
12	Can provide information ppcn	3	can_provide_information
13	Read Mitigation Action	4	read_mitigation_action
14	Delete Mitigation Action	4	delete_mitigation_action
15	Edit Mitigation Action	4	edit_mitigation_action
16	Edit Ppcn	4	edit_ppcn
17	Create Mccr	4	create_mccr
18	Delete Ppcn	4	delete_ppcn
19	Create Mitigation Action	4	create_mitigation_action
20	Delete Mccr	4	delete_mccr
21	Read Mccr	4	read_mccr
22	Read User	4	read_user
23	Read All Mitigation Action	4	read_all_mitigation_action
24	Create Ppcn	4	create_ppcn
25	Read All Mccr	4	read_all_mccr
26	Delete User	4	delete_user
27	Read All Ppcn	4	read_all_ppcn
28	Read Ppcn	4	read_ppcn
29	Create User	4	create_user
30	Edit Mccr	4	edit_mccr
31	Edit User	4	edit_user
32	Can add log entry	5	add_logentry
33	Can change log entry	5	change_logentry
34	Can delete log entry	5	delete_logentry
35	Can add permission	6	add_permission
36	Can change permission	6	change_permission
37	Can delete permission	6	delete_permission
38	Can add group	7	add_group
39	Can change group	7	change_group
40	Can delete group	7	delete_group
41	Can add content type	8	add_contenttype
42	Can change content type	8	change_contenttype
43	Can delete content type	8	delete_contenttype
44	Can add session	9	add_session
45	Can change session	9	change_session
46	Can delete session	9	delete_session
47	Can add ReportFile	10	add_reportfile
48	Can change ReportFile	10	change_reportfile
49	Can delete ReportFile	10	delete_reportfile
50	Can add ReportFileVersion	11	add_reportfileversion
51	Can change ReportFileVersion	11	change_reportfileversion
52	Can delete ReportFileVersion	11	delete_reportfileversion
53	Can add ReportFileMetadata	12	add_reportfilemetadata
54	Can change ReportFileMetadata	12	change_reportfilemetadata
55	Can delete ReportFileMetadata	12	delete_reportfilemetadata
56	Can add Contact	13	add_contact
57	Can change Contact	13	change_contact
58	Can delete Contact	13	delete_contact
59	Can add Finance	14	add_finance
60	Can change Finance	14	change_finance
61	Can delete Finance	14	delete_finance
62	Can add GeographicScale	15	add_geographicscale
63	Can change GeographicScale	15	change_geographicscale
64	Can delete GeographicScale	15	delete_geographicscale
65	Can add IngeiCompliance	16	add_ingeicompliance
66	Can change IngeiCompliance	16	change_ingeicompliance
67	Can delete IngeiCompliance	16	delete_ingeicompliance
68	Can add Institution	17	add_institution
69	Can change Institution	17	change_institution
70	Can delete Institution	17	delete_institution
71	Can add Location	18	add_location
72	Can change Location	18	change_location
73	Can delete Location	18	delete_location
74	Can add ProgressIndicator	19	add_progressindicator
75	Can change ProgressIndicator	19	change_progressindicator
76	Can delete ProgressIndicator	19	delete_progressindicator
77	Can add RegistrationType	20	add_registrationtype
78	Can change RegistrationType	20	change_registrationtype
79	Can delete RegistrationType	20	delete_registrationtype
80	Can add Status	21	add_status
81	Can change Status	21	change_status
82	Can delete Status	21	delete_status
83	Can add MitigationAccess	2	add_mitigation
84	Can change MitigationAccess	2	change_mitigation
85	Can delete MitigationAccess	2	delete_mitigation
86	Can add ChangeLog	22	add_changelog
87	Can change ChangeLog	22	change_changelog
88	Can delete ChangeLog	22	delete_changelog
89	Can add FinanceSourceType	23	add_financesourcetype
90	Can change FinanceSourceType	23	change_financesourcetype
91	Can delete FinanceSourceType	23	delete_financesourcetype
92	Can add Workflow Step	24	add_maworkflowstep
93	Can change Workflow Step	24	change_maworkflowstep
94	Can delete Workflow Step	24	delete_maworkflowstep
95	Can add Workflow Step File	25	add_maworkflowstepfile
96	Can change Workflow Step File	25	change_maworkflowstepfile
97	Can delete Workflow Step File	25	delete_maworkflowstepfile
98	Can add FinanceStatus	26	add_financestatus
99	Can change FinanceStatus	26	change_financestatus
100	Can delete FinanceStatus	26	delete_financestatus
101	Can add Initiative	27	add_initiative
102	Can change Initiative	27	change_initiative
103	Can delete Initiative	27	delete_initiative
104	Can add InitiativeFinance	28	add_initiativefinance
105	Can change InitiativeFinance	28	change_initiativefinance
106	Can delete InitiativeFinance	28	delete_initiativefinance
107	Can add InitiativeType	29	add_initiativetype
108	Can change InitiativeType	29	change_initiativetype
109	Can delete InitiativeType	29	delete_initiativetype
110	Can add Comment	30	add_comment
111	Can change Comment	30	change_comment
112	Can delete Comment	30	delete_comment
113	Can add ReviewStatus	31	add_reviewstatus
114	Can change ReviewStatus	31	change_reviewstatus
115	Can delete ReviewStatus	31	delete_reviewstatus
116	Can add MCCRFile	32	add_mccrfile
117	Can change MCCRFile	32	change_mccrfile
118	Can delete MCCRFile	32	delete_mccrfile
119	Can add MCCRRegistry	1	add_mccrregistry
120	Can change MCCRRegistry	1	change_mccrregistry
121	Can delete MCCRRegistry	1	delete_mccrregistry
122	Can add MCCRUserType	33	add_mccrusertype
123	Can change MCCRUserType	33	change_mccrusertype
124	Can delete MCCRUserType	33	delete_mccrusertype
125	Can add MCCR OVV Relation	34	add_mccrregistryovvrelation
126	Can change MCCR OVV Relation	34	change_mccrregistryovvrelation
127	Can delete MCCR OVV Relation	34	delete_mccrregistryovvrelation
128	Can add Organismo Validador Verifador	35	add_ovv
129	Can change Organismo Validador Verifador	35	change_ovv
130	Can delete Organismo Validador Verifador	35	delete_ovv
131	Can add ChangeLog	36	add_changelog
132	Can change ChangeLog	36	change_changelog
133	Can delete ChangeLog	36	delete_changelog
134	Can add Workflow Step	37	add_mccrworkflowstep
135	Can change Workflow Step	37	change_mccrworkflowstep
136	Can delete Workflow Step	37	delete_mccrworkflowstep
137	Can add Workflow Step File	38	add_mccrworkflowstepfile
138	Can change Workflow Step File	38	change_mccrworkflowstepfile
139	Can delete Workflow Step File	38	delete_mccrworkflowstepfile
140	Can add EmissionFactor	39	add_emissionfactor
141	Can change EmissionFactor	39	change_emissionfactor
142	Can delete EmissionFactor	39	delete_emissionfactor
143	Can add InventoryMethodology	40	add_inventorymethodology
144	Can change InventoryMethodology	40	change_inventorymethodology
145	Can delete InventoryMethodology	40	delete_inventorymethodology
146	Can add Organization	41	add_organization
147	Can change Organization	41	change_organization
148	Can delete Organization	41	delete_organization
149	Can add PlusAction	42	add_plusaction
150	Can change PlusAction	42	change_plusaction
151	Can delete PlusAction	42	delete_plusaction
152	Can add PotentialGlobalWarming	43	add_potentialglobalwarming
153	Can change PotentialGlobalWarming	43	change_potentialglobalwarming
154	Can delete PotentialGlobalWarming	43	delete_potentialglobalwarming
155	Can add QuantifiedGas	44	add_quantifiedgas
156	Can change QuantifiedGas	44	change_quantifiedgas
157	Can delete QuantifiedGas	44	delete_quantifiedgas
158	Can add GeiOrganization	45	add_geiorganization
159	Can change GeiOrganization	45	change_geiorganization
160	Can delete GeiOrganization	45	delete_geiorganization
161	Can add RecognitionType	46	add_recognitiontype
162	Can change RecognitionType	46	change_recognitiontype
163	Can delete RecognitionType	46	delete_recognitiontype
164	Can add RequiredLevel	47	add_requiredlevel
165	Can change RequiredLevel	47	change_requiredlevel
166	Can delete RequiredLevel	47	delete_requiredlevel
167	Can add Sector	48	add_sector
168	Can change Sector	48	change_sector
169	Can delete Sector	48	delete_sector
170	Can add SubSector	49	add_subsector
171	Can change SubSector	49	change_subsector
172	Can delete SubSector	49	delete_subsector
173	Can add GeographicLevel	50	add_geographiclevel
174	Can change GeographicLevel	50	change_geographiclevel
175	Can delete GeographicLevel	50	delete_geographiclevel
176	Can add ppcn file	51	add_ppcnfile
177	Can change ppcn file	51	change_ppcnfile
178	Can delete ppcn file	51	delete_ppcnfile
179	Can add PPCN	3	add_ppcn
180	Can change PPCN	3	change_ppcn
181	Can delete PPCN	3	delete_ppcn
182	Can add Workflow Step	52	add_ppcnworkflowstep
183	Can change Workflow Step	52	change_ppcnworkflowstep
184	Can delete Workflow Step	52	delete_ppcnworkflowstep
185	Can add Workflow Step File	53	add_ppcnworkflowstepfile
186	Can change Workflow Step File	53	change_ppcnworkflowstepfile
187	Can delete Workflow Step File	53	delete_ppcnworkflowstepfile
188	Can add ChangeLog	54	add_changelog
189	Can change ChangeLog	54	change_changelog
190	Can delete ChangeLog	54	delete_changelog
191	Can add gei activity type	55	add_geiactivitytype
192	Can change gei activity type	55	change_geiactivitytype
193	Can delete gei activity type	55	delete_geiactivitytype
194	Can add user	4	add_customuser
195	Can change user	4	change_customuser
196	Can delete user	4	delete_customuser
\.


--
-- TOC entry 3946 (class 0 OID 113595)
-- Dependencies: 219
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- TOC entry 3932 (class 0 OID 113478)
-- Dependencies: 205
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	mccr	mccrregistry
2	mitigation_action	mitigation
3	ppcn	ppcn
4	users	customuser
5	admin	logentry
6	auth	permission
7	auth	group
8	contenttypes	contenttype
9	sessions	session
10	report_data	reportfile
11	report_data	reportfileversion
12	report_data	reportfilemetadata
13	mitigation_action	contact
14	mitigation_action	finance
15	mitigation_action	geographicscale
16	mitigation_action	ingeicompliance
17	mitigation_action	institution
18	mitigation_action	location
19	mitigation_action	progressindicator
20	mitigation_action	registrationtype
21	mitigation_action	status
22	mitigation_action	changelog
23	mitigation_action	financesourcetype
24	mitigation_action	maworkflowstep
25	mitigation_action	maworkflowstepfile
26	mitigation_action	financestatus
27	mitigation_action	initiative
28	mitigation_action	initiativefinance
29	mitigation_action	initiativetype
30	workflow	comment
31	workflow	reviewstatus
32	mccr	mccrfile
33	mccr	mccrusertype
34	mccr	mccrregistryovvrelation
35	mccr	ovv
36	mccr	changelog
37	mccr	mccrworkflowstep
38	mccr	mccrworkflowstepfile
39	ppcn	emissionfactor
40	ppcn	inventorymethodology
41	ppcn	organization
42	ppcn	plusaction
43	ppcn	potentialglobalwarming
44	ppcn	quantifiedgas
45	ppcn	geiorganization
46	ppcn	recognitiontype
47	ppcn	requiredlevel
48	ppcn	sector
49	ppcn	subsector
50	ppcn	geographiclevel
51	ppcn	ppcnfile
52	ppcn	ppcnworkflowstep
53	ppcn	ppcnworkflowstepfile
54	ppcn	changelog
55	ppcn	geiactivitytype
\.


--
-- TOC entry 3930 (class 0 OID 113467)
-- Dependencies: 203
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2020-02-14 10:49:57.762194-06
2	contenttypes	0002_remove_content_type_name	2020-02-14 10:49:57.790173-06
3	auth	0001_initial	2020-02-14 10:49:57.834346-06
4	auth	0002_alter_permission_name_max_length	2020-02-14 10:49:57.842018-06
5	auth	0003_alter_user_email_max_length	2020-02-14 10:49:57.848541-06
6	auth	0004_alter_user_username_opts	2020-02-14 10:49:57.85447-06
7	auth	0005_alter_user_last_login_null	2020-02-14 10:49:57.861062-06
8	auth	0006_require_contenttypes_0002	2020-02-14 10:49:57.862944-06
9	auth	0007_alter_validators_add_error_messages	2020-02-14 10:49:57.868634-06
10	auth	0008_alter_user_username_max_length	2020-02-14 10:49:57.888631-06
11	users	0001_initial	2020-02-14 10:49:57.921311-06
12	admin	0001_initial	2020-02-14 10:49:57.943239-06
13	admin	0002_logentry_remove_auto_add	2020-02-14 10:49:57.955338-06
14	general	0001_initial	2020-02-14 10:49:57.957619-06
15	mitigation_action	0001_initial	2020-02-14 10:49:58.084532-06
16	mitigation_action	0002_auto_20180406_0303	2020-02-14 10:49:58.121411-06
17	mitigation_action	0003_auto_20180410_0140	2020-02-14 10:49:58.14716-06
18	mccr	0001_initial	2020-02-14 10:49:58.241068-06
19	mccr	0002_mccrregistry_status	2020-02-14 10:49:58.260369-06
20	mccr	0003_auto_20180504_0350	2020-02-14 10:49:58.335492-06
21	mccr	0004_initial_user_types	2020-02-14 10:49:58.364089-06
22	mccr	0005_auto_20180514_0527	2020-02-14 10:49:58.400104-06
23	mccr	0006_auto_20180726_0106	2020-02-14 10:49:58.435929-06
24	mccr	0007_auto_20180803_1658	2020-02-14 10:49:58.55153-06
25	mccr	0008_auto_20181003_1705	2020-02-14 10:49:58.718024-06
26	mccr	0009_addPermissions	2020-02-14 10:49:58.768386-06
27	mccr	0010_auto_20190801_2139	2020-02-14 10:49:58.814123-06
28	workflow	0001_initial	2020-02-14 10:49:58.824634-06
29	mitigation_action	0004_progressindicator_name	2020-02-14 10:49:58.833139-06
30	mitigation_action	0005_auto_20180418_0529	2020-02-14 10:49:58.902962-06
31	mitigation_action	0006_auto_20180501_2219	2020-02-14 10:49:59.133762-06
32	mitigation_action	0007_auto_20180503_0256	2020-02-14 10:49:59.155761-06
33	mitigation_action	0006_mitigation_question_ucc	2020-02-14 10:49:59.180183-06
34	mitigation_action	0008_merge_20180505_0137	2020-02-14 10:49:59.182391-06
35	mitigation_action	0009_auto_20180509_1347	2020-02-14 10:49:59.220593-06
36	mitigation_action	0010_auto_20180512_2026	2020-02-14 10:49:59.291191-06
37	mitigation_action	0011_auto_20180513_1828	2020-02-14 10:49:59.336136-06
38	mitigation_action	0012_mitigation_question_ovv	2020-02-14 10:49:59.361287-06
39	mitigation_action	0013_auto_20180526_0052	2020-02-14 10:49:59.429779-06
40	mitigation_action	0014_auto_20180604_2002	2020-02-14 10:49:59.547127-06
41	mitigation_action	0015_auto_20180722_2021	2020-02-14 10:49:59.609438-06
42	mitigation_action	0016_registrationtype_type_key	2020-02-14 10:49:59.715432-06
43	mitigation_action	0015_harmonizationingei	2020-02-14 10:49:59.750786-06
44	mitigation_action	0016_merge_20180726_1803	2020-02-14 10:49:59.752922-06
45	mitigation_action	0017_auto_20180726_1804	2020-02-14 10:49:59.941995-06
46	mitigation_action	0018_auto_20180726_1805	2020-02-14 10:49:59.966373-06
47	mitigation_action	0019_auto_20180803_1658	2020-02-14 10:49:59.991877-06
48	mitigation_action	0020_auto_20180817_2248	2020-02-14 10:50:00.074454-06
49	mitigation_action	0021_auto_20180819_0423	2020-02-14 10:50:00.303568-06
50	mitigation_action	0022_auto_20180919_1556	2020-02-14 10:50:00.496442-06
51	mitigation_action	0023_auto_20181029_1753	2020-02-14 10:50:01.706036-06
52	mitigation_action	0024_auto_20181029_2112	2020-02-14 10:50:01.720774-06
53	mitigation_action	0023_auto_20181030_0214	2020-02-14 10:50:01.773431-06
54	mitigation_action	0025_merge_20181030_1721	2020-02-14 10:50:01.78376-06
55	mitigation_action	0026_auto_20181204_1636	2020-02-14 10:50:01.926885-06
56	mitigation_action	0027_addPermissions	2020-02-14 10:50:01.97089-06
57	mitigation_action	0028_auto_20190318_2142	2020-02-14 10:50:01.998656-06
58	workflow	0002_auto_20180503_0303	2020-02-14 10:50:02.038059-06
59	workflow	0003_auto_20180513_1755	2020-02-14 10:50:02.053481-06
60	ppcn	0001_initial	2020-02-14 10:50:02.168966-06
61	ppcn	0002_auto_20180730_2101	2020-02-14 10:50:02.43116-06
62	ppcn	0003_auto_20180730_0140	2020-02-14 10:50:02.519949-06
63	ppcn	0004_auto_20180801_2004	2020-02-14 10:50:02.710724-06
64	ppcn	0005_auto_20180816_1713	2020-02-14 10:50:02.765103-06
65	ppcn	0006_auto_20180820_2149	2020-02-14 10:50:02.859866-06
66	ppcn	0007_auto_20180821_1607	2020-02-14 10:50:02.904514-06
67	ppcn	0008_auto_20180822_1938	2020-02-14 10:50:02.979017-06
68	ppcn	0009_auto_20180827_1549	2020-02-14 10:50:03.064089-06
69	ppcn	0010_auto_20180831_1950	2020-02-14 10:50:03.097544-06
70	ppcn	0011_ppcnworkflowstep_ppcnworkflowstepfile	2020-02-14 10:50:03.269995-06
71	ppcn	0012_auto_20180911_1654	2020-02-14 10:50:03.464983-06
72	ppcn	0013_auto_20181116_1950	2020-02-14 10:50:03.502447-06
73	ppcn	0014_auto_20181125_1702	2020-02-14 10:50:03.623557-06
74	ppcn	0015_auto_20181210_0448	2020-02-14 10:50:04.379971-06
75	ppcn	0016_auto_20190304_1628	2020-02-14 10:50:04.429132-06
76	ppcn	0017_addPermissions	2020-02-14 10:50:04.550838-06
77	ppcn	0018_auto_20190318_2142	2020-02-14 10:50:04.581682-06
78	ppcn	0019_auto_20190718_2141	2020-02-14 10:50:04.643532-06
79	report_data	0001_initial	2020-02-14 10:50:04.652631-06
80	report_data	0002_auto_20180307_0345	2020-02-14 10:50:04.663658-06
81	report_data	0003_auto_20180307_0406	2020-02-14 10:50:04.669312-06
82	report_data	0004_auto_20180314_2352	2020-02-14 10:50:04.688923-06
83	report_data	0005_auto_20180315_0014	2020-02-14 10:50:04.721012-06
84	report_data	0006_reportfileversion_file	2020-02-14 10:50:04.730943-06
85	report_data	0007_auto_20180320_0346	2020-02-14 10:50:04.745341-06
86	report_data	0008_auto_20180320_0427	2020-02-14 10:50:04.765296-06
87	report_data	0004_reportfile_user	2020-02-14 10:50:04.826038-06
88	report_data	0009_merge_20180322_0012	2020-02-14 10:50:04.828042-06
89	report_data	0010_reportfileversion_user	2020-02-14 10:50:04.882221-06
90	report_data	0011_auto_20180322_0207	2020-02-14 10:50:04.929772-06
91	report_data	0012_auto_20180517_0247	2020-02-14 10:50:04.95935-06
92	report_data	0013_reportfilemetadata	2020-02-14 10:50:05.011484-06
93	sessions	0001_initial	2020-02-14 10:50:05.02339-06
94	users	0002_auto_20190322_2126	2020-02-14 10:50:05.113697-06
95	users	0003_addPermissions	2020-02-14 10:50:05.471202-06
\.


--
-- TOC entry 4050 (class 0 OID 114817)
-- Dependencies: 323
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
x997a9z87jm82fn92lf4l23xiyrkki59	YTUyYThkZmQyODg1OTg3ODRmMTcwMjcxODM0YTgwMzdhNWZlOWRlZjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJkZDE5OTQwOWVjMGMwYWE0YTI4MWI0ZmI1NjhiMTRjZDkzZjViMzA1In0=	2020-02-28 11:00:32.426421-06
ebglyxo0iwrzc9l1j584awlugzf8qz9x	YTUyYThkZmQyODg1OTg3ODRmMTcwMjcxODM0YTgwMzdhNWZlOWRlZjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJkZDE5OTQwOWVjMGMwYWE0YTI4MWI0ZmI1NjhiMTRjZDkzZjViMzA1In0=	2020-02-28 11:00:49.903682-06
\.


--
-- TOC entry 3975 (class 0 OID 113855)
-- Dependencies: 248
-- Data for Name: mccr_changelog; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mccr_changelog (id, date, previous_status, current_status, mccr_id, user_id) FROM stdin;
\.


--
-- TOC entry 3966 (class 0 OID 113761)
-- Dependencies: 239
-- Data for Name: mccr_mccrfile; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mccr_mccrfile (id, file, mccr_id, user_id, created, updated) FROM stdin;
\.


--
-- TOC entry 3967 (class 0 OID 113766)
-- Dependencies: 240
-- Data for Name: mccr_mccrregistry; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mccr_mccrregistry (id, user_type_id, mitigation_id, user_id, status, created, updated, fsm_state) FROM stdin;
\.


--
-- TOC entry 3971 (class 0 OID 113825)
-- Dependencies: 244
-- Data for Name: mccr_mccrregistryovvrelation; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mccr_mccrregistryovvrelation (id, status, created, updated, mccr_id, ovv_id) FROM stdin;
\.


--
-- TOC entry 3969 (class 0 OID 113798)
-- Dependencies: 242
-- Data for Name: mccr_mccrusertype; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mccr_mccrusertype (id, name) FROM stdin;
1	Registrator
2	Reviewer
\.


--
-- TOC entry 3977 (class 0 OID 113863)
-- Dependencies: 250
-- Data for Name: mccr_mccrworkflowstep; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mccr_mccrworkflowstep (id, name, entry_name, status, created, updated, mccr_id, user_id) FROM stdin;
\.


--
-- TOC entry 3979 (class 0 OID 113871)
-- Dependencies: 252
-- Data for Name: mccr_mccrworkflowstepfile; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mccr_mccrworkflowstepfile (id, created, updated, file, user_id, workflow_step_id) FROM stdin;
\.


--
-- TOC entry 3973 (class 0 OID 113833)
-- Dependencies: 246
-- Data for Name: mccr_ovv; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mccr_ovv (id, name, email, phone, created, updated) FROM stdin;
1	Test backend OVV	sinamec@grupoincocr.com	(506) 9309-2345	2020-02-14 10:49:58.544367-06	2020-02-14 10:49:58.544387-06
\.


--
-- TOC entry 3987 (class 0 OID 113960)
-- Dependencies: 260
-- Data for Name: mitigation_action_changelog; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mitigation_action_changelog (id, date, current_status, mitigation_action_id, previous_status, user_id) FROM stdin;
\.


--
-- TOC entry 3948 (class 0 OID 113620)
-- Dependencies: 221
-- Data for Name: mitigation_action_contact; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mitigation_action_contact (id, full_name, job_title, email, phone) FROM stdin;
1	test	test	test@test.com	88888888
\.


--
-- TOC entry 3950 (class 0 OID 113631)
-- Dependencies: 223
-- Data for Name: mitigation_action_finance; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mitigation_action_finance (id, source, status_id) FROM stdin;
\.


--
-- TOC entry 3991 (class 0 OID 114023)
-- Dependencies: 264
-- Data for Name: mitigation_action_financesourcetype; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mitigation_action_financesourcetype (id, name_en, name_es) FROM stdin;
3	Public Budget	Presupuesto público 
4	Private Finance	Financiamiento privado
5	Cooperation Project	Proyecto de cooperación
6	Loan	Préstamo
\.


--
-- TOC entry 3997 (class 0 OID 114189)
-- Dependencies: 270
-- Data for Name: mitigation_action_financestatus; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mitigation_action_financestatus (id, name_es, name_en) FROM stdin;
1	Por obtener	To obtain
2	Asegurado	Insured
\.


--
-- TOC entry 3952 (class 0 OID 113639)
-- Dependencies: 225
-- Data for Name: mitigation_action_geographicscale; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mitigation_action_geographicscale (id, name_en, name_es) FROM stdin;
4	National	Nacional
5	Regional	Regional
6	Local	Local
\.


--
-- TOC entry 3954 (class 0 OID 113647)
-- Dependencies: 227
-- Data for Name: mitigation_action_ingeicompliance; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mitigation_action_ingeicompliance (id, name_en, name_es) FROM stdin;
4	Agriculture, forestry and other land uses	Agricultura, silvicultura y otros usos de la tierra (AFOLU)
5	Industrial processes and use of products	Procesos industriales y uso de productos
6	Residue	Residuos
\.


--
-- TOC entry 3999 (class 0 OID 114197)
-- Dependencies: 272
-- Data for Name: mitigation_action_initiative; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mitigation_action_initiative (id, name, objective, description, goal, entity_responsible, budget, contact_id, finance_id, initiative_type_id, status_id) FROM stdin;
\.


--
-- TOC entry 4001 (class 0 OID 114208)
-- Dependencies: 274
-- Data for Name: mitigation_action_initiativefinance; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mitigation_action_initiativefinance (id, finance_source_type_id, status_id, source) FROM stdin;
\.


--
-- TOC entry 4003 (class 0 OID 114216)
-- Dependencies: 276
-- Data for Name: mitigation_action_initiativetype; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mitigation_action_initiativetype (id, initiative_type_es, initiative_type_en) FROM stdin;
1	Proyecto	Proyect
2	Política	Law
3	Meta	Goal
\.


--
-- TOC entry 3956 (class 0 OID 113655)
-- Dependencies: 229
-- Data for Name: mitigation_action_institution; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mitigation_action_institution (id, name) FROM stdin;
1	MINAE
2	SINAMECC
\.


--
-- TOC entry 3958 (class 0 OID 113663)
-- Dependencies: 231
-- Data for Name: mitigation_action_location; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mitigation_action_location (id, geographical_site, is_gis_annexed) FROM stdin;
\.


--
-- TOC entry 3993 (class 0 OID 114129)
-- Dependencies: 266
-- Data for Name: mitigation_action_maworkflowstep; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mitigation_action_maworkflowstep (id, name, entry_name, status, created, updated, mitigation_action_id, user_id) FROM stdin;
\.


--
-- TOC entry 3995 (class 0 OID 114137)
-- Dependencies: 268
-- Data for Name: mitigation_action_maworkflowstepfile; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mitigation_action_maworkflowstepfile (id, file, created, updated, user_id, workflow_step_id) FROM stdin;
\.


--
-- TOC entry 3959 (class 0 OID 113669)
-- Dependencies: 232
-- Data for Name: mitigation_action_mitigation; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mitigation_action_mitigation (id, strategy_name, name, purpose, start_date, end_date, gas_inventory, emissions_source, carbon_sinks, impact_plan, impact, calculation_methodology, is_international, international_participation, created, updated, contact_id, finance_id, geographic_scale_id, institution_id, location_id, progress_indicator_id, registration_type_id, status_id, user_id, review_count, fsm_state, initiative_id) FROM stdin;
\.


--
-- TOC entry 3989 (class 0 OID 113968)
-- Dependencies: 262
-- Data for Name: mitigation_action_mitigation_comments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mitigation_action_mitigation_comments (id, mitigation_id, comment_id) FROM stdin;
\.


--
-- TOC entry 3985 (class 0 OID 113938)
-- Dependencies: 258
-- Data for Name: mitigation_action_mitigation_ingei_compliances; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mitigation_action_mitigation_ingei_compliances (id, mitigation_id, ingeicompliance_id) FROM stdin;
\.


--
-- TOC entry 3961 (class 0 OID 113679)
-- Dependencies: 234
-- Data for Name: mitigation_action_progressindicator; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mitigation_action_progressindicator (id, type, unit, start_date, name) FROM stdin;
\.


--
-- TOC entry 3963 (class 0 OID 113687)
-- Dependencies: 236
-- Data for Name: mitigation_action_registrationtype; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mitigation_action_registrationtype (id, type_en, type_es, type_key) FROM stdin;
5	Registration for the first time	Inscripción por primera vez	new
6	Update of mitigation action information	Actualización de información de acción de mitigación	update
\.


--
-- TOC entry 3965 (class 0 OID 113695)
-- Dependencies: 238
-- Data for Name: mitigation_action_status; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mitigation_action_status (id, status_en, status_es) FROM stdin;
4	Planning	Planeación
5	Implementation	Implementación
6	Completed	Finalizada
\.


--
-- TOC entry 4037 (class 0 OID 114597)
-- Dependencies: 310
-- Data for Name: ppcn_changelog; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ppcn_changelog (id, date, previous_status, current_status, ppcn_id, user_id) FROM stdin;
1	2020-02-14 10:53:52.823329-06	PPCN_new	PPCN_submitted	1	3
2	2020-02-14 10:57:05.077688-06	PPCN_submitted	PPCN_evaluation_by_DCC	1	3
\.


--
-- TOC entry 4005 (class 0 OID 114318)
-- Dependencies: 278
-- Data for Name: ppcn_emissionfactor; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ppcn_emissionfactor (id, name) FROM stdin;
\.


--
-- TOC entry 4041 (class 0 OID 114658)
-- Dependencies: 314
-- Data for Name: ppcn_geiactivitytype; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ppcn_geiactivitytype (id, activity_type, sector_id, sub_sector_id) FROM stdin;
1	test	2	9
\.


--
-- TOC entry 4019 (class 0 OID 114403)
-- Dependencies: 292
-- Data for Name: ppcn_geiorganization; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ppcn_geiorganization (id, ovv_id, emission_ovv_date, report_year, base_year) FROM stdin;
1	1	2020-07-16	1995	1992
\.


--
-- TOC entry 4043 (class 0 OID 114679)
-- Dependencies: 316
-- Data for Name: ppcn_geiorganization_gei_activity_types; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ppcn_geiorganization_gei_activity_types (id, geiorganization_id, geiactivitytype_id) FROM stdin;
1	1	1
\.


--
-- TOC entry 4009 (class 0 OID 114334)
-- Dependencies: 282
-- Data for Name: ppcn_geographiclevel; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ppcn_geographiclevel (id, level_es, level_en) FROM stdin;
1	Cantonal	Cantonal
2	Organizacional	Organizational
\.


--
-- TOC entry 4007 (class 0 OID 114326)
-- Dependencies: 280
-- Data for Name: ppcn_inventorymethodology; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ppcn_inventorymethodology (id, name) FROM stdin;
\.


--
-- TOC entry 4011 (class 0 OID 114342)
-- Dependencies: 284
-- Data for Name: ppcn_organization; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ppcn_organization (id, name, representative_name, postal_code, fax, address, ciiu, contact_id, phone_organization) FROM stdin;
1	test	test			test	test	1	888888888
\.


--
-- TOC entry 4013 (class 0 OID 114353)
-- Dependencies: 286
-- Data for Name: ppcn_plusaction; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ppcn_plusaction (id, name) FROM stdin;
\.


--
-- TOC entry 4015 (class 0 OID 114361)
-- Dependencies: 288
-- Data for Name: ppcn_potentialglobalwarming; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ppcn_potentialglobalwarming (id, name) FROM stdin;
\.


--
-- TOC entry 4031 (class 0 OID 114469)
-- Dependencies: 304
-- Data for Name: ppcn_ppcn; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ppcn_ppcn (id, organization_id, created, updated, user_id, fsm_state, review_count, gei_organization_id, geographic_level_id, recognition_type_id, required_level_id) FROM stdin;
1	1	2020-02-14 10:53:52.815642-06	2020-02-14 10:57:05.068596-06	3	PPCN_evaluation_by_DCC	1	1	2	2	2
\.


--
-- TOC entry 4039 (class 0 OID 114605)
-- Dependencies: 312
-- Data for Name: ppcn_ppcn_comments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ppcn_ppcn_comments (id, ppcn_id, comment_id) FROM stdin;
1	1	1
\.


--
-- TOC entry 4029 (class 0 OID 114461)
-- Dependencies: 302
-- Data for Name: ppcn_ppcnfile; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ppcn_ppcnfile (id, file, created, updated, ppcn_form_id, user_id) FROM stdin;
1	ppcn/files/20200214/165629/PPCN_CANTONAL.xlsx	2020-02-14 10:56:35.682078-06	2020-02-14 10:56:35.68213-06	1	3
\.


--
-- TOC entry 4033 (class 0 OID 114557)
-- Dependencies: 306
-- Data for Name: ppcn_ppcnworkflowstep; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ppcn_ppcnworkflowstep (id, name, entry_name, status, created, updated, ppcn_id, user_id) FROM stdin;
\.


--
-- TOC entry 4035 (class 0 OID 114565)
-- Dependencies: 308
-- Data for Name: ppcn_ppcnworkflowstepfile; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ppcn_ppcnworkflowstepfile (id, file, created, updated, user_id, workflow_step_id) FROM stdin;
\.


--
-- TOC entry 4017 (class 0 OID 114369)
-- Dependencies: 290
-- Data for Name: ppcn_quantifiedgas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ppcn_quantifiedgas (id, name) FROM stdin;
\.


--
-- TOC entry 4021 (class 0 OID 114411)
-- Dependencies: 294
-- Data for Name: ppcn_recognitiontype; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ppcn_recognitiontype (id, recognition_type_es, recognition_type_en) FROM stdin;
1	Carbono Inventario	Carbon Inventary
2	Carbono Reducción	Carbon Reduction
3	Carbono Reducción +	Carbon Reduction +
4	Carbono Neutral	Carbon Neutral
5	Carbono Neutral +	Carbon Neutral +
\.


--
-- TOC entry 4023 (class 0 OID 114419)
-- Dependencies: 296
-- Data for Name: ppcn_requiredlevel; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ppcn_requiredlevel (id, level_type_es, level_type_en) FROM stdin;
1	Solicitud inicial de incorporación al PPCN	Initial Request to incorporate with PPCN
2	Mantenimiento en el PPCN	Maintenance to PPCN
3	Renovación en el PPCN	Renovation in the PPCN
\.


--
-- TOC entry 4025 (class 0 OID 114427)
-- Dependencies: 298
-- Data for Name: ppcn_sector; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ppcn_sector (id, name_es, name_en, "geographicLevel_id") FROM stdin;
1	Energía	Energy	2
2	Procesos Industriales	Industrial Processes	2
3	Agricultura	Agriculture	2
4	Residuos	Waste	2
5	Uso de Suelo, Cambio de Suelo y Silvicultura (USCUSyS)	Land Use, Land Change and Forestry (USCUSyS)	2
6	Energía Estacionaria	Stationary Energy	1
7	Transporte	Transport	1
8	Residuos	Waste	1
9	Agricultura, Silvicultura y Otros Usos de la Tierra	Agriculture, Forestry and Other Uses of the Earth	1
\.


--
-- TOC entry 4027 (class 0 OID 114435)
-- Dependencies: 300
-- Data for Name: ppcn_subsector; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ppcn_subsector (id, name_es, name_en, sector_id) FROM stdin;
1	Consumo de combustibles fósiles	Consumption of fossil fuels	1
2	Emisiones fugitivas	Fugitive emissions	1
3	Emisiones GEI por quema de biomasa	GEI emissions from burning biomass	1
4	Distribución de energía	Energy Distribution	1
5	Productos Minerales	Minerals products	2
6	Industria química	Chemistry Industry	2
7	Producción de metales	Metal production	2
8	Otros procesos industriales	Other industrial processes	2
9	Producción de halocarbonos y hexafloruro de azufre	Production of halocarbons and sulfur hexafluoride	2
10	Consumo de halocarbonos y haxafloruro de azufre	Consumption of halocarbons and sulfur hexafluoride	2
11	Fermentación entérica	Enteric fermentation	3
12	Manejo de estiércol	Manure management	3
13	Cultivo del arroz	Rice cultivation	3
14	Suelos agrícolas	Agricultural soils	3
15	Quemas programadas de suelos	Scheduled burns of floors	3
16	Quema in situ de residuos agrícolas	On-site burning of agricultural wastee	3
17	Disposición de residuos sólidos en suelo	Disposal of solid waste in soil	4
18	Manejo y tratamiento de aguas residuales	Wastewater treatment and treatment	4
19	Incineración de residuos	Waste incineration	4
20	Tierras	Lands	5
21	Edificios residenciales	Residential buildings	6
22	Edificios e instalaciones comerciales e institucionales	Commercial and institutional buildings and facilities	6
23	Construcción e industrias manufactureras	Construction and manufacturing industries	6
24	Industrias energéticas	Energy industries	6
25	Actividades agrícolas, de silvicultura y de pesca	Agricultural, forestry and fishing activities	6
26	Fuentes no especificadas	Unspecified sources	6
27	Emisiones fugitivas provenientes de la minería, el procesamiento, el almacenamiento y el transporte de carbón	Fugitive emissions from coal mining, processing, storage and transportation	6
28	Emisiones fugitivas provenientes de los sistemas de petróleo y gas natural	Fugitive emissions from oil and natural gas systems	6
29	Por carretera	By highway	7
30	Ferroviario	Ferroviario	7
31	Navegación marítima, fluvial y lacustre	Maritime, fluvial and lacustrine navigation	7
32	Aviación	Aviation	7
33	Fuera de carretera	Off road	7
34	Disposición de residuos sólidos generados en la ciudad	Disposal of solid waste generated in the city	8
35	Tratamiento biológico de residuos generados en la ciudad	Biological treatment of waste generated in the city	8
36	Incineración y quema a cielo abierto de residuos generados en la ciudad	Incineration and open burning of waste generated in the city	8
37	Aguas residuales generadas en la ciudad	Wastewater generated in the city	8
38	Ganadería	Cattle raising	9
39	Uso de la Tierra	Use of the Earth	9
40	Fuentes agregadas y emisiones procedentes de fuentes del suelo distintas  al CO2	Aggregate sources and emissions from sources other than CO2	9
\.


--
-- TOC entry 4045 (class 0 OID 114736)
-- Dependencies: 318
-- Data for Name: report_data_reportfile; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.report_data_reportfile (id, name, created, updated, user_id) FROM stdin;
\.


--
-- TOC entry 4049 (class 0 OID 114805)
-- Dependencies: 322
-- Data for Name: report_data_reportfilemetadata; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.report_data_reportfilemetadata (id, name, value, report_file_id) FROM stdin;
\.


--
-- TOC entry 4047 (class 0 OID 114748)
-- Dependencies: 320
-- Data for Name: report_data_reportfileversion; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.report_data_reportfileversion (id, active, version, file, report_file_id, user_id) FROM stdin;
\.


--
-- TOC entry 3940 (class 0 OID 113537)
-- Dependencies: 213
-- Data for Name: users_customuser; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users_customuser (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, is_administrador_dcc, is_provider, phone) FROM stdin;
1	pbkdf2_sha256$36000$vgbYgDsZfwuY$nL9miuqECSaedNFycVmMEB/PcYdEFFnODgsiIsTsbgs=	2020-02-14 10:51:33.862505-06	t	admin	Administrador	Sinamecc	sinamec@grupoincocr.com	t	t	2020-02-14 10:50:05.172403-06	t	t	\N
3	pbkdf2_sha256$36000$QGE0ntKGKUJn$hzNakZrefQU2jIGYLTcXQul3kBJ/TUtEDXNtpTtpU7s=	2020-02-14 10:51:48.796442-06	f	information_provider	Provider	Sinamecc	carlos@grupoincocr.com	t	t	2020-02-14 10:50:05.181219-06	f	t	\N
2	pbkdf2_sha256$36000$dy2QXgMCjudo$Id1UrlkfCd/G+UpFMZgbtfNPKdewytZK0Nu8lKwFrOA=	2020-02-14 11:00:49.901965-06	f	general_dcc	DCC	Sinamecc	izcar@grupoincocr.com	t	t	2020-02-14 10:50:05.176628-06	t	f	\N
\.


--
-- TOC entry 3942 (class 0 OID 113550)
-- Dependencies: 215
-- Data for Name: users_customuser_groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users_customuser_groups (id, customuser_id, group_id) FROM stdin;
1	1	1
2	2	2
3	3	3
\.


--
-- TOC entry 3944 (class 0 OID 113558)
-- Dependencies: 217
-- Data for Name: users_customuser_user_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users_customuser_user_permissions (id, customuser_id, permission_id) FROM stdin;
1	1	13
2	1	14
3	1	15
4	1	16
5	1	17
6	1	18
7	1	19
8	1	20
9	1	21
10	1	22
11	1	23
12	1	24
13	1	25
14	1	26
15	1	27
16	1	28
17	1	29
18	1	30
19	1	31
20	2	13
21	2	14
22	2	15
23	2	16
24	2	17
25	2	18
26	2	19
27	2	20
28	2	21
29	2	23
30	2	24
31	2	25
32	2	27
33	2	28
34	2	30
35	3	13
36	3	14
37	3	15
38	3	16
39	3	17
40	3	18
41	3	19
42	3	20
43	3	21
44	3	24
45	3	28
46	3	30
\.


--
-- TOC entry 3981 (class 0 OID 113921)
-- Dependencies: 254
-- Data for Name: workflow_comment; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.workflow_comment (id, comment) FROM stdin;
1	undefined
\.


--
-- TOC entry 3983 (class 0 OID 113929)
-- Dependencies: 256
-- Data for Name: workflow_reviewstatus; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.workflow_reviewstatus (id, status) FROM stdin;
1	submitted
2	in-review
3	on-change
4	approved
5	rejected
\.


--
-- TOC entry 4115 (class 0 OID 0)
-- Dependencies: 208
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 3, true);


--
-- TOC entry 4116 (class 0 OID 0)
-- Dependencies: 210
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- TOC entry 4117 (class 0 OID 0)
-- Dependencies: 206
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 196, true);


--
-- TOC entry 4118 (class 0 OID 0)
-- Dependencies: 218
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);


--
-- TOC entry 4119 (class 0 OID 0)
-- Dependencies: 204
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 55, true);


--
-- TOC entry 4120 (class 0 OID 0)
-- Dependencies: 202
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 95, true);


--
-- TOC entry 4121 (class 0 OID 0)
-- Dependencies: 247
-- Name: mccr_changelog_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mccr_changelog_id_seq', 1, false);


--
-- TOC entry 4122 (class 0 OID 0)
-- Dependencies: 243
-- Name: mccr_mccrregistryovvrelation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mccr_mccrregistryovvrelation_id_seq', 1, false);


--
-- TOC entry 4123 (class 0 OID 0)
-- Dependencies: 241
-- Name: mccr_mccrusertype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mccr_mccrusertype_id_seq', 2, true);


--
-- TOC entry 4124 (class 0 OID 0)
-- Dependencies: 249
-- Name: mccr_mccrworkflowstep_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mccr_mccrworkflowstep_id_seq', 1, false);


--
-- TOC entry 4125 (class 0 OID 0)
-- Dependencies: 251
-- Name: mccr_mccrworkflowstepfile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mccr_mccrworkflowstepfile_id_seq', 1, false);


--
-- TOC entry 4126 (class 0 OID 0)
-- Dependencies: 245
-- Name: mccr_ovv_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mccr_ovv_id_seq', 1, true);


--
-- TOC entry 4127 (class 0 OID 0)
-- Dependencies: 259
-- Name: mitigation_action_changelog_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mitigation_action_changelog_id_seq', 1, false);


--
-- TOC entry 4128 (class 0 OID 0)
-- Dependencies: 220
-- Name: mitigation_action_contact_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mitigation_action_contact_id_seq', 1, true);


--
-- TOC entry 4129 (class 0 OID 0)
-- Dependencies: 222
-- Name: mitigation_action_finance_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mitigation_action_finance_id_seq', 2, true);


--
-- TOC entry 4130 (class 0 OID 0)
-- Dependencies: 263
-- Name: mitigation_action_financesourcetype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mitigation_action_financesourcetype_id_seq', 6, true);


--
-- TOC entry 4131 (class 0 OID 0)
-- Dependencies: 269
-- Name: mitigation_action_financestatus_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mitigation_action_financestatus_id_seq', 2, true);


--
-- TOC entry 4132 (class 0 OID 0)
-- Dependencies: 224
-- Name: mitigation_action_geographicscale_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mitigation_action_geographicscale_id_seq', 6, true);


--
-- TOC entry 4133 (class 0 OID 0)
-- Dependencies: 226
-- Name: mitigation_action_ingeicompliance_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mitigation_action_ingeicompliance_id_seq', 6, true);


--
-- TOC entry 4134 (class 0 OID 0)
-- Dependencies: 271
-- Name: mitigation_action_initiative_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mitigation_action_initiative_id_seq', 1, false);


--
-- TOC entry 4135 (class 0 OID 0)
-- Dependencies: 273
-- Name: mitigation_action_initiativefinance_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mitigation_action_initiativefinance_id_seq', 1, false);


--
-- TOC entry 4136 (class 0 OID 0)
-- Dependencies: 275
-- Name: mitigation_action_initiativetype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mitigation_action_initiativetype_id_seq', 3, true);


--
-- TOC entry 4137 (class 0 OID 0)
-- Dependencies: 228
-- Name: mitigation_action_institution_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mitigation_action_institution_id_seq', 2, true);


--
-- TOC entry 4138 (class 0 OID 0)
-- Dependencies: 230
-- Name: mitigation_action_location_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mitigation_action_location_id_seq', 1, false);


--
-- TOC entry 4139 (class 0 OID 0)
-- Dependencies: 265
-- Name: mitigation_action_maworkflowstep_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mitigation_action_maworkflowstep_id_seq', 1, false);


--
-- TOC entry 4140 (class 0 OID 0)
-- Dependencies: 267
-- Name: mitigation_action_maworkflowstepfile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mitigation_action_maworkflowstepfile_id_seq', 1, false);


--
-- TOC entry 4141 (class 0 OID 0)
-- Dependencies: 261
-- Name: mitigation_action_mitigation_comments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mitigation_action_mitigation_comments_id_seq', 1, false);


--
-- TOC entry 4142 (class 0 OID 0)
-- Dependencies: 257
-- Name: mitigation_action_mitigation_ingei_compliances_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mitigation_action_mitigation_ingei_compliances_id_seq', 1, false);


--
-- TOC entry 4143 (class 0 OID 0)
-- Dependencies: 233
-- Name: mitigation_action_progressindicator_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mitigation_action_progressindicator_id_seq', 1, false);


--
-- TOC entry 4144 (class 0 OID 0)
-- Dependencies: 235
-- Name: mitigation_action_registrationtype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mitigation_action_registrationtype_id_seq', 6, true);


--
-- TOC entry 4145 (class 0 OID 0)
-- Dependencies: 237
-- Name: mitigation_action_status_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mitigation_action_status_id_seq', 6, true);


--
-- TOC entry 4146 (class 0 OID 0)
-- Dependencies: 309
-- Name: ppcn_changelog_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ppcn_changelog_id_seq', 2, true);


--
-- TOC entry 4147 (class 0 OID 0)
-- Dependencies: 277
-- Name: ppcn_emissionfactor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ppcn_emissionfactor_id_seq', 1, false);


--
-- TOC entry 4148 (class 0 OID 0)
-- Dependencies: 313
-- Name: ppcn_geiactivitytype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ppcn_geiactivitytype_id_seq', 1, true);


--
-- TOC entry 4149 (class 0 OID 0)
-- Dependencies: 315
-- Name: ppcn_geiorganization_gei_activity_types_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ppcn_geiorganization_gei_activity_types_id_seq', 1, true);


--
-- TOC entry 4150 (class 0 OID 0)
-- Dependencies: 291
-- Name: ppcn_geiorganization_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ppcn_geiorganization_id_seq', 1, true);


--
-- TOC entry 4151 (class 0 OID 0)
-- Dependencies: 279
-- Name: ppcn_inventorymethodology_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ppcn_inventorymethodology_id_seq', 1, false);


--
-- TOC entry 4152 (class 0 OID 0)
-- Dependencies: 281
-- Name: ppcn_level_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ppcn_level_id_seq', 2, true);


--
-- TOC entry 4153 (class 0 OID 0)
-- Dependencies: 283
-- Name: ppcn_organization_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ppcn_organization_id_seq', 1, true);


--
-- TOC entry 4154 (class 0 OID 0)
-- Dependencies: 285
-- Name: ppcn_plusaction_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ppcn_plusaction_id_seq', 1, false);


--
-- TOC entry 4155 (class 0 OID 0)
-- Dependencies: 287
-- Name: ppcn_potentialglobalwarming_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ppcn_potentialglobalwarming_id_seq', 1, false);


--
-- TOC entry 4156 (class 0 OID 0)
-- Dependencies: 311
-- Name: ppcn_ppcn_comments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ppcn_ppcn_comments_id_seq', 1, true);


--
-- TOC entry 4157 (class 0 OID 0)
-- Dependencies: 303
-- Name: ppcn_ppcn_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ppcn_ppcn_id_seq', 1, true);


--
-- TOC entry 4158 (class 0 OID 0)
-- Dependencies: 301
-- Name: ppcn_ppcnfile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ppcn_ppcnfile_id_seq', 1, true);


--
-- TOC entry 4159 (class 0 OID 0)
-- Dependencies: 305
-- Name: ppcn_ppcnworkflowstep_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ppcn_ppcnworkflowstep_id_seq', 1, false);


--
-- TOC entry 4160 (class 0 OID 0)
-- Dependencies: 307
-- Name: ppcn_ppcnworkflowstepfile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ppcn_ppcnworkflowstepfile_id_seq', 1, false);


--
-- TOC entry 4161 (class 0 OID 0)
-- Dependencies: 289
-- Name: ppcn_quantifiedgas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ppcn_quantifiedgas_id_seq', 1, false);


--
-- TOC entry 4162 (class 0 OID 0)
-- Dependencies: 293
-- Name: ppcn_recognitiontype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ppcn_recognitiontype_id_seq', 5, true);


--
-- TOC entry 4163 (class 0 OID 0)
-- Dependencies: 295
-- Name: ppcn_requiredlevel_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ppcn_requiredlevel_id_seq', 3, true);


--
-- TOC entry 4164 (class 0 OID 0)
-- Dependencies: 297
-- Name: ppcn_sector_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ppcn_sector_id_seq', 9, true);


--
-- TOC entry 4165 (class 0 OID 0)
-- Dependencies: 299
-- Name: ppcn_subsector_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ppcn_subsector_id_seq', 40, true);


--
-- TOC entry 4166 (class 0 OID 0)
-- Dependencies: 317
-- Name: report_data_reportfile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.report_data_reportfile_id_seq', 1, false);


--
-- TOC entry 4167 (class 0 OID 0)
-- Dependencies: 321
-- Name: report_data_reportfilemetadata_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.report_data_reportfilemetadata_id_seq', 1, false);


--
-- TOC entry 4168 (class 0 OID 0)
-- Dependencies: 319
-- Name: report_data_reportfileversion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.report_data_reportfileversion_id_seq', 1, false);


--
-- TOC entry 4169 (class 0 OID 0)
-- Dependencies: 214
-- Name: users_customuser_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_customuser_groups_id_seq', 3, true);


--
-- TOC entry 4170 (class 0 OID 0)
-- Dependencies: 212
-- Name: users_customuser_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_customuser_id_seq', 3, true);


--
-- TOC entry 4171 (class 0 OID 0)
-- Dependencies: 216
-- Name: users_customuser_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_customuser_user_permissions_id_seq', 46, true);


--
-- TOC entry 4172 (class 0 OID 0)
-- Dependencies: 253
-- Name: workflow_comment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.workflow_comment_id_seq', 1, true);


--
-- TOC entry 4173 (class 0 OID 0)
-- Dependencies: 255
-- Name: workflow_reviewstatus_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.workflow_reviewstatus_id_seq', 5, true);


--
-- TOC entry 3507 (class 2606 OID 113503)
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- TOC entry 3512 (class 2606 OID 113532)
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- TOC entry 3515 (class 2606 OID 113511)
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- TOC entry 3509 (class 2606 OID 113501)
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- TOC entry 3502 (class 2606 OID 113518)
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- TOC entry 3504 (class 2606 OID 113493)
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- TOC entry 3535 (class 2606 OID 113604)
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- TOC entry 3497 (class 2606 OID 113485)
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- TOC entry 3499 (class 2606 OID 113483)
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- TOC entry 3495 (class 2606 OID 113475)
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- TOC entry 3724 (class 2606 OID 114824)
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- TOC entry 3586 (class 2606 OID 113860)
-- Name: mccr_changelog mccr_changelog_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_changelog
    ADD CONSTRAINT mccr_changelog_pkey PRIMARY KEY (id);


--
-- TOC entry 3570 (class 2606 OID 113765)
-- Name: mccr_mccrfile mccr_mccrfile_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_mccrfile
    ADD CONSTRAINT mccr_mccrfile_pkey PRIMARY KEY (id);


--
-- TOC entry 3574 (class 2606 OID 113770)
-- Name: mccr_mccrregistry mccr_mccrregistry_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_mccrregistry
    ADD CONSTRAINT mccr_mccrregistry_pkey PRIMARY KEY (id);


--
-- TOC entry 3582 (class 2606 OID 113830)
-- Name: mccr_mccrregistryovvrelation mccr_mccrregistryovvrelation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_mccrregistryovvrelation
    ADD CONSTRAINT mccr_mccrregistryovvrelation_pkey PRIMARY KEY (id);


--
-- TOC entry 3578 (class 2606 OID 113803)
-- Name: mccr_mccrusertype mccr_mccrusertype_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_mccrusertype
    ADD CONSTRAINT mccr_mccrusertype_pkey PRIMARY KEY (id);


--
-- TOC entry 3591 (class 2606 OID 113868)
-- Name: mccr_mccrworkflowstep mccr_mccrworkflowstep_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_mccrworkflowstep
    ADD CONSTRAINT mccr_mccrworkflowstep_pkey PRIMARY KEY (id);


--
-- TOC entry 3594 (class 2606 OID 113876)
-- Name: mccr_mccrworkflowstepfile mccr_mccrworkflowstepfile_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_mccrworkflowstepfile
    ADD CONSTRAINT mccr_mccrworkflowstepfile_pkey PRIMARY KEY (id);


--
-- TOC entry 3584 (class 2606 OID 113838)
-- Name: mccr_ovv mccr_ovv_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_ovv
    ADD CONSTRAINT mccr_ovv_pkey PRIMARY KEY (id);


--
-- TOC entry 3609 (class 2606 OID 113965)
-- Name: mitigation_action_changelog mitigation_action_changelog_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_changelog
    ADD CONSTRAINT mitigation_action_changelog_pkey PRIMARY KEY (id);


--
-- TOC entry 3538 (class 2606 OID 113628)
-- Name: mitigation_action_contact mitigation_action_contact_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_contact
    ADD CONSTRAINT mitigation_action_contact_pkey PRIMARY KEY (id);


--
-- TOC entry 3540 (class 2606 OID 113636)
-- Name: mitigation_action_finance mitigation_action_finance_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_finance
    ADD CONSTRAINT mitigation_action_finance_pkey PRIMARY KEY (id);


--
-- TOC entry 3618 (class 2606 OID 114028)
-- Name: mitigation_action_financesourcetype mitigation_action_financesourcetype_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_financesourcetype
    ADD CONSTRAINT mitigation_action_financesourcetype_pkey PRIMARY KEY (id);


--
-- TOC entry 3628 (class 2606 OID 114194)
-- Name: mitigation_action_financestatus mitigation_action_financestatus_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_financestatus
    ADD CONSTRAINT mitigation_action_financestatus_pkey PRIMARY KEY (id);


--
-- TOC entry 3543 (class 2606 OID 113644)
-- Name: mitigation_action_geographicscale mitigation_action_geographicscale_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_geographicscale
    ADD CONSTRAINT mitigation_action_geographicscale_pkey PRIMARY KEY (id);


--
-- TOC entry 3545 (class 2606 OID 113652)
-- Name: mitigation_action_ingeicompliance mitigation_action_ingeicompliance_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_ingeicompliance
    ADD CONSTRAINT mitigation_action_ingeicompliance_pkey PRIMARY KEY (id);


--
-- TOC entry 3633 (class 2606 OID 114205)
-- Name: mitigation_action_initiative mitigation_action_initiative_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_initiative
    ADD CONSTRAINT mitigation_action_initiative_pkey PRIMARY KEY (id);


--
-- TOC entry 3637 (class 2606 OID 114213)
-- Name: mitigation_action_initiativefinance mitigation_action_initiativefinance_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_initiativefinance
    ADD CONSTRAINT mitigation_action_initiativefinance_pkey PRIMARY KEY (id);


--
-- TOC entry 3640 (class 2606 OID 114221)
-- Name: mitigation_action_initiativetype mitigation_action_initiativetype_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_initiativetype
    ADD CONSTRAINT mitigation_action_initiativetype_pkey PRIMARY KEY (id);


--
-- TOC entry 3547 (class 2606 OID 113660)
-- Name: mitigation_action_institution mitigation_action_institution_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_institution
    ADD CONSTRAINT mitigation_action_institution_pkey PRIMARY KEY (id);


--
-- TOC entry 3549 (class 2606 OID 113668)
-- Name: mitigation_action_location mitigation_action_location_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_location
    ADD CONSTRAINT mitigation_action_location_pkey PRIMARY KEY (id);


--
-- TOC entry 3621 (class 2606 OID 114134)
-- Name: mitigation_action_maworkflowstep mitigation_action_maworkflowstep_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_maworkflowstep
    ADD CONSTRAINT mitigation_action_maworkflowstep_pkey PRIMARY KEY (id);


--
-- TOC entry 3624 (class 2606 OID 114142)
-- Name: mitigation_action_maworkflowstepfile mitigation_action_maworkflowstepfile_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_maworkflowstepfile
    ADD CONSTRAINT mitigation_action_maworkflowstepfile_pkey PRIMARY KEY (id);


--
-- TOC entry 3612 (class 2606 OID 113993)
-- Name: mitigation_action_mitigation_comments mitigation_action_mitiga_mitigation_id_comment_id_e062b2f1_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_mitigation_comments
    ADD CONSTRAINT mitigation_action_mitiga_mitigation_id_comment_id_e062b2f1_uniq UNIQUE (mitigation_id, comment_id);


--
-- TOC entry 3602 (class 2606 OID 113955)
-- Name: mitigation_action_mitigation_ingei_compliances mitigation_action_mitiga_mitigation_id_ingeicompl_f69646fe_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_mitigation_ingei_compliances
    ADD CONSTRAINT mitigation_action_mitiga_mitigation_id_ingeicompl_f69646fe_uniq UNIQUE (mitigation_id, ingeicompliance_id);


--
-- TOC entry 3616 (class 2606 OID 113973)
-- Name: mitigation_action_mitigation_comments mitigation_action_mitigation_comments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_mitigation_comments
    ADD CONSTRAINT mitigation_action_mitigation_comments_pkey PRIMARY KEY (id);


--
-- TOC entry 3606 (class 2606 OID 113943)
-- Name: mitigation_action_mitigation_ingei_compliances mitigation_action_mitigation_ingei_compliances_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_mitigation_ingei_compliances
    ADD CONSTRAINT mitigation_action_mitigation_ingei_compliances_pkey PRIMARY KEY (id);


--
-- TOC entry 3559 (class 2606 OID 113676)
-- Name: mitigation_action_mitigation mitigation_action_mitigationaction_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_mitigation
    ADD CONSTRAINT mitigation_action_mitigationaction_pkey PRIMARY KEY (id);


--
-- TOC entry 3563 (class 2606 OID 113684)
-- Name: mitigation_action_progressindicator mitigation_action_progressindicator_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_progressindicator
    ADD CONSTRAINT mitigation_action_progressindicator_pkey PRIMARY KEY (id);


--
-- TOC entry 3565 (class 2606 OID 113692)
-- Name: mitigation_action_registrationtype mitigation_action_registrationtype_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_registrationtype
    ADD CONSTRAINT mitigation_action_registrationtype_pkey PRIMARY KEY (id);


--
-- TOC entry 3567 (class 2606 OID 113700)
-- Name: mitigation_action_status mitigation_action_status_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_status
    ADD CONSTRAINT mitigation_action_status_pkey PRIMARY KEY (id);


--
-- TOC entry 3690 (class 2606 OID 114602)
-- Name: ppcn_changelog ppcn_changelog_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_changelog
    ADD CONSTRAINT ppcn_changelog_pkey PRIMARY KEY (id);


--
-- TOC entry 3642 (class 2606 OID 114323)
-- Name: ppcn_emissionfactor ppcn_emissionfactor_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_emissionfactor
    ADD CONSTRAINT ppcn_emissionfactor_pkey PRIMARY KEY (id);


--
-- TOC entry 3700 (class 2606 OID 114666)
-- Name: ppcn_geiactivitytype ppcn_geiactivitytype_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_geiactivitytype
    ADD CONSTRAINT ppcn_geiactivitytype_pkey PRIMARY KEY (id);


--
-- TOC entry 3706 (class 2606 OID 114684)
-- Name: ppcn_geiorganization_gei_activity_types ppcn_geiorganization_gei_activity_types_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_geiorganization_gei_activity_types
    ADD CONSTRAINT ppcn_geiorganization_gei_activity_types_pkey PRIMARY KEY (id);


--
-- TOC entry 3708 (class 2606 OID 114726)
-- Name: ppcn_geiorganization_gei_activity_types ppcn_geiorganization_gei_geiorganization_id_geiac_43936059_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_geiorganization_gei_activity_types
    ADD CONSTRAINT ppcn_geiorganization_gei_geiorganization_id_geiac_43936059_uniq UNIQUE (geiorganization_id, geiactivitytype_id);


--
-- TOC entry 3658 (class 2606 OID 114408)
-- Name: ppcn_geiorganization ppcn_geiorganization_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_geiorganization
    ADD CONSTRAINT ppcn_geiorganization_pkey PRIMARY KEY (id);


--
-- TOC entry 3644 (class 2606 OID 114331)
-- Name: ppcn_inventorymethodology ppcn_inventorymethodology_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_inventorymethodology
    ADD CONSTRAINT ppcn_inventorymethodology_pkey PRIMARY KEY (id);


--
-- TOC entry 3646 (class 2606 OID 114339)
-- Name: ppcn_geographiclevel ppcn_level_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_geographiclevel
    ADD CONSTRAINT ppcn_level_pkey PRIMARY KEY (id);


--
-- TOC entry 3649 (class 2606 OID 114350)
-- Name: ppcn_organization ppcn_organization_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_organization
    ADD CONSTRAINT ppcn_organization_pkey PRIMARY KEY (id);


--
-- TOC entry 3651 (class 2606 OID 114358)
-- Name: ppcn_plusaction ppcn_plusaction_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_plusaction
    ADD CONSTRAINT ppcn_plusaction_pkey PRIMARY KEY (id);


--
-- TOC entry 3653 (class 2606 OID 114366)
-- Name: ppcn_potentialglobalwarming ppcn_potentialglobalwarming_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_potentialglobalwarming
    ADD CONSTRAINT ppcn_potentialglobalwarming_pkey PRIMARY KEY (id);


--
-- TOC entry 3695 (class 2606 OID 114610)
-- Name: ppcn_ppcn_comments ppcn_ppcn_comments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcn_comments
    ADD CONSTRAINT ppcn_ppcn_comments_pkey PRIMARY KEY (id);


--
-- TOC entry 3698 (class 2606 OID 114624)
-- Name: ppcn_ppcn_comments ppcn_ppcn_comments_ppcn_id_comment_id_ccb4e106_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcn_comments
    ADD CONSTRAINT ppcn_ppcn_comments_ppcn_id_comment_id_ccb4e106_uniq UNIQUE (ppcn_id, comment_id);


--
-- TOC entry 3677 (class 2606 OID 114474)
-- Name: ppcn_ppcn ppcn_ppcn_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcn
    ADD CONSTRAINT ppcn_ppcn_pkey PRIMARY KEY (id);


--
-- TOC entry 3670 (class 2606 OID 114466)
-- Name: ppcn_ppcnfile ppcn_ppcnfile_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcnfile
    ADD CONSTRAINT ppcn_ppcnfile_pkey PRIMARY KEY (id);


--
-- TOC entry 3682 (class 2606 OID 114562)
-- Name: ppcn_ppcnworkflowstep ppcn_ppcnworkflowstep_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcnworkflowstep
    ADD CONSTRAINT ppcn_ppcnworkflowstep_pkey PRIMARY KEY (id);


--
-- TOC entry 3686 (class 2606 OID 114570)
-- Name: ppcn_ppcnworkflowstepfile ppcn_ppcnworkflowstepfile_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcnworkflowstepfile
    ADD CONSTRAINT ppcn_ppcnworkflowstepfile_pkey PRIMARY KEY (id);


--
-- TOC entry 3655 (class 2606 OID 114374)
-- Name: ppcn_quantifiedgas ppcn_quantifiedgas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_quantifiedgas
    ADD CONSTRAINT ppcn_quantifiedgas_pkey PRIMARY KEY (id);


--
-- TOC entry 3660 (class 2606 OID 114416)
-- Name: ppcn_recognitiontype ppcn_recognitiontype_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_recognitiontype
    ADD CONSTRAINT ppcn_recognitiontype_pkey PRIMARY KEY (id);


--
-- TOC entry 3662 (class 2606 OID 114424)
-- Name: ppcn_requiredlevel ppcn_requiredlevel_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_requiredlevel
    ADD CONSTRAINT ppcn_requiredlevel_pkey PRIMARY KEY (id);


--
-- TOC entry 3665 (class 2606 OID 114432)
-- Name: ppcn_sector ppcn_sector_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_sector
    ADD CONSTRAINT ppcn_sector_pkey PRIMARY KEY (id);


--
-- TOC entry 3667 (class 2606 OID 114440)
-- Name: ppcn_subsector ppcn_subsector_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_subsector
    ADD CONSTRAINT ppcn_subsector_pkey PRIMARY KEY (id);


--
-- TOC entry 3710 (class 2606 OID 114741)
-- Name: report_data_reportfile report_data_reportfile_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_data_reportfile
    ADD CONSTRAINT report_data_reportfile_pkey PRIMARY KEY (id);


--
-- TOC entry 3720 (class 2606 OID 114810)
-- Name: report_data_reportfilemetadata report_data_reportfilemetadata_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_data_reportfilemetadata
    ADD CONSTRAINT report_data_reportfilemetadata_pkey PRIMARY KEY (id);


--
-- TOC entry 3713 (class 2606 OID 114753)
-- Name: report_data_reportfileversion report_data_reportfileversion_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_data_reportfileversion
    ADD CONSTRAINT report_data_reportfileversion_pkey PRIMARY KEY (id);


--
-- TOC entry 3718 (class 2606 OID 114779)
-- Name: report_data_reportfileversion report_data_reportfileversion_version_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_data_reportfileversion
    ADD CONSTRAINT report_data_reportfileversion_version_key UNIQUE (version);


--
-- TOC entry 3523 (class 2606 OID 113576)
-- Name: users_customuser_groups users_customuser_groups_customuser_id_group_id_76b619e3_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_customuser_groups
    ADD CONSTRAINT users_customuser_groups_customuser_id_group_id_76b619e3_uniq UNIQUE (customuser_id, group_id);


--
-- TOC entry 3526 (class 2606 OID 113555)
-- Name: users_customuser_groups users_customuser_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_customuser_groups
    ADD CONSTRAINT users_customuser_groups_pkey PRIMARY KEY (id);


--
-- TOC entry 3517 (class 2606 OID 113545)
-- Name: users_customuser users_customuser_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_customuser
    ADD CONSTRAINT users_customuser_pkey PRIMARY KEY (id);


--
-- TOC entry 3528 (class 2606 OID 113590)
-- Name: users_customuser_user_permissions users_customuser_user_pe_customuser_id_permission_7a7debf6_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_customuser_user_permissions
    ADD CONSTRAINT users_customuser_user_pe_customuser_id_permission_7a7debf6_uniq UNIQUE (customuser_id, permission_id);


--
-- TOC entry 3532 (class 2606 OID 113563)
-- Name: users_customuser_user_permissions users_customuser_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_customuser_user_permissions
    ADD CONSTRAINT users_customuser_user_permissions_pkey PRIMARY KEY (id);


--
-- TOC entry 3520 (class 2606 OID 113547)
-- Name: users_customuser users_customuser_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_customuser
    ADD CONSTRAINT users_customuser_username_key UNIQUE (username);


--
-- TOC entry 3598 (class 2606 OID 113926)
-- Name: workflow_comment workflow_comment_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflow_comment
    ADD CONSTRAINT workflow_comment_pkey PRIMARY KEY (id);


--
-- TOC entry 3600 (class 2606 OID 113934)
-- Name: workflow_reviewstatus workflow_reviewstatus_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflow_reviewstatus
    ADD CONSTRAINT workflow_reviewstatus_pkey PRIMARY KEY (id);


--
-- TOC entry 3505 (class 1259 OID 113520)
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- TOC entry 3510 (class 1259 OID 113533)
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- TOC entry 3513 (class 1259 OID 113534)
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- TOC entry 3500 (class 1259 OID 113519)
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- TOC entry 3533 (class 1259 OID 113615)
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- TOC entry 3536 (class 1259 OID 113616)
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- TOC entry 3722 (class 1259 OID 114826)
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- TOC entry 3725 (class 1259 OID 114825)
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- TOC entry 3587 (class 1259 OID 113902)
-- Name: mccr_changelog_ppcn_id_adeaca0d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mccr_changelog_ppcn_id_adeaca0d ON public.mccr_changelog USING btree (mccr_id);


--
-- TOC entry 3588 (class 1259 OID 113908)
-- Name: mccr_changelog_user_id_4678b3eb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mccr_changelog_user_id_4678b3eb ON public.mccr_changelog USING btree (user_id);


--
-- TOC entry 3568 (class 1259 OID 113783)
-- Name: mccr_mccrfile_mccr_id_08c07172; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mccr_mccrfile_mccr_id_08c07172 ON public.mccr_mccrfile USING btree (mccr_id);


--
-- TOC entry 3571 (class 1259 OID 113789)
-- Name: mccr_mccrfile_user_id_517351bd; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mccr_mccrfile_user_id_517351bd ON public.mccr_mccrfile USING btree (user_id);


--
-- TOC entry 3572 (class 1259 OID 113781)
-- Name: mccr_mccrregistry_mitigation_id_42e7601c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mccr_mccrregistry_mitigation_id_42e7601c ON public.mccr_mccrregistry USING btree (mitigation_id);


--
-- TOC entry 3575 (class 1259 OID 113782)
-- Name: mccr_mccrregistry_user_id_8ce12972; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mccr_mccrregistry_user_id_8ce12972 ON public.mccr_mccrregistry USING btree (user_id);


--
-- TOC entry 3576 (class 1259 OID 113810)
-- Name: mccr_mccrregistry_user_type_id_36dc1127; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mccr_mccrregistry_user_type_id_36dc1127 ON public.mccr_mccrregistry USING btree (user_type_id);


--
-- TOC entry 3579 (class 1259 OID 113841)
-- Name: mccr_mccrregistryovvrelation_mccr_id_6c978edf; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mccr_mccrregistryovvrelation_mccr_id_6c978edf ON public.mccr_mccrregistryovvrelation USING btree (mccr_id);


--
-- TOC entry 3580 (class 1259 OID 113847)
-- Name: mccr_mccrregistryovvrelation_ovv_id_25f87d39; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mccr_mccrregistryovvrelation_ovv_id_25f87d39 ON public.mccr_mccrregistryovvrelation USING btree (ovv_id);


--
-- TOC entry 3589 (class 1259 OID 113890)
-- Name: mccr_mccrworkflowstep_mccr_id_00c7d236; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mccr_mccrworkflowstep_mccr_id_00c7d236 ON public.mccr_mccrworkflowstep USING btree (mccr_id);


--
-- TOC entry 3592 (class 1259 OID 113896)
-- Name: mccr_mccrworkflowstep_user_id_c48a5841; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mccr_mccrworkflowstep_user_id_c48a5841 ON public.mccr_mccrworkflowstep USING btree (user_id);


--
-- TOC entry 3595 (class 1259 OID 113888)
-- Name: mccr_mccrworkflowstepfile_user_id_0c2c21c3; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mccr_mccrworkflowstepfile_user_id_0c2c21c3 ON public.mccr_mccrworkflowstepfile USING btree (user_id);


--
-- TOC entry 3596 (class 1259 OID 113889)
-- Name: mccr_mccrworkflowstepfile_workflow_step_id_a4e95d21; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mccr_mccrworkflowstepfile_workflow_step_id_a4e95d21 ON public.mccr_mccrworkflowstepfile USING btree (workflow_step_id);


--
-- TOC entry 3607 (class 1259 OID 114002)
-- Name: mitigation_action_changelog_mitigation_action_id_a4801a1b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_changelog_mitigation_action_id_a4801a1b ON public.mitigation_action_changelog USING btree (mitigation_action_id);


--
-- TOC entry 3610 (class 1259 OID 114014)
-- Name: mitigation_action_changelog_user_id_c0f7d427; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_changelog_user_id_c0f7d427 ON public.mitigation_action_changelog USING btree (user_id);


--
-- TOC entry 3541 (class 1259 OID 114298)
-- Name: mitigation_action_finance_status_id_a940da2d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_finance_status_id_a940da2d ON public.mitigation_action_finance USING btree (status_id);


--
-- TOC entry 3635 (class 1259 OID 114278)
-- Name: mitigation_action_initiati_finance_source_type_id_1d97a554; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_initiati_finance_source_type_id_1d97a554 ON public.mitigation_action_initiativefinance USING btree (finance_source_type_id);


--
-- TOC entry 3629 (class 1259 OID 114267)
-- Name: mitigation_action_initiative_contact_id_b4f438da; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_initiative_contact_id_b4f438da ON public.mitigation_action_initiative USING btree (contact_id);


--
-- TOC entry 3630 (class 1259 OID 114280)
-- Name: mitigation_action_initiative_finance_id_605f54db; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_initiative_finance_id_605f54db ON public.mitigation_action_initiative USING btree (finance_id);


--
-- TOC entry 3631 (class 1259 OID 114286)
-- Name: mitigation_action_initiative_initiative_type_id_54661d5b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_initiative_initiative_type_id_54661d5b ON public.mitigation_action_initiative USING btree (initiative_type_id);


--
-- TOC entry 3634 (class 1259 OID 114292)
-- Name: mitigation_action_initiative_status_id_44027193; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_initiative_status_id_44027193 ON public.mitigation_action_initiative USING btree (status_id);


--
-- TOC entry 3638 (class 1259 OID 114279)
-- Name: mitigation_action_initiativefinance_status_id_fa3cebf4; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_initiativefinance_status_id_fa3cebf4 ON public.mitigation_action_initiativefinance USING btree (status_id);


--
-- TOC entry 3619 (class 1259 OID 114153)
-- Name: mitigation_action_maworkflowstep_mitigation_action_id_e3bbba48; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_maworkflowstep_mitigation_action_id_e3bbba48 ON public.mitigation_action_maworkflowstep USING btree (mitigation_action_id);


--
-- TOC entry 3622 (class 1259 OID 114154)
-- Name: mitigation_action_maworkflowstep_user_id_f1494fbc; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_maworkflowstep_user_id_f1494fbc ON public.mitigation_action_maworkflowstep USING btree (user_id);


--
-- TOC entry 3625 (class 1259 OID 114165)
-- Name: mitigation_action_maworkflowstepfile_user_id_67fc87e2; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_maworkflowstepfile_user_id_67fc87e2 ON public.mitigation_action_maworkflowstepfile USING btree (user_id);


--
-- TOC entry 3626 (class 1259 OID 114166)
-- Name: mitigation_action_maworkflowstepfile_workflow_step_id_0cba48d8; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_maworkflowstepfile_workflow_step_id_0cba48d8 ON public.mitigation_action_maworkflowstepfile USING btree (workflow_step_id);


--
-- TOC entry 3603 (class 1259 OID 113957)
-- Name: mitigation_action_mitigati_ingeicompliance_id_3a83b0d9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_mitigati_ingeicompliance_id_3a83b0d9 ON public.mitigation_action_mitigation_ingei_compliances USING btree (ingeicompliance_id);


--
-- TOC entry 3604 (class 1259 OID 113956)
-- Name: mitigation_action_mitigati_mitigation_id_f4c4460f; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_mitigati_mitigation_id_f4c4460f ON public.mitigation_action_mitigation_ingei_compliances USING btree (mitigation_id);


--
-- TOC entry 3550 (class 1259 OID 113737)
-- Name: mitigation_action_mitigati_progress_indicator_id_a7e7a5fb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_mitigati_progress_indicator_id_a7e7a5fb ON public.mitigation_action_mitigation USING btree (progress_indicator_id);


--
-- TOC entry 3551 (class 1259 OID 113743)
-- Name: mitigation_action_mitigati_registration_type_id_794241da; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_mitigati_registration_type_id_794241da ON public.mitigation_action_mitigation USING btree (registration_type_id);


--
-- TOC entry 3613 (class 1259 OID 113995)
-- Name: mitigation_action_mitigation_comments_comment_id_d430a9a4; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_mitigation_comments_comment_id_d430a9a4 ON public.mitigation_action_mitigation_comments USING btree (comment_id);


--
-- TOC entry 3614 (class 1259 OID 113994)
-- Name: mitigation_action_mitigation_comments_mitigation_id_98b68b5f; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_mitigation_comments_mitigation_id_98b68b5f ON public.mitigation_action_mitigation_comments USING btree (mitigation_id);


--
-- TOC entry 3552 (class 1259 OID 114304)
-- Name: mitigation_action_mitigation_initiative_id_342cab00; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_mitigation_initiative_id_342cab00 ON public.mitigation_action_mitigation USING btree (initiative_id);


--
-- TOC entry 3553 (class 1259 OID 113731)
-- Name: mitigation_action_mitigationaction_contact_id_ad72c37c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_mitigationaction_contact_id_ad72c37c ON public.mitigation_action_mitigation USING btree (contact_id);


--
-- TOC entry 3554 (class 1259 OID 113732)
-- Name: mitigation_action_mitigationaction_finance_id_955ea6ac; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_mitigationaction_finance_id_955ea6ac ON public.mitigation_action_mitigation USING btree (finance_id);


--
-- TOC entry 3555 (class 1259 OID 113733)
-- Name: mitigation_action_mitigationaction_geographic_scale_id_a33fc61e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_mitigationaction_geographic_scale_id_a33fc61e ON public.mitigation_action_mitigation USING btree (geographic_scale_id);


--
-- TOC entry 3556 (class 1259 OID 113735)
-- Name: mitigation_action_mitigationaction_institution_id_b189af89; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_mitigationaction_institution_id_b189af89 ON public.mitigation_action_mitigation USING btree (institution_id);


--
-- TOC entry 3557 (class 1259 OID 113736)
-- Name: mitigation_action_mitigationaction_location_id_2770ab5d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_mitigationaction_location_id_2770ab5d ON public.mitigation_action_mitigation USING btree (location_id);


--
-- TOC entry 3560 (class 1259 OID 113749)
-- Name: mitigation_action_mitigationaction_status_id_4a0647fc; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_mitigationaction_status_id_4a0647fc ON public.mitigation_action_mitigation USING btree (status_id);


--
-- TOC entry 3561 (class 1259 OID 113755)
-- Name: mitigation_action_mitigationaction_user_id_b61093af; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_mitigationaction_user_id_b61093af ON public.mitigation_action_mitigation USING btree (user_id);


--
-- TOC entry 3691 (class 1259 OID 114627)
-- Name: ppcn_changelog_ppcn_id_59e2c714; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ppcn_changelog_ppcn_id_59e2c714 ON public.ppcn_changelog USING btree (ppcn_id);


--
-- TOC entry 3692 (class 1259 OID 114633)
-- Name: ppcn_changelog_user_id_bb4cef6f; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ppcn_changelog_user_id_bb4cef6f ON public.ppcn_changelog USING btree (user_id);


--
-- TOC entry 3701 (class 1259 OID 114695)
-- Name: ppcn_geiactivitytype_sector_id_c7f8fcfb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ppcn_geiactivitytype_sector_id_c7f8fcfb ON public.ppcn_geiactivitytype USING btree (sector_id);


--
-- TOC entry 3702 (class 1259 OID 114696)
-- Name: ppcn_geiactivitytype_sub_sector_id_c1e19ae2; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ppcn_geiactivitytype_sub_sector_id_c1e19ae2 ON public.ppcn_geiactivitytype USING btree (sub_sector_id);


--
-- TOC entry 3703 (class 1259 OID 114728)
-- Name: ppcn_geiorganization_gei_a_geiactivitytype_id_048f50be; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ppcn_geiorganization_gei_a_geiactivitytype_id_048f50be ON public.ppcn_geiorganization_gei_activity_types USING btree (geiactivitytype_id);


--
-- TOC entry 3704 (class 1259 OID 114727)
-- Name: ppcn_geiorganization_gei_a_geiorganization_id_82dd23c3; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ppcn_geiorganization_gei_a_geiorganization_id_82dd23c3 ON public.ppcn_geiorganization_gei_activity_types USING btree (geiorganization_id);


--
-- TOC entry 3656 (class 1259 OID 114644)
-- Name: ppcn_geiorganization_ovv_id_17530bac; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ppcn_geiorganization_ovv_id_17530bac ON public.ppcn_geiorganization USING btree (ovv_id);


--
-- TOC entry 3647 (class 1259 OID 114393)
-- Name: ppcn_organization_contact_id_d94c7c13; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ppcn_organization_contact_id_d94c7c13 ON public.ppcn_organization USING btree (contact_id);


--
-- TOC entry 3693 (class 1259 OID 114626)
-- Name: ppcn_ppcn_comments_comment_id_82a722c9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ppcn_ppcn_comments_comment_id_82a722c9 ON public.ppcn_ppcn_comments USING btree (comment_id);


--
-- TOC entry 3696 (class 1259 OID 114625)
-- Name: ppcn_ppcn_comments_ppcn_id_3a7defde; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ppcn_ppcn_comments_ppcn_id_3a7defde ON public.ppcn_ppcn_comments USING btree (ppcn_id);


--
-- TOC entry 3673 (class 1259 OID 114650)
-- Name: ppcn_ppcn_gei_organization_id_debbc419; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ppcn_ppcn_gei_organization_id_debbc419 ON public.ppcn_ppcn USING btree (gei_organization_id);


--
-- TOC entry 3674 (class 1259 OID 114697)
-- Name: ppcn_ppcn_geographic_level_id_c1066abb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ppcn_ppcn_geographic_level_id_c1066abb ON public.ppcn_ppcn USING btree (geographic_level_id);


--
-- TOC entry 3675 (class 1259 OID 114506)
-- Name: ppcn_ppcn_organization_id_7c48620d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ppcn_ppcn_organization_id_7c48620d ON public.ppcn_ppcn USING btree (organization_id);


--
-- TOC entry 3678 (class 1259 OID 114703)
-- Name: ppcn_ppcn_recognition_type_id_1bee6248; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ppcn_ppcn_recognition_type_id_1bee6248 ON public.ppcn_ppcn USING btree (recognition_type_id);


--
-- TOC entry 3679 (class 1259 OID 114709)
-- Name: ppcn_ppcn_required_level_id_da88f790; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ppcn_ppcn_required_level_id_da88f790 ON public.ppcn_ppcn USING btree (required_level_id);


--
-- TOC entry 3680 (class 1259 OID 114523)
-- Name: ppcn_ppcn_user_id_41508d8e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ppcn_ppcn_user_id_41508d8e ON public.ppcn_ppcn USING btree (user_id);


--
-- TOC entry 3671 (class 1259 OID 114511)
-- Name: ppcn_ppcnfile_ppcn_form_id_258b17a5; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ppcn_ppcnfile_ppcn_form_id_258b17a5 ON public.ppcn_ppcnfile USING btree (ppcn_form_id);


--
-- TOC entry 3672 (class 1259 OID 114517)
-- Name: ppcn_ppcnfile_user_id_de589eff; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ppcn_ppcnfile_user_id_de589eff ON public.ppcn_ppcnfile USING btree (user_id);


--
-- TOC entry 3683 (class 1259 OID 114581)
-- Name: ppcn_ppcnworkflowstep_ppcn_id_e0c05733; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ppcn_ppcnworkflowstep_ppcn_id_e0c05733 ON public.ppcn_ppcnworkflowstep USING btree (ppcn_id);


--
-- TOC entry 3684 (class 1259 OID 114582)
-- Name: ppcn_ppcnworkflowstep_user_id_33177343; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ppcn_ppcnworkflowstep_user_id_33177343 ON public.ppcn_ppcnworkflowstep USING btree (user_id);


--
-- TOC entry 3687 (class 1259 OID 114593)
-- Name: ppcn_ppcnworkflowstepfile_user_id_345e37d6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ppcn_ppcnworkflowstepfile_user_id_345e37d6 ON public.ppcn_ppcnworkflowstepfile USING btree (user_id);


--
-- TOC entry 3688 (class 1259 OID 114594)
-- Name: ppcn_ppcnworkflowstepfile_workflow_step_id_29a9efd3; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ppcn_ppcnworkflowstepfile_workflow_step_id_29a9efd3 ON public.ppcn_ppcnworkflowstepfile USING btree (workflow_step_id);


--
-- TOC entry 3663 (class 1259 OID 114453)
-- Name: ppcn_sector_geographicLevel_id_8827ad6c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "ppcn_sector_geographicLevel_id_8827ad6c" ON public.ppcn_sector USING btree ("geographicLevel_id");


--
-- TOC entry 3668 (class 1259 OID 114447)
-- Name: ppcn_subsector_sector_id_0a8366aa; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ppcn_subsector_sector_id_0a8366aa ON public.ppcn_subsector USING btree (sector_id);


--
-- TOC entry 3711 (class 1259 OID 114790)
-- Name: report_data_reportfile_user_id_96d75ab0; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX report_data_reportfile_user_id_96d75ab0 ON public.report_data_reportfile USING btree (user_id);


--
-- TOC entry 3721 (class 1259 OID 114816)
-- Name: report_data_reportfilemetadata_report_file_id_4f18b601; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX report_data_reportfilemetadata_report_file_id_4f18b601 ON public.report_data_reportfilemetadata USING btree (report_file_id);


--
-- TOC entry 3714 (class 1259 OID 114783)
-- Name: report_data_reportfileversion_report_file_id_3d0c13cb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX report_data_reportfileversion_report_file_id_3d0c13cb ON public.report_data_reportfileversion USING btree (report_file_id);


--
-- TOC entry 3715 (class 1259 OID 114797)
-- Name: report_data_reportfileversion_user_id_c0ab27e1; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX report_data_reportfileversion_user_id_c0ab27e1 ON public.report_data_reportfileversion USING btree (user_id);


--
-- TOC entry 3716 (class 1259 OID 114780)
-- Name: report_data_reportfileversion_version_16e5e2f7_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX report_data_reportfileversion_version_16e5e2f7_like ON public.report_data_reportfileversion USING btree (version varchar_pattern_ops);


--
-- TOC entry 3521 (class 1259 OID 113577)
-- Name: users_customuser_groups_customuser_id_958147bf; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX users_customuser_groups_customuser_id_958147bf ON public.users_customuser_groups USING btree (customuser_id);


--
-- TOC entry 3524 (class 1259 OID 113578)
-- Name: users_customuser_groups_group_id_01390b14; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX users_customuser_groups_group_id_01390b14 ON public.users_customuser_groups USING btree (group_id);


--
-- TOC entry 3529 (class 1259 OID 113591)
-- Name: users_customuser_user_permissions_customuser_id_5771478b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX users_customuser_user_permissions_customuser_id_5771478b ON public.users_customuser_user_permissions USING btree (customuser_id);


--
-- TOC entry 3530 (class 1259 OID 113592)
-- Name: users_customuser_user_permissions_permission_id_baaa2f74; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX users_customuser_user_permissions_permission_id_baaa2f74 ON public.users_customuser_user_permissions USING btree (permission_id);


--
-- TOC entry 3518 (class 1259 OID 113564)
-- Name: users_customuser_username_80452fdf_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX users_customuser_username_80452fdf_like ON public.users_customuser USING btree (username varchar_pattern_ops);


--
-- TOC entry 3728 (class 2606 OID 113526)
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3727 (class 2606 OID 113521)
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3726 (class 2606 OID 113512)
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3733 (class 2606 OID 113605)
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3734 (class 2606 OID 113610)
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_users_customuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_users_customuser_id FOREIGN KEY (user_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3754 (class 2606 OID 113914)
-- Name: mccr_changelog mccr_changelog_mccr_id_1b6a3dff_fk_mccr_mccrregistry_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_changelog
    ADD CONSTRAINT mccr_changelog_mccr_id_1b6a3dff_fk_mccr_mccrregistry_id FOREIGN KEY (mccr_id) REFERENCES public.mccr_mccrregistry(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3753 (class 2606 OID 113909)
-- Name: mccr_changelog mccr_changelog_user_id_4678b3eb_fk_users_customuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_changelog
    ADD CONSTRAINT mccr_changelog_user_id_4678b3eb_fk_users_customuser_id FOREIGN KEY (user_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3747 (class 2606 OID 113816)
-- Name: mccr_mccrfile mccr_mccrfile_mccr_id_08c07172_fk_mccr_mccrregistry_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_mccrfile
    ADD CONSTRAINT mccr_mccrfile_mccr_id_08c07172_fk_mccr_mccrregistry_id FOREIGN KEY (mccr_id) REFERENCES public.mccr_mccrregistry(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3746 (class 2606 OID 113790)
-- Name: mccr_mccrfile mccr_mccrfile_user_id_517351bd_fk_users_customuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_mccrfile
    ADD CONSTRAINT mccr_mccrfile_user_id_517351bd_fk_users_customuser_id FOREIGN KEY (user_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3748 (class 2606 OID 113771)
-- Name: mccr_mccrregistry mccr_mccrregistry_mitigation_id_42e7601c_fk_mitigatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_mccrregistry
    ADD CONSTRAINT mccr_mccrregistry_mitigation_id_42e7601c_fk_mitigatio FOREIGN KEY (mitigation_id) REFERENCES public.mitigation_action_mitigation(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3749 (class 2606 OID 113776)
-- Name: mccr_mccrregistry mccr_mccrregistry_user_id_8ce12972_fk_users_customuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_mccrregistry
    ADD CONSTRAINT mccr_mccrregistry_user_id_8ce12972_fk_users_customuser_id FOREIGN KEY (user_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3750 (class 2606 OID 113811)
-- Name: mccr_mccrregistry mccr_mccrregistry_user_type_id_36dc1127_fk_mccr_mccrusertype_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_mccrregistry
    ADD CONSTRAINT mccr_mccrregistry_user_type_id_36dc1127_fk_mccr_mccrusertype_id FOREIGN KEY (user_type_id) REFERENCES public.mccr_mccrusertype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3751 (class 2606 OID 113842)
-- Name: mccr_mccrregistryovvrelation mccr_mccrregistryovv_mccr_id_6c978edf_fk_mccr_mccr; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_mccrregistryovvrelation
    ADD CONSTRAINT mccr_mccrregistryovv_mccr_id_6c978edf_fk_mccr_mccr FOREIGN KEY (mccr_id) REFERENCES public.mccr_mccrregistry(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3752 (class 2606 OID 113848)
-- Name: mccr_mccrregistryovvrelation mccr_mccrregistryovvrelation_ovv_id_25f87d39_fk_mccr_ovv_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_mccrregistryovvrelation
    ADD CONSTRAINT mccr_mccrregistryovvrelation_ovv_id_25f87d39_fk_mccr_ovv_id FOREIGN KEY (ovv_id) REFERENCES public.mccr_ovv(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3757 (class 2606 OID 113878)
-- Name: mccr_mccrworkflowstepfile mccr_mccrworkflowste_user_id_0c2c21c3_fk_users_cus; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_mccrworkflowstepfile
    ADD CONSTRAINT mccr_mccrworkflowste_user_id_0c2c21c3_fk_users_cus FOREIGN KEY (user_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3758 (class 2606 OID 113883)
-- Name: mccr_mccrworkflowstepfile mccr_mccrworkflowste_workflow_step_id_a4e95d21_fk_mccr_mccr; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_mccrworkflowstepfile
    ADD CONSTRAINT mccr_mccrworkflowste_workflow_step_id_a4e95d21_fk_mccr_mccr FOREIGN KEY (workflow_step_id) REFERENCES public.mccr_mccrworkflowstep(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3755 (class 2606 OID 113891)
-- Name: mccr_mccrworkflowstep mccr_mccrworkflowstep_mccr_id_00c7d236_fk_mccr_mccrregistry_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_mccrworkflowstep
    ADD CONSTRAINT mccr_mccrworkflowstep_mccr_id_00c7d236_fk_mccr_mccrregistry_id FOREIGN KEY (mccr_id) REFERENCES public.mccr_mccrregistry(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3756 (class 2606 OID 113897)
-- Name: mccr_mccrworkflowstep mccr_mccrworkflowstep_user_id_c48a5841_fk_users_customuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_mccrworkflowstep
    ADD CONSTRAINT mccr_mccrworkflowstep_user_id_c48a5841_fk_users_customuser_id FOREIGN KEY (user_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3761 (class 2606 OID 114003)
-- Name: mitigation_action_changelog mitigation_action_ch_mitigation_action_id_a4801a1b_fk_mitigatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_changelog
    ADD CONSTRAINT mitigation_action_ch_mitigation_action_id_a4801a1b_fk_mitigatio FOREIGN KEY (mitigation_action_id) REFERENCES public.mitigation_action_mitigation(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3762 (class 2606 OID 114015)
-- Name: mitigation_action_changelog mitigation_action_ch_user_id_c0f7d427_fk_users_cus; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_changelog
    ADD CONSTRAINT mitigation_action_ch_user_id_c0f7d427_fk_users_cus FOREIGN KEY (user_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3735 (class 2606 OID 114299)
-- Name: mitigation_action_finance mitigation_action_fi_status_id_a940da2d_fk_mitigatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_finance
    ADD CONSTRAINT mitigation_action_fi_status_id_a940da2d_fk_mitigatio FOREIGN KEY (status_id) REFERENCES public.mitigation_action_financestatus(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3769 (class 2606 OID 114262)
-- Name: mitigation_action_initiative mitigation_action_in_contact_id_b4f438da_fk_mitigatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_initiative
    ADD CONSTRAINT mitigation_action_in_contact_id_b4f438da_fk_mitigatio FOREIGN KEY (contact_id) REFERENCES public.mitigation_action_contact(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3770 (class 2606 OID 114281)
-- Name: mitigation_action_initiative mitigation_action_in_finance_id_605f54db_fk_mitigatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_initiative
    ADD CONSTRAINT mitigation_action_in_finance_id_605f54db_fk_mitigatio FOREIGN KEY (finance_id) REFERENCES public.mitigation_action_initiativefinance(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3773 (class 2606 OID 114268)
-- Name: mitigation_action_initiativefinance mitigation_action_in_finance_source_type__1d97a554_fk_mitigatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_initiativefinance
    ADD CONSTRAINT mitigation_action_in_finance_source_type__1d97a554_fk_mitigatio FOREIGN KEY (finance_source_type_id) REFERENCES public.mitigation_action_financesourcetype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3771 (class 2606 OID 114287)
-- Name: mitigation_action_initiative mitigation_action_in_initiative_type_id_54661d5b_fk_mitigatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_initiative
    ADD CONSTRAINT mitigation_action_in_initiative_type_id_54661d5b_fk_mitigatio FOREIGN KEY (initiative_type_id) REFERENCES public.mitigation_action_initiativetype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3772 (class 2606 OID 114293)
-- Name: mitigation_action_initiative mitigation_action_in_status_id_44027193_fk_mitigatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_initiative
    ADD CONSTRAINT mitigation_action_in_status_id_44027193_fk_mitigatio FOREIGN KEY (status_id) REFERENCES public.mitigation_action_status(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3774 (class 2606 OID 114273)
-- Name: mitigation_action_initiativefinance mitigation_action_in_status_id_fa3cebf4_fk_mitigatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_initiativefinance
    ADD CONSTRAINT mitigation_action_in_status_id_fa3cebf4_fk_mitigatio FOREIGN KEY (status_id) REFERENCES public.mitigation_action_financestatus(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3765 (class 2606 OID 114167)
-- Name: mitigation_action_maworkflowstep mitigation_action_ma_mitigation_action_id_e3bbba48_fk_mitigatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_maworkflowstep
    ADD CONSTRAINT mitigation_action_ma_mitigation_action_id_e3bbba48_fk_mitigatio FOREIGN KEY (mitigation_action_id) REFERENCES public.mitigation_action_mitigation(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3767 (class 2606 OID 114177)
-- Name: mitigation_action_maworkflowstepfile mitigation_action_ma_user_id_67fc87e2_fk_users_cus; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_maworkflowstepfile
    ADD CONSTRAINT mitigation_action_ma_user_id_67fc87e2_fk_users_cus FOREIGN KEY (user_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3766 (class 2606 OID 114172)
-- Name: mitigation_action_maworkflowstep mitigation_action_ma_user_id_f1494fbc_fk_users_cus; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_maworkflowstep
    ADD CONSTRAINT mitigation_action_ma_user_id_f1494fbc_fk_users_cus FOREIGN KEY (user_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3768 (class 2606 OID 114182)
-- Name: mitigation_action_maworkflowstepfile mitigation_action_ma_workflow_step_id_0cba48d8_fk_mitigatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_maworkflowstepfile
    ADD CONSTRAINT mitigation_action_ma_workflow_step_id_0cba48d8_fk_mitigatio FOREIGN KEY (workflow_step_id) REFERENCES public.mitigation_action_maworkflowstep(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3763 (class 2606 OID 114036)
-- Name: mitigation_action_mitigation_comments mitigation_action_mi_comment_id_d430a9a4_fk_workflow_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_mitigation_comments
    ADD CONSTRAINT mitigation_action_mi_comment_id_d430a9a4_fk_workflow_ FOREIGN KEY (comment_id) REFERENCES public.workflow_comment(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3737 (class 2606 OID 114222)
-- Name: mitigation_action_mitigation mitigation_action_mi_contact_id_b84fb28c_fk_mitigatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_mitigation
    ADD CONSTRAINT mitigation_action_mi_contact_id_b84fb28c_fk_mitigatio FOREIGN KEY (contact_id) REFERENCES public.mitigation_action_contact(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3738 (class 2606 OID 114227)
-- Name: mitigation_action_mitigation mitigation_action_mi_finance_id_b7a14603_fk_mitigatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_mitigation
    ADD CONSTRAINT mitigation_action_mi_finance_id_b7a14603_fk_mitigatio FOREIGN KEY (finance_id) REFERENCES public.mitigation_action_finance(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3739 (class 2606 OID 114232)
-- Name: mitigation_action_mitigation mitigation_action_mi_geographic_scale_id_c6c7ec6a_fk_mitigatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_mitigation
    ADD CONSTRAINT mitigation_action_mi_geographic_scale_id_c6c7ec6a_fk_mitigatio FOREIGN KEY (geographic_scale_id) REFERENCES public.mitigation_action_geographicscale(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3760 (class 2606 OID 113949)
-- Name: mitigation_action_mitigation_ingei_compliances mitigation_action_mi_ingeicompliance_id_3a83b0d9_fk_mitigatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_mitigation_ingei_compliances
    ADD CONSTRAINT mitigation_action_mi_ingeicompliance_id_3a83b0d9_fk_mitigatio FOREIGN KEY (ingeicompliance_id) REFERENCES public.mitigation_action_ingeicompliance(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3745 (class 2606 OID 114305)
-- Name: mitigation_action_mitigation mitigation_action_mi_initiative_id_342cab00_fk_mitigatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_mitigation
    ADD CONSTRAINT mitigation_action_mi_initiative_id_342cab00_fk_mitigatio FOREIGN KEY (initiative_id) REFERENCES public.mitigation_action_initiative(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3740 (class 2606 OID 114237)
-- Name: mitigation_action_mitigation mitigation_action_mi_institution_id_06109e57_fk_mitigatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_mitigation
    ADD CONSTRAINT mitigation_action_mi_institution_id_06109e57_fk_mitigatio FOREIGN KEY (institution_id) REFERENCES public.mitigation_action_institution(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3741 (class 2606 OID 114242)
-- Name: mitigation_action_mitigation mitigation_action_mi_location_id_01de67fe_fk_mitigatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_mitigation
    ADD CONSTRAINT mitigation_action_mi_location_id_01de67fe_fk_mitigatio FOREIGN KEY (location_id) REFERENCES public.mitigation_action_location(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3764 (class 2606 OID 114041)
-- Name: mitigation_action_mitigation_comments mitigation_action_mi_mitigation_id_98b68b5f_fk_mitigatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_mitigation_comments
    ADD CONSTRAINT mitigation_action_mi_mitigation_id_98b68b5f_fk_mitigatio FOREIGN KEY (mitigation_id) REFERENCES public.mitigation_action_mitigation(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3759 (class 2606 OID 113944)
-- Name: mitigation_action_mitigation_ingei_compliances mitigation_action_mi_mitigation_id_f4c4460f_fk_mitigatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_mitigation_ingei_compliances
    ADD CONSTRAINT mitigation_action_mi_mitigation_id_f4c4460f_fk_mitigatio FOREIGN KEY (mitigation_id) REFERENCES public.mitigation_action_mitigation(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3742 (class 2606 OID 114247)
-- Name: mitigation_action_mitigation mitigation_action_mi_progress_indicator_i_a9ea5158_fk_mitigatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_mitigation
    ADD CONSTRAINT mitigation_action_mi_progress_indicator_i_a9ea5158_fk_mitigatio FOREIGN KEY (progress_indicator_id) REFERENCES public.mitigation_action_progressindicator(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3743 (class 2606 OID 114252)
-- Name: mitigation_action_mitigation mitigation_action_mi_registration_type_id_51575b17_fk_mitigatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_mitigation
    ADD CONSTRAINT mitigation_action_mi_registration_type_id_51575b17_fk_mitigatio FOREIGN KEY (registration_type_id) REFERENCES public.mitigation_action_registrationtype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3744 (class 2606 OID 114257)
-- Name: mitigation_action_mitigation mitigation_action_mi_status_id_820e5056_fk_mitigatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_mitigation
    ADD CONSTRAINT mitigation_action_mi_status_id_820e5056_fk_mitigatio FOREIGN KEY (status_id) REFERENCES public.mitigation_action_status(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3736 (class 2606 OID 113756)
-- Name: mitigation_action_mitigation mitigation_action_mi_user_id_b61093af_fk_users_cus; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_mitigation
    ADD CONSTRAINT mitigation_action_mi_user_id_b61093af_fk_users_cus FOREIGN KEY (user_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3791 (class 2606 OID 114628)
-- Name: ppcn_changelog ppcn_changelog_ppcn_id_59e2c714_fk_ppcn_ppcn_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_changelog
    ADD CONSTRAINT ppcn_changelog_ppcn_id_59e2c714_fk_ppcn_ppcn_id FOREIGN KEY (ppcn_id) REFERENCES public.ppcn_ppcn(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3792 (class 2606 OID 114634)
-- Name: ppcn_changelog ppcn_changelog_user_id_bb4cef6f_fk_users_customuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_changelog
    ADD CONSTRAINT ppcn_changelog_user_id_bb4cef6f_fk_users_customuser_id FOREIGN KEY (user_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3796 (class 2606 OID 114729)
-- Name: ppcn_geiactivitytype ppcn_geiactivitytype_sector_id_c7f8fcfb_fk_ppcn_sector_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_geiactivitytype
    ADD CONSTRAINT ppcn_geiactivitytype_sector_id_c7f8fcfb_fk_ppcn_sector_id FOREIGN KEY (sector_id) REFERENCES public.ppcn_sector(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3795 (class 2606 OID 114690)
-- Name: ppcn_geiactivitytype ppcn_geiactivitytype_sub_sector_id_c1e19ae2_fk_ppcn_subs; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_geiactivitytype
    ADD CONSTRAINT ppcn_geiactivitytype_sub_sector_id_c1e19ae2_fk_ppcn_subs FOREIGN KEY (sub_sector_id) REFERENCES public.ppcn_subsector(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3798 (class 2606 OID 114720)
-- Name: ppcn_geiorganization_gei_activity_types ppcn_geiorganization_geiactivitytype_id_048f50be_fk_ppcn_geia; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_geiorganization_gei_activity_types
    ADD CONSTRAINT ppcn_geiorganization_geiactivitytype_id_048f50be_fk_ppcn_geia FOREIGN KEY (geiactivitytype_id) REFERENCES public.ppcn_geiactivitytype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3797 (class 2606 OID 114715)
-- Name: ppcn_geiorganization_gei_activity_types ppcn_geiorganization_geiorganization_id_82dd23c3_fk_ppcn_geio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_geiorganization_gei_activity_types
    ADD CONSTRAINT ppcn_geiorganization_geiorganization_id_82dd23c3_fk_ppcn_geio FOREIGN KEY (geiorganization_id) REFERENCES public.ppcn_geiorganization(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3776 (class 2606 OID 114645)
-- Name: ppcn_geiorganization ppcn_geiorganization_ovv_id_17530bac_fk_mccr_ovv_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_geiorganization
    ADD CONSTRAINT ppcn_geiorganization_ovv_id_17530bac_fk_mccr_ovv_id FOREIGN KEY (ovv_id) REFERENCES public.mccr_ovv(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3775 (class 2606 OID 114383)
-- Name: ppcn_organization ppcn_organization_contact_id_d94c7c13_fk_mitigatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_organization
    ADD CONSTRAINT ppcn_organization_contact_id_d94c7c13_fk_mitigatio FOREIGN KEY (contact_id) REFERENCES public.mitigation_action_contact(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3794 (class 2606 OID 114618)
-- Name: ppcn_ppcn_comments ppcn_ppcn_comments_comment_id_82a722c9_fk_workflow_comment_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcn_comments
    ADD CONSTRAINT ppcn_ppcn_comments_comment_id_82a722c9_fk_workflow_comment_id FOREIGN KEY (comment_id) REFERENCES public.workflow_comment(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3793 (class 2606 OID 114613)
-- Name: ppcn_ppcn_comments ppcn_ppcn_comments_ppcn_id_3a7defde_fk_ppcn_ppcn_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcn_comments
    ADD CONSTRAINT ppcn_ppcn_comments_ppcn_id_3a7defde_fk_ppcn_ppcn_id FOREIGN KEY (ppcn_id) REFERENCES public.ppcn_ppcn(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3782 (class 2606 OID 114667)
-- Name: ppcn_ppcn ppcn_ppcn_gei_organization_id_debbc419_fk_ppcn_geio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcn
    ADD CONSTRAINT ppcn_ppcn_gei_organization_id_debbc419_fk_ppcn_geio FOREIGN KEY (gei_organization_id) REFERENCES public.ppcn_geiorganization(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3784 (class 2606 OID 114698)
-- Name: ppcn_ppcn ppcn_ppcn_geographic_level_id_c1066abb_fk_ppcn_geog; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcn
    ADD CONSTRAINT ppcn_ppcn_geographic_level_id_c1066abb_fk_ppcn_geog FOREIGN KEY (geographic_level_id) REFERENCES public.ppcn_geographiclevel(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3783 (class 2606 OID 114672)
-- Name: ppcn_ppcn ppcn_ppcn_organization_id_7c48620d_fk_ppcn_organization_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcn
    ADD CONSTRAINT ppcn_ppcn_organization_id_7c48620d_fk_ppcn_organization_id FOREIGN KEY (organization_id) REFERENCES public.ppcn_organization(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3785 (class 2606 OID 114704)
-- Name: ppcn_ppcn ppcn_ppcn_recognition_type_id_1bee6248_fk_ppcn_reco; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcn
    ADD CONSTRAINT ppcn_ppcn_recognition_type_id_1bee6248_fk_ppcn_reco FOREIGN KEY (recognition_type_id) REFERENCES public.ppcn_recognitiontype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3786 (class 2606 OID 114710)
-- Name: ppcn_ppcn ppcn_ppcn_required_level_id_da88f790_fk_ppcn_requiredlevel_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcn
    ADD CONSTRAINT ppcn_ppcn_required_level_id_da88f790_fk_ppcn_requiredlevel_id FOREIGN KEY (required_level_id) REFERENCES public.ppcn_requiredlevel(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3781 (class 2606 OID 114524)
-- Name: ppcn_ppcn ppcn_ppcn_user_id_41508d8e_fk_users_customuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcn
    ADD CONSTRAINT ppcn_ppcn_user_id_41508d8e_fk_users_customuser_id FOREIGN KEY (user_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3780 (class 2606 OID 114529)
-- Name: ppcn_ppcnfile ppcn_ppcnfile_ppcn_form_id_258b17a5_fk_ppcn_ppcn_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcnfile
    ADD CONSTRAINT ppcn_ppcnfile_ppcn_form_id_258b17a5_fk_ppcn_ppcn_id FOREIGN KEY (ppcn_form_id) REFERENCES public.ppcn_ppcn(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3779 (class 2606 OID 114518)
-- Name: ppcn_ppcnfile ppcn_ppcnfile_user_id_de589eff_fk_users_customuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcnfile
    ADD CONSTRAINT ppcn_ppcnfile_user_id_de589eff_fk_users_customuser_id FOREIGN KEY (user_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3789 (class 2606 OID 114583)
-- Name: ppcn_ppcnworkflowstepfile ppcn_ppcnworkflowste_user_id_345e37d6_fk_users_cus; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcnworkflowstepfile
    ADD CONSTRAINT ppcn_ppcnworkflowste_user_id_345e37d6_fk_users_cus FOREIGN KEY (user_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3790 (class 2606 OID 114588)
-- Name: ppcn_ppcnworkflowstepfile ppcn_ppcnworkflowste_workflow_step_id_29a9efd3_fk_ppcn_ppcn; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcnworkflowstepfile
    ADD CONSTRAINT ppcn_ppcnworkflowste_workflow_step_id_29a9efd3_fk_ppcn_ppcn FOREIGN KEY (workflow_step_id) REFERENCES public.ppcn_ppcnworkflowstep(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3787 (class 2606 OID 114571)
-- Name: ppcn_ppcnworkflowstep ppcn_ppcnworkflowstep_ppcn_id_e0c05733_fk_ppcn_ppcn_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcnworkflowstep
    ADD CONSTRAINT ppcn_ppcnworkflowstep_ppcn_id_e0c05733_fk_ppcn_ppcn_id FOREIGN KEY (ppcn_id) REFERENCES public.ppcn_ppcn(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3788 (class 2606 OID 114576)
-- Name: ppcn_ppcnworkflowstep ppcn_ppcnworkflowstep_user_id_33177343_fk_users_customuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcnworkflowstep
    ADD CONSTRAINT ppcn_ppcnworkflowstep_user_id_33177343_fk_users_customuser_id FOREIGN KEY (user_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3777 (class 2606 OID 114550)
-- Name: ppcn_sector ppcn_sector_geographicLevel_id_8827ad6c_fk_ppcn_geog; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_sector
    ADD CONSTRAINT "ppcn_sector_geographicLevel_id_8827ad6c_fk_ppcn_geog" FOREIGN KEY ("geographicLevel_id") REFERENCES public.ppcn_geographiclevel(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3778 (class 2606 OID 114448)
-- Name: ppcn_subsector ppcn_subsector_sector_id_0a8366aa_fk_ppcn_sector_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_subsector
    ADD CONSTRAINT ppcn_subsector_sector_id_0a8366aa_fk_ppcn_sector_id FOREIGN KEY (sector_id) REFERENCES public.ppcn_sector(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3800 (class 2606 OID 114784)
-- Name: report_data_reportfileversion report_data_reportfi_report_file_id_3d0c13cb_fk_report_da; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_data_reportfileversion
    ADD CONSTRAINT report_data_reportfi_report_file_id_3d0c13cb_fk_report_da FOREIGN KEY (report_file_id) REFERENCES public.report_data_reportfile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3802 (class 2606 OID 114811)
-- Name: report_data_reportfilemetadata report_data_reportfi_report_file_id_4f18b601_fk_report_da; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_data_reportfilemetadata
    ADD CONSTRAINT report_data_reportfi_report_file_id_4f18b601_fk_report_da FOREIGN KEY (report_file_id) REFERENCES public.report_data_reportfile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3801 (class 2606 OID 114798)
-- Name: report_data_reportfileversion report_data_reportfi_user_id_c0ab27e1_fk_users_cus; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_data_reportfileversion
    ADD CONSTRAINT report_data_reportfi_user_id_c0ab27e1_fk_users_cus FOREIGN KEY (user_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3799 (class 2606 OID 114791)
-- Name: report_data_reportfile report_data_reportfile_user_id_96d75ab0_fk_users_customuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_data_reportfile
    ADD CONSTRAINT report_data_reportfile_user_id_96d75ab0_fk_users_customuser_id FOREIGN KEY (user_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3729 (class 2606 OID 113565)
-- Name: users_customuser_groups users_customuser_gro_customuser_id_958147bf_fk_users_cus; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_customuser_groups
    ADD CONSTRAINT users_customuser_gro_customuser_id_958147bf_fk_users_cus FOREIGN KEY (customuser_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3730 (class 2606 OID 113570)
-- Name: users_customuser_groups users_customuser_groups_group_id_01390b14_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_customuser_groups
    ADD CONSTRAINT users_customuser_groups_group_id_01390b14_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3731 (class 2606 OID 113579)
-- Name: users_customuser_user_permissions users_customuser_use_customuser_id_5771478b_fk_users_cus; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_customuser_user_permissions
    ADD CONSTRAINT users_customuser_use_customuser_id_5771478b_fk_users_cus FOREIGN KEY (customuser_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3732 (class 2606 OID 113584)
-- Name: users_customuser_user_permissions users_customuser_use_permission_id_baaa2f74_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_customuser_user_permissions
    ADD CONSTRAINT users_customuser_use_permission_id_baaa2f74_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


-- Completed on 2020-02-17 15:53:28 CST

--
-- PostgreSQL database dump complete
--

