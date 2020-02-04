--
-- PostgreSQL database dump
--

-- Dumped from database version 11.1
-- Dumped by pg_dump version 11.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: adminpack; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS adminpack WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION adminpack; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION adminpack IS 'administrative functions for PostgreSQL';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO postgres;

--
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
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO postgres;

--
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
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
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
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
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
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO postgres;

--
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
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
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
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO postgres;

--
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
-- Name: mccr_changelog_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mccr_changelog_id_seq OWNED BY public.mccr_changelog.id;


--
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
-- Name: mccr_mccrregistryovvrelation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mccr_mccrregistryovvrelation_id_seq OWNED BY public.mccr_mccrregistryovvrelation.id;


--
-- Name: mccr_mccrusertype; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mccr_mccrusertype (
    id integer NOT NULL,
    name character varying(100) NOT NULL
);


ALTER TABLE public.mccr_mccrusertype OWNER TO postgres;

--
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
-- Name: mccr_mccrusertype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mccr_mccrusertype_id_seq OWNED BY public.mccr_mccrusertype.id;


--
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
-- Name: mccr_mccrworkflowstep_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mccr_mccrworkflowstep_id_seq OWNED BY public.mccr_mccrworkflowstep.id;


--
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
-- Name: mccr_mccrworkflowstepfile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mccr_mccrworkflowstepfile_id_seq OWNED BY public.mccr_mccrworkflowstepfile.id;


--
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
-- Name: mccr_ovv_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mccr_ovv_id_seq OWNED BY public.mccr_ovv.id;


--
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
-- Name: mitigation_action_changelog_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitigation_action_changelog_id_seq OWNED BY public.mitigation_action_changelog.id;


--
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
-- Name: mitigation_action_contact_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitigation_action_contact_id_seq OWNED BY public.mitigation_action_contact.id;


--
-- Name: mitigation_action_finance; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitigation_action_finance (
    id integer NOT NULL,
    source character varying(100),
    status_id integer NOT NULL
);


ALTER TABLE public.mitigation_action_finance OWNER TO postgres;

--
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
-- Name: mitigation_action_finance_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitigation_action_finance_id_seq OWNED BY public.mitigation_action_finance.id;


--
-- Name: mitigation_action_financesourcetype; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitigation_action_financesourcetype (
    id integer NOT NULL,
    name_en character varying(100) NOT NULL,
    name_es character varying(100) NOT NULL
);


ALTER TABLE public.mitigation_action_financesourcetype OWNER TO postgres;

--
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
-- Name: mitigation_action_financesourcetype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitigation_action_financesourcetype_id_seq OWNED BY public.mitigation_action_financesourcetype.id;


--
-- Name: mitigation_action_financestatus; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitigation_action_financestatus (
    id integer NOT NULL,
    name_es character varying(100) NOT NULL,
    name_en character varying(100) NOT NULL
);


ALTER TABLE public.mitigation_action_financestatus OWNER TO postgres;

--
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
-- Name: mitigation_action_financestatus_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitigation_action_financestatus_id_seq OWNED BY public.mitigation_action_financestatus.id;


--
-- Name: mitigation_action_geographicscale; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitigation_action_geographicscale (
    id integer NOT NULL,
    name_en character varying(100) NOT NULL,
    name_es character varying(100) NOT NULL
);


ALTER TABLE public.mitigation_action_geographicscale OWNER TO postgres;

--
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
-- Name: mitigation_action_geographicscale_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitigation_action_geographicscale_id_seq OWNED BY public.mitigation_action_geographicscale.id;


--
-- Name: mitigation_action_ingeicompliance; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitigation_action_ingeicompliance (
    id integer NOT NULL,
    name_en character varying(100) NOT NULL,
    name_es character varying(100) NOT NULL
);


ALTER TABLE public.mitigation_action_ingeicompliance OWNER TO postgres;

--
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
-- Name: mitigation_action_ingeicompliance_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitigation_action_ingeicompliance_id_seq OWNED BY public.mitigation_action_ingeicompliance.id;


--
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
-- Name: mitigation_action_initiative_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitigation_action_initiative_id_seq OWNED BY public.mitigation_action_initiative.id;


--
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
-- Name: mitigation_action_initiativefinance_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitigation_action_initiativefinance_id_seq OWNED BY public.mitigation_action_initiativefinance.id;


--
-- Name: mitigation_action_initiativetype; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitigation_action_initiativetype (
    id integer NOT NULL,
    initiative_type_es character varying(100) NOT NULL,
    initiative_type_en character varying(100) NOT NULL
);


ALTER TABLE public.mitigation_action_initiativetype OWNER TO postgres;

--
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
-- Name: mitigation_action_initiativetype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitigation_action_initiativetype_id_seq OWNED BY public.mitigation_action_initiativetype.id;


--
-- Name: mitigation_action_institution; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitigation_action_institution (
    id integer NOT NULL,
    name character varying(100) NOT NULL
);


ALTER TABLE public.mitigation_action_institution OWNER TO postgres;

--
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
-- Name: mitigation_action_institution_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitigation_action_institution_id_seq OWNED BY public.mitigation_action_institution.id;


--
-- Name: mitigation_action_location; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitigation_action_location (
    id integer NOT NULL,
    geographical_site character varying(100) NOT NULL,
    is_gis_annexed boolean NOT NULL
);


ALTER TABLE public.mitigation_action_location OWNER TO postgres;

--
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
-- Name: mitigation_action_location_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitigation_action_location_id_seq OWNED BY public.mitigation_action_location.id;


--
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
-- Name: mitigation_action_maworkflowstep_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitigation_action_maworkflowstep_id_seq OWNED BY public.mitigation_action_maworkflowstep.id;


--
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
-- Name: mitigation_action_maworkflowstepfile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitigation_action_maworkflowstepfile_id_seq OWNED BY public.mitigation_action_maworkflowstepfile.id;


--
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
-- Name: mitigation_action_mitigation_comments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitigation_action_mitigation_comments (
    id integer NOT NULL,
    mitigation_id uuid NOT NULL,
    comment_id integer NOT NULL
);


ALTER TABLE public.mitigation_action_mitigation_comments OWNER TO postgres;

--
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
-- Name: mitigation_action_mitigation_comments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitigation_action_mitigation_comments_id_seq OWNED BY public.mitigation_action_mitigation_comments.id;


--
-- Name: mitigation_action_mitigation_ingei_compliances; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitigation_action_mitigation_ingei_compliances (
    id integer NOT NULL,
    mitigation_id uuid NOT NULL,
    ingeicompliance_id integer NOT NULL
);


ALTER TABLE public.mitigation_action_mitigation_ingei_compliances OWNER TO postgres;

--
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
-- Name: mitigation_action_mitigation_ingei_compliances_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitigation_action_mitigation_ingei_compliances_id_seq OWNED BY public.mitigation_action_mitigation_ingei_compliances.id;


--
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
-- Name: mitigation_action_progressindicator_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitigation_action_progressindicator_id_seq OWNED BY public.mitigation_action_progressindicator.id;


--
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
-- Name: mitigation_action_registrationtype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitigation_action_registrationtype_id_seq OWNED BY public.mitigation_action_registrationtype.id;


--
-- Name: mitigation_action_status; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mitigation_action_status (
    id integer NOT NULL,
    status_en character varying(100) NOT NULL,
    status_es character varying(100) NOT NULL
);


ALTER TABLE public.mitigation_action_status OWNER TO postgres;

--
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
-- Name: mitigation_action_status_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mitigation_action_status_id_seq OWNED BY public.mitigation_action_status.id;


--
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
-- Name: ppcn_changelog_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ppcn_changelog_id_seq OWNED BY public.ppcn_changelog.id;


--
-- Name: ppcn_emissionfactor; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ppcn_emissionfactor (
    id integer NOT NULL,
    name character varying(200) NOT NULL
);


ALTER TABLE public.ppcn_emissionfactor OWNER TO postgres;

--
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
-- Name: ppcn_emissionfactor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ppcn_emissionfactor_id_seq OWNED BY public.ppcn_emissionfactor.id;


--
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
-- Name: ppcn_geiactivitytype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ppcn_geiactivitytype_id_seq OWNED BY public.ppcn_geiactivitytype.id;


--
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
-- Name: ppcn_geiorganization_gei_activity_types; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ppcn_geiorganization_gei_activity_types (
    id integer NOT NULL,
    geiorganization_id integer NOT NULL,
    geiactivitytype_id integer NOT NULL
);


ALTER TABLE public.ppcn_geiorganization_gei_activity_types OWNER TO postgres;

--
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
-- Name: ppcn_geiorganization_gei_activity_types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ppcn_geiorganization_gei_activity_types_id_seq OWNED BY public.ppcn_geiorganization_gei_activity_types.id;


--
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
-- Name: ppcn_geiorganization_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ppcn_geiorganization_id_seq OWNED BY public.ppcn_geiorganization.id;


--
-- Name: ppcn_geographiclevel; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ppcn_geographiclevel (
    id integer NOT NULL,
    level_es character varying(200) NOT NULL,
    level_en character varying(200) NOT NULL
);


ALTER TABLE public.ppcn_geographiclevel OWNER TO postgres;

--
-- Name: ppcn_inventorymethodology; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ppcn_inventorymethodology (
    id integer NOT NULL,
    name character varying(200) NOT NULL
);


ALTER TABLE public.ppcn_inventorymethodology OWNER TO postgres;

--
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
-- Name: ppcn_inventorymethodology_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ppcn_inventorymethodology_id_seq OWNED BY public.ppcn_inventorymethodology.id;


--
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
-- Name: ppcn_level_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ppcn_level_id_seq OWNED BY public.ppcn_geographiclevel.id;


--
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
-- Name: ppcn_organization_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ppcn_organization_id_seq OWNED BY public.ppcn_organization.id;


--
-- Name: ppcn_plusaction; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ppcn_plusaction (
    id integer NOT NULL,
    name character varying(200) NOT NULL
);


ALTER TABLE public.ppcn_plusaction OWNER TO postgres;

--
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
-- Name: ppcn_plusaction_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ppcn_plusaction_id_seq OWNED BY public.ppcn_plusaction.id;


--
-- Name: ppcn_potentialglobalwarming; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ppcn_potentialglobalwarming (
    id integer NOT NULL,
    name character varying(200) NOT NULL
);


ALTER TABLE public.ppcn_potentialglobalwarming OWNER TO postgres;

--
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
-- Name: ppcn_potentialglobalwarming_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ppcn_potentialglobalwarming_id_seq OWNED BY public.ppcn_potentialglobalwarming.id;


--
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
-- Name: ppcn_ppcn_comments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ppcn_ppcn_comments (
    id integer NOT NULL,
    ppcn_id integer NOT NULL,
    comment_id integer NOT NULL
);


ALTER TABLE public.ppcn_ppcn_comments OWNER TO postgres;

--
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
-- Name: ppcn_ppcn_comments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ppcn_ppcn_comments_id_seq OWNED BY public.ppcn_ppcn_comments.id;


--
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
-- Name: ppcn_ppcn_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ppcn_ppcn_id_seq OWNED BY public.ppcn_ppcn.id;


--
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
-- Name: ppcn_ppcnfile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ppcn_ppcnfile_id_seq OWNED BY public.ppcn_ppcnfile.id;


--
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
-- Name: ppcn_ppcnworkflowstep_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ppcn_ppcnworkflowstep_id_seq OWNED BY public.ppcn_ppcnworkflowstep.id;


--
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
-- Name: ppcn_ppcnworkflowstepfile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ppcn_ppcnworkflowstepfile_id_seq OWNED BY public.ppcn_ppcnworkflowstepfile.id;


--
-- Name: ppcn_quantifiedgas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ppcn_quantifiedgas (
    id integer NOT NULL,
    name character varying(200) NOT NULL
);


ALTER TABLE public.ppcn_quantifiedgas OWNER TO postgres;

--
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
-- Name: ppcn_quantifiedgas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ppcn_quantifiedgas_id_seq OWNED BY public.ppcn_quantifiedgas.id;


--
-- Name: ppcn_recognitiontype; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ppcn_recognitiontype (
    id integer NOT NULL,
    recognition_type_es character varying(200) NOT NULL,
    recognition_type_en character varying(200) NOT NULL
);


ALTER TABLE public.ppcn_recognitiontype OWNER TO postgres;

--
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
-- Name: ppcn_recognitiontype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ppcn_recognitiontype_id_seq OWNED BY public.ppcn_recognitiontype.id;


--
-- Name: ppcn_requiredlevel; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ppcn_requiredlevel (
    id integer NOT NULL,
    level_type_es character varying(200) NOT NULL,
    level_type_en character varying(200) NOT NULL
);


ALTER TABLE public.ppcn_requiredlevel OWNER TO postgres;

--
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
-- Name: ppcn_requiredlevel_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ppcn_requiredlevel_id_seq OWNED BY public.ppcn_requiredlevel.id;


--
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
-- Name: ppcn_sector_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ppcn_sector_id_seq OWNED BY public.ppcn_sector.id;


--
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
-- Name: ppcn_subsector_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ppcn_subsector_id_seq OWNED BY public.ppcn_subsector.id;


--
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
-- Name: report_data_reportfile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.report_data_reportfile_id_seq OWNED BY public.report_data_reportfile.id;


--
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
-- Name: report_data_reportfilemetadata_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.report_data_reportfilemetadata_id_seq OWNED BY public.report_data_reportfilemetadata.id;


--
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
-- Name: report_data_reportfileversion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.report_data_reportfileversion_id_seq OWNED BY public.report_data_reportfileversion.id;


--
-- Name: users_customgroup; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users_customgroup (
    id integer NOT NULL,
    label character varying(200) NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.users_customgroup OWNER TO postgres;

--
-- Name: users_customgroup_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_customgroup_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_customgroup_id_seq OWNER TO postgres;

--
-- Name: users_customgroup_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_customgroup_id_seq OWNED BY public.users_customgroup.id;


--
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
    is_provider boolean NOT NULL
);


ALTER TABLE public.users_customuser OWNER TO postgres;

--
-- Name: users_customuser_groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users_customuser_groups (
    id integer NOT NULL,
    customuser_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.users_customuser_groups OWNER TO postgres;

--
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
-- Name: users_customuser_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_customuser_groups_id_seq OWNED BY public.users_customuser_groups.id;


--
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
-- Name: users_customuser_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_customuser_id_seq OWNED BY public.users_customuser.id;


--
-- Name: users_customuser_user_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users_customuser_user_permissions (
    id integer NOT NULL,
    customuser_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.users_customuser_user_permissions OWNER TO postgres;

--
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
-- Name: users_customuser_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_customuser_user_permissions_id_seq OWNED BY public.users_customuser_user_permissions.id;


--
-- Name: workflow_comment; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.workflow_comment (
    id integer NOT NULL,
    comment character varying(3000) NOT NULL
);


ALTER TABLE public.workflow_comment OWNER TO postgres;

--
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
-- Name: workflow_comment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.workflow_comment_id_seq OWNED BY public.workflow_comment.id;


--
-- Name: workflow_reviewstatus; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.workflow_reviewstatus (
    id integer NOT NULL,
    status character varying(100) NOT NULL
);


ALTER TABLE public.workflow_reviewstatus OWNER TO postgres;

--
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
-- Name: workflow_reviewstatus_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.workflow_reviewstatus_id_seq OWNED BY public.workflow_reviewstatus.id;


--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Name: mccr_changelog id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_changelog ALTER COLUMN id SET DEFAULT nextval('public.mccr_changelog_id_seq'::regclass);


--
-- Name: mccr_mccrregistryovvrelation id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_mccrregistryovvrelation ALTER COLUMN id SET DEFAULT nextval('public.mccr_mccrregistryovvrelation_id_seq'::regclass);


--
-- Name: mccr_mccrusertype id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_mccrusertype ALTER COLUMN id SET DEFAULT nextval('public.mccr_mccrusertype_id_seq'::regclass);


--
-- Name: mccr_mccrworkflowstep id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_mccrworkflowstep ALTER COLUMN id SET DEFAULT nextval('public.mccr_mccrworkflowstep_id_seq'::regclass);


--
-- Name: mccr_mccrworkflowstepfile id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_mccrworkflowstepfile ALTER COLUMN id SET DEFAULT nextval('public.mccr_mccrworkflowstepfile_id_seq'::regclass);


--
-- Name: mccr_ovv id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_ovv ALTER COLUMN id SET DEFAULT nextval('public.mccr_ovv_id_seq'::regclass);


--
-- Name: mitigation_action_changelog id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_changelog ALTER COLUMN id SET DEFAULT nextval('public.mitigation_action_changelog_id_seq'::regclass);


--
-- Name: mitigation_action_contact id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_contact ALTER COLUMN id SET DEFAULT nextval('public.mitigation_action_contact_id_seq'::regclass);


--
-- Name: mitigation_action_finance id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_finance ALTER COLUMN id SET DEFAULT nextval('public.mitigation_action_finance_id_seq'::regclass);


--
-- Name: mitigation_action_financesourcetype id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_financesourcetype ALTER COLUMN id SET DEFAULT nextval('public.mitigation_action_financesourcetype_id_seq'::regclass);


--
-- Name: mitigation_action_financestatus id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_financestatus ALTER COLUMN id SET DEFAULT nextval('public.mitigation_action_financestatus_id_seq'::regclass);


--
-- Name: mitigation_action_geographicscale id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_geographicscale ALTER COLUMN id SET DEFAULT nextval('public.mitigation_action_geographicscale_id_seq'::regclass);


--
-- Name: mitigation_action_ingeicompliance id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_ingeicompliance ALTER COLUMN id SET DEFAULT nextval('public.mitigation_action_ingeicompliance_id_seq'::regclass);


--
-- Name: mitigation_action_initiative id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_initiative ALTER COLUMN id SET DEFAULT nextval('public.mitigation_action_initiative_id_seq'::regclass);


--
-- Name: mitigation_action_initiativefinance id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_initiativefinance ALTER COLUMN id SET DEFAULT nextval('public.mitigation_action_initiativefinance_id_seq'::regclass);


--
-- Name: mitigation_action_initiativetype id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_initiativetype ALTER COLUMN id SET DEFAULT nextval('public.mitigation_action_initiativetype_id_seq'::regclass);


--
-- Name: mitigation_action_institution id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_institution ALTER COLUMN id SET DEFAULT nextval('public.mitigation_action_institution_id_seq'::regclass);


--
-- Name: mitigation_action_location id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_location ALTER COLUMN id SET DEFAULT nextval('public.mitigation_action_location_id_seq'::regclass);


--
-- Name: mitigation_action_maworkflowstep id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_maworkflowstep ALTER COLUMN id SET DEFAULT nextval('public.mitigation_action_maworkflowstep_id_seq'::regclass);


--
-- Name: mitigation_action_maworkflowstepfile id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_maworkflowstepfile ALTER COLUMN id SET DEFAULT nextval('public.mitigation_action_maworkflowstepfile_id_seq'::regclass);


--
-- Name: mitigation_action_mitigation_comments id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_mitigation_comments ALTER COLUMN id SET DEFAULT nextval('public.mitigation_action_mitigation_comments_id_seq'::regclass);


--
-- Name: mitigation_action_mitigation_ingei_compliances id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_mitigation_ingei_compliances ALTER COLUMN id SET DEFAULT nextval('public.mitigation_action_mitigation_ingei_compliances_id_seq'::regclass);


--
-- Name: mitigation_action_progressindicator id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_progressindicator ALTER COLUMN id SET DEFAULT nextval('public.mitigation_action_progressindicator_id_seq'::regclass);


--
-- Name: mitigation_action_registrationtype id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_registrationtype ALTER COLUMN id SET DEFAULT nextval('public.mitigation_action_registrationtype_id_seq'::regclass);


--
-- Name: mitigation_action_status id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_status ALTER COLUMN id SET DEFAULT nextval('public.mitigation_action_status_id_seq'::regclass);


--
-- Name: ppcn_changelog id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_changelog ALTER COLUMN id SET DEFAULT nextval('public.ppcn_changelog_id_seq'::regclass);


--
-- Name: ppcn_emissionfactor id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_emissionfactor ALTER COLUMN id SET DEFAULT nextval('public.ppcn_emissionfactor_id_seq'::regclass);


--
-- Name: ppcn_geiactivitytype id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_geiactivitytype ALTER COLUMN id SET DEFAULT nextval('public.ppcn_geiactivitytype_id_seq'::regclass);


--
-- Name: ppcn_geiorganization id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_geiorganization ALTER COLUMN id SET DEFAULT nextval('public.ppcn_geiorganization_id_seq'::regclass);


--
-- Name: ppcn_geiorganization_gei_activity_types id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_geiorganization_gei_activity_types ALTER COLUMN id SET DEFAULT nextval('public.ppcn_geiorganization_gei_activity_types_id_seq'::regclass);


--
-- Name: ppcn_geographiclevel id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_geographiclevel ALTER COLUMN id SET DEFAULT nextval('public.ppcn_level_id_seq'::regclass);


--
-- Name: ppcn_inventorymethodology id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_inventorymethodology ALTER COLUMN id SET DEFAULT nextval('public.ppcn_inventorymethodology_id_seq'::regclass);


--
-- Name: ppcn_organization id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_organization ALTER COLUMN id SET DEFAULT nextval('public.ppcn_organization_id_seq'::regclass);


--
-- Name: ppcn_plusaction id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_plusaction ALTER COLUMN id SET DEFAULT nextval('public.ppcn_plusaction_id_seq'::regclass);


--
-- Name: ppcn_potentialglobalwarming id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_potentialglobalwarming ALTER COLUMN id SET DEFAULT nextval('public.ppcn_potentialglobalwarming_id_seq'::regclass);


--
-- Name: ppcn_ppcn id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcn ALTER COLUMN id SET DEFAULT nextval('public.ppcn_ppcn_id_seq'::regclass);


--
-- Name: ppcn_ppcn_comments id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcn_comments ALTER COLUMN id SET DEFAULT nextval('public.ppcn_ppcn_comments_id_seq'::regclass);


--
-- Name: ppcn_ppcnfile id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcnfile ALTER COLUMN id SET DEFAULT nextval('public.ppcn_ppcnfile_id_seq'::regclass);


--
-- Name: ppcn_ppcnworkflowstep id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcnworkflowstep ALTER COLUMN id SET DEFAULT nextval('public.ppcn_ppcnworkflowstep_id_seq'::regclass);


--
-- Name: ppcn_ppcnworkflowstepfile id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcnworkflowstepfile ALTER COLUMN id SET DEFAULT nextval('public.ppcn_ppcnworkflowstepfile_id_seq'::regclass);


--
-- Name: ppcn_quantifiedgas id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_quantifiedgas ALTER COLUMN id SET DEFAULT nextval('public.ppcn_quantifiedgas_id_seq'::regclass);


--
-- Name: ppcn_recognitiontype id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_recognitiontype ALTER COLUMN id SET DEFAULT nextval('public.ppcn_recognitiontype_id_seq'::regclass);


--
-- Name: ppcn_requiredlevel id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_requiredlevel ALTER COLUMN id SET DEFAULT nextval('public.ppcn_requiredlevel_id_seq'::regclass);


--
-- Name: ppcn_sector id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_sector ALTER COLUMN id SET DEFAULT nextval('public.ppcn_sector_id_seq'::regclass);


--
-- Name: ppcn_subsector id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_subsector ALTER COLUMN id SET DEFAULT nextval('public.ppcn_subsector_id_seq'::regclass);


--
-- Name: report_data_reportfile id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_data_reportfile ALTER COLUMN id SET DEFAULT nextval('public.report_data_reportfile_id_seq'::regclass);


--
-- Name: report_data_reportfilemetadata id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_data_reportfilemetadata ALTER COLUMN id SET DEFAULT nextval('public.report_data_reportfilemetadata_id_seq'::regclass);


--
-- Name: report_data_reportfileversion id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_data_reportfileversion ALTER COLUMN id SET DEFAULT nextval('public.report_data_reportfileversion_id_seq'::regclass);


--
-- Name: users_customgroup id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_customgroup ALTER COLUMN id SET DEFAULT nextval('public.users_customgroup_id_seq'::regclass);


--
-- Name: users_customuser id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_customuser ALTER COLUMN id SET DEFAULT nextval('public.users_customuser_id_seq'::regclass);


--
-- Name: users_customuser_groups id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_customuser_groups ALTER COLUMN id SET DEFAULT nextval('public.users_customuser_groups_id_seq'::regclass);


--
-- Name: users_customuser_user_permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_customuser_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.users_customuser_user_permissions_id_seq'::regclass);


--
-- Name: workflow_comment id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflow_comment ALTER COLUMN id SET DEFAULT nextval('public.workflow_comment_id_seq'::regclass);


--
-- Name: workflow_reviewstatus id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflow_reviewstatus ALTER COLUMN id SET DEFAULT nextval('public.workflow_reviewstatus_id_seq'::regclass);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group (id, name) FROM stdin;
12	general_administrator
13	registry_operator
14	mitigation_action_provider
15	ppcn_provider
16	mccr_provider
17	pgai
18	validation_organization
19	government_representative
20	data_analyst
21	non_governmental_data_provider
22	inventory_compiler
23	dcc_ppcn_responsible
24	dcc_mitigation_action_responsible
25	dcc_mccr_responsible
26	dcc_executive_secretary
27	dcc_executive_committee
28	dcc_general
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
8	25	1
9	16	4
10	27	5
11	26	2
12	14	6
13	24	7
14	26	8
15	23	10
16	23	11
17	15	12
18	26	9
\.


--
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
13	Can add log entry	4	add_logentry
14	Can change log entry	4	change_logentry
15	Can delete log entry	4	delete_logentry
16	Can add permission	5	add_permission
17	Can change permission	5	change_permission
18	Can delete permission	5	delete_permission
19	Can add group	6	add_group
20	Can change group	6	change_group
21	Can delete group	6	delete_group
22	Can add content type	7	add_contenttype
23	Can change content type	7	change_contenttype
24	Can delete content type	7	delete_contenttype
25	Can add session	8	add_session
26	Can change session	8	change_session
27	Can delete session	8	delete_session
28	Can add ReportFile	9	add_reportfile
29	Can change ReportFile	9	change_reportfile
30	Can delete ReportFile	9	delete_reportfile
31	Can add ReportFileVersion	10	add_reportfileversion
32	Can change ReportFileVersion	10	change_reportfileversion
33	Can delete ReportFileVersion	10	delete_reportfileversion
34	Can add ReportFileMetadata	11	add_reportfilemetadata
35	Can change ReportFileMetadata	11	change_reportfilemetadata
36	Can delete ReportFileMetadata	11	delete_reportfilemetadata
37	Can add Contact	12	add_contact
38	Can change Contact	12	change_contact
39	Can delete Contact	12	delete_contact
40	Can add Finance	13	add_finance
41	Can change Finance	13	change_finance
42	Can delete Finance	13	delete_finance
43	Can add GeographicScale	14	add_geographicscale
44	Can change GeographicScale	14	change_geographicscale
45	Can delete GeographicScale	14	delete_geographicscale
46	Can add IngeiCompliance	15	add_ingeicompliance
47	Can change IngeiCompliance	15	change_ingeicompliance
48	Can delete IngeiCompliance	15	delete_ingeicompliance
49	Can add Institution	16	add_institution
50	Can change Institution	16	change_institution
51	Can delete Institution	16	delete_institution
52	Can add Location	17	add_location
53	Can change Location	17	change_location
54	Can delete Location	17	delete_location
55	Can add ProgressIndicator	18	add_progressindicator
56	Can change ProgressIndicator	18	change_progressindicator
57	Can delete ProgressIndicator	18	delete_progressindicator
58	Can add RegistrationType	19	add_registrationtype
59	Can change RegistrationType	19	change_registrationtype
60	Can delete RegistrationType	19	delete_registrationtype
61	Can add Status	20	add_status
62	Can change Status	20	change_status
63	Can delete Status	20	delete_status
64	Can add MitigationAccess	2	add_mitigation
65	Can change MitigationAccess	2	change_mitigation
66	Can delete MitigationAccess	2	delete_mitigation
67	Can add ChangeLog	21	add_changelog
68	Can change ChangeLog	21	change_changelog
69	Can delete ChangeLog	21	delete_changelog
70	Can add FinanceSourceType	22	add_financesourcetype
71	Can change FinanceSourceType	22	change_financesourcetype
72	Can delete FinanceSourceType	22	delete_financesourcetype
73	Can add Workflow Step	23	add_maworkflowstep
74	Can change Workflow Step	23	change_maworkflowstep
75	Can delete Workflow Step	23	delete_maworkflowstep
76	Can add Workflow Step File	24	add_maworkflowstepfile
77	Can change Workflow Step File	24	change_maworkflowstepfile
78	Can delete Workflow Step File	24	delete_maworkflowstepfile
79	Can add FinanceStatus	25	add_financestatus
80	Can change FinanceStatus	25	change_financestatus
81	Can delete FinanceStatus	25	delete_financestatus
82	Can add Initiative	26	add_initiative
83	Can change Initiative	26	change_initiative
84	Can delete Initiative	26	delete_initiative
85	Can add InitiativeFinance	27	add_initiativefinance
86	Can change InitiativeFinance	27	change_initiativefinance
87	Can delete InitiativeFinance	27	delete_initiativefinance
88	Can add InitiativeType	28	add_initiativetype
89	Can change InitiativeType	28	change_initiativetype
90	Can delete InitiativeType	28	delete_initiativetype
91	Can add Comment	29	add_comment
92	Can change Comment	29	change_comment
93	Can delete Comment	29	delete_comment
94	Can add ReviewStatus	30	add_reviewstatus
95	Can change ReviewStatus	30	change_reviewstatus
96	Can delete ReviewStatus	30	delete_reviewstatus
97	Can add MCCRFile	31	add_mccrfile
98	Can change MCCRFile	31	change_mccrfile
99	Can delete MCCRFile	31	delete_mccrfile
100	Can add MCCRRegistry	1	add_mccrregistry
101	Can change MCCRRegistry	1	change_mccrregistry
102	Can delete MCCRRegistry	1	delete_mccrregistry
103	Can add MCCRUserType	32	add_mccrusertype
104	Can change MCCRUserType	32	change_mccrusertype
105	Can delete MCCRUserType	32	delete_mccrusertype
106	Can add MCCR OVV Relation	33	add_mccrregistryovvrelation
107	Can change MCCR OVV Relation	33	change_mccrregistryovvrelation
108	Can delete MCCR OVV Relation	33	delete_mccrregistryovvrelation
109	Can add Organismo Validador Verifador	34	add_ovv
110	Can change Organismo Validador Verifador	34	change_ovv
111	Can delete Organismo Validador Verifador	34	delete_ovv
112	Can add ChangeLog	35	add_changelog
113	Can change ChangeLog	35	change_changelog
114	Can delete ChangeLog	35	delete_changelog
115	Can add Workflow Step	36	add_mccrworkflowstep
116	Can change Workflow Step	36	change_mccrworkflowstep
117	Can delete Workflow Step	36	delete_mccrworkflowstep
118	Can add Workflow Step File	37	add_mccrworkflowstepfile
119	Can change Workflow Step File	37	change_mccrworkflowstepfile
120	Can delete Workflow Step File	37	delete_mccrworkflowstepfile
121	Can add EmissionFactor	38	add_emissionfactor
122	Can change EmissionFactor	38	change_emissionfactor
123	Can delete EmissionFactor	38	delete_emissionfactor
124	Can add InventoryMethodology	39	add_inventorymethodology
125	Can change InventoryMethodology	39	change_inventorymethodology
126	Can delete InventoryMethodology	39	delete_inventorymethodology
127	Can add Organization	40	add_organization
128	Can change Organization	40	change_organization
129	Can delete Organization	40	delete_organization
130	Can add PlusAction	41	add_plusaction
131	Can change PlusAction	41	change_plusaction
132	Can delete PlusAction	41	delete_plusaction
133	Can add PotentialGlobalWarming	42	add_potentialglobalwarming
134	Can change PotentialGlobalWarming	42	change_potentialglobalwarming
135	Can delete PotentialGlobalWarming	42	delete_potentialglobalwarming
136	Can add QuantifiedGas	43	add_quantifiedgas
137	Can change QuantifiedGas	43	change_quantifiedgas
138	Can delete QuantifiedGas	43	delete_quantifiedgas
139	Can add GeiOrganization	44	add_geiorganization
140	Can change GeiOrganization	44	change_geiorganization
141	Can delete GeiOrganization	44	delete_geiorganization
142	Can add RecognitionType	45	add_recognitiontype
143	Can change RecognitionType	45	change_recognitiontype
144	Can delete RecognitionType	45	delete_recognitiontype
145	Can add RequiredLevel	46	add_requiredlevel
146	Can change RequiredLevel	46	change_requiredlevel
147	Can delete RequiredLevel	46	delete_requiredlevel
148	Can add Sector	47	add_sector
149	Can change Sector	47	change_sector
150	Can delete Sector	47	delete_sector
151	Can add SubSector	48	add_subsector
152	Can change SubSector	48	change_subsector
153	Can delete SubSector	48	delete_subsector
154	Can add GeographicLevel	49	add_geographiclevel
155	Can change GeographicLevel	49	change_geographiclevel
156	Can delete GeographicLevel	49	delete_geographiclevel
157	Can add ppcn file	50	add_ppcnfile
158	Can change ppcn file	50	change_ppcnfile
159	Can delete ppcn file	50	delete_ppcnfile
160	Can add PPCN	3	add_ppcn
161	Can change PPCN	3	change_ppcn
162	Can delete PPCN	3	delete_ppcn
163	Can add Workflow Step	51	add_ppcnworkflowstep
164	Can change Workflow Step	51	change_ppcnworkflowstep
165	Can delete Workflow Step	51	delete_ppcnworkflowstep
166	Can add Workflow Step File	52	add_ppcnworkflowstepfile
167	Can change Workflow Step File	52	change_ppcnworkflowstepfile
168	Can delete Workflow Step File	52	delete_ppcnworkflowstepfile
169	Can add ChangeLog	53	add_changelog
170	Can change ChangeLog	53	change_changelog
171	Can delete ChangeLog	53	delete_changelog
172	Can add gei activity type	54	add_geiactivitytype
173	Can change gei activity type	54	change_geiactivitytype
174	Can delete gei activity type	54	delete_geiactivitytype
175	Can add user	55	add_customuser
176	Can change user	55	change_customuser
177	Can delete user	55	delete_customuser
178	Can add CustomGroup	56	add_customgroup
179	Can change CustomGroup	56	change_customgroup
180	Can delete CustomGroup	56	delete_customgroup
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	mccr	mccrregistry
2	mitigation_action	mitigation
3	ppcn	ppcn
4	admin	logentry
5	auth	permission
6	auth	group
7	contenttypes	contenttype
8	sessions	session
9	report_data	reportfile
10	report_data	reportfileversion
11	report_data	reportfilemetadata
12	mitigation_action	contact
13	mitigation_action	finance
14	mitigation_action	geographicscale
15	mitigation_action	ingeicompliance
16	mitigation_action	institution
17	mitigation_action	location
18	mitigation_action	progressindicator
19	mitigation_action	registrationtype
20	mitigation_action	status
21	mitigation_action	changelog
22	mitigation_action	financesourcetype
23	mitigation_action	maworkflowstep
24	mitigation_action	maworkflowstepfile
25	mitigation_action	financestatus
26	mitigation_action	initiative
27	mitigation_action	initiativefinance
28	mitigation_action	initiativetype
29	workflow	comment
30	workflow	reviewstatus
31	mccr	mccrfile
32	mccr	mccrusertype
33	mccr	mccrregistryovvrelation
34	mccr	ovv
35	mccr	changelog
36	mccr	mccrworkflowstep
37	mccr	mccrworkflowstepfile
38	ppcn	emissionfactor
39	ppcn	inventorymethodology
40	ppcn	organization
41	ppcn	plusaction
42	ppcn	potentialglobalwarming
43	ppcn	quantifiedgas
44	ppcn	geiorganization
45	ppcn	recognitiontype
46	ppcn	requiredlevel
47	ppcn	sector
48	ppcn	subsector
49	ppcn	geographiclevel
50	ppcn	ppcnfile
51	ppcn	ppcnworkflowstep
52	ppcn	ppcnworkflowstepfile
53	ppcn	changelog
54	ppcn	geiactivitytype
55	users	customuser
56	users	customgroup
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2019-08-26 23:15:29.912212-06
2	contenttypes	0002_remove_content_type_name	2019-08-26 23:15:29.921263-06
3	auth	0001_initial	2019-08-26 23:15:29.953274-06
4	auth	0002_alter_permission_name_max_length	2019-08-26 23:15:29.96185-06
5	auth	0003_alter_user_email_max_length	2019-08-26 23:15:29.968751-06
6	auth	0004_alter_user_username_opts	2019-08-26 23:15:29.975551-06
7	auth	0005_alter_user_last_login_null	2019-08-26 23:15:29.981914-06
8	auth	0006_require_contenttypes_0002	2019-08-26 23:15:29.983581-06
9	auth	0007_alter_validators_add_error_messages	2019-08-26 23:15:29.991609-06
10	auth	0008_alter_user_username_max_length	2019-08-26 23:15:29.998139-06
11	users	0001_initial	2019-08-26 23:15:30.052633-06
12	admin	0001_initial	2019-08-26 23:15:30.077138-06
13	admin	0002_logentry_remove_auto_add	2019-08-26 23:15:30.091284-06
14	general	0001_initial	2019-08-26 23:15:30.093547-06
15	general	0002_auto_20180414_1639	2019-08-26 23:15:30.110567-06
16	mitigation_action	0001_initial	2019-08-26 23:15:30.237728-06
17	mitigation_action	0002_auto_20180406_0303	2019-08-26 23:15:30.271165-06
18	mitigation_action	0003_auto_20180410_0140	2019-08-26 23:15:30.296884-06
19	mccr	0001_initial	2019-08-26 23:15:30.383184-06
20	mccr	0002_mccrregistry_status	2019-08-26 23:15:30.402832-06
21	mccr	0003_auto_20180504_0350	2019-08-26 23:15:30.457587-06
22	mccr	0004_initial_user_types	2019-08-26 23:15:30.479209-06
23	mccr	0005_auto_20180514_0527	2019-08-26 23:15:30.508691-06
24	mccr	0006_auto_20180726_0106	2019-08-26 23:15:30.546478-06
25	mccr	0007_auto_20180803_1658	2019-08-26 23:15:30.650318-06
26	mccr	0008_auto_20181003_1705	2019-08-26 23:15:30.795502-06
27	mccr	0009_addPermissions	2019-08-26 23:15:30.841009-06
28	mccr	0010_auto_20190801_2139	2019-08-26 23:15:30.867335-06
29	workflow	0001_initial	2019-08-26 23:15:30.878593-06
30	mitigation_action	0004_progressindicator_name	2019-08-26 23:15:30.887659-06
31	mitigation_action	0005_auto_20180418_0529	2019-08-26 23:15:30.949428-06
32	mitigation_action	0006_auto_20180501_2219	2019-08-26 23:15:31.16207-06
33	mitigation_action	0007_auto_20180503_0256	2019-08-26 23:15:31.185863-06
34	mitigation_action	0006_mitigation_question_ucc	2019-08-26 23:15:31.209467-06
35	mitigation_action	0008_merge_20180505_0137	2019-08-26 23:15:31.211529-06
36	mitigation_action	0009_auto_20180509_1347	2019-08-26 23:15:31.236142-06
37	mitigation_action	0010_auto_20180512_2026	2019-08-26 23:15:31.302513-06
38	mitigation_action	0011_auto_20180513_1828	2019-08-26 23:15:31.336575-06
39	mitigation_action	0012_mitigation_question_ovv	2019-08-26 23:15:31.361588-06
40	mitigation_action	0013_auto_20180526_0052	2019-08-26 23:15:31.426153-06
41	mitigation_action	0014_auto_20180604_2002	2019-08-26 23:15:31.536113-06
42	mitigation_action	0015_auto_20180722_2021	2019-08-26 23:15:31.592124-06
43	mitigation_action	0016_registrationtype_type_key	2019-08-26 23:15:31.680834-06
44	mitigation_action	0015_harmonizationingei	2019-08-26 23:15:31.713066-06
45	mitigation_action	0016_merge_20180726_1803	2019-08-26 23:15:31.714731-06
46	mitigation_action	0017_auto_20180726_1804	2019-08-26 23:15:31.8745-06
47	mitigation_action	0018_auto_20180726_1805	2019-08-26 23:15:31.897822-06
48	mitigation_action	0019_auto_20180803_1658	2019-08-26 23:15:31.930277-06
49	mitigation_action	0020_auto_20180817_2248	2019-08-26 23:15:32.006028-06
50	mitigation_action	0021_auto_20180819_0423	2019-08-26 23:15:32.228769-06
51	mitigation_action	0022_auto_20180919_1556	2019-08-26 23:15:32.407706-06
52	mitigation_action	0023_auto_20181029_1753	2019-08-26 23:15:33.501451-06
53	mitigation_action	0024_auto_20181029_2112	2019-08-26 23:15:33.517233-06
54	mitigation_action	0023_auto_20181030_0214	2019-08-26 23:15:33.552392-06
55	mitigation_action	0025_merge_20181030_1721	2019-08-26 23:15:33.563054-06
56	mitigation_action	0026_auto_20181204_1636	2019-08-26 23:15:33.707496-06
57	mitigation_action	0027_addPermissions	2019-08-26 23:15:33.742626-06
58	mitigation_action	0028_auto_20190318_2142	2019-08-26 23:15:33.778443-06
59	workflow	0002_auto_20180503_0303	2019-08-26 23:15:33.816021-06
60	workflow	0003_auto_20180513_1755	2019-08-26 23:15:33.831597-06
61	ppcn	0001_initial	2019-08-26 23:15:33.943847-06
62	ppcn	0002_auto_20180730_2101	2019-08-26 23:15:34.186218-06
63	ppcn	0003_auto_20180730_0140	2019-08-26 23:15:34.26596-06
64	ppcn	0004_auto_20180801_2004	2019-08-26 23:15:34.431903-06
65	ppcn	0005_auto_20180816_1713	2019-08-26 23:15:34.474833-06
66	ppcn	0006_auto_20180820_2149	2019-08-26 23:15:34.560651-06
67	ppcn	0007_auto_20180821_1607	2019-08-26 23:15:34.602721-06
68	ppcn	0008_auto_20180822_1938	2019-08-26 23:15:34.674393-06
69	ppcn	0009_auto_20180827_1549	2019-08-26 23:15:34.757941-06
70	ppcn	0010_auto_20180831_1950	2019-08-26 23:15:34.792193-06
71	ppcn	0011_ppcnworkflowstep_ppcnworkflowstepfile	2019-08-26 23:15:34.931385-06
72	ppcn	0012_auto_20180911_1654	2019-08-26 23:15:35.136117-06
73	ppcn	0013_auto_20181116_1950	2019-08-26 23:15:35.186248-06
74	ppcn	0014_auto_20181125_1702	2019-08-26 23:15:35.301103-06
75	ppcn	0015_auto_20181210_0448	2019-08-26 23:15:35.994388-06
76	ppcn	0016_auto_20190304_1628	2019-08-26 23:15:36.028683-06
77	ppcn	0017_addPermissions	2019-08-26 23:15:36.158978-06
78	ppcn	0018_auto_20190318_2142	2019-08-26 23:15:36.191478-06
79	ppcn	0019_auto_20190718_2141	2019-08-26 23:15:36.253537-06
80	report_data	0001_initial	2019-08-26 23:15:36.262147-06
81	report_data	0002_auto_20180307_0345	2019-08-26 23:15:36.272632-06
82	report_data	0003_auto_20180307_0406	2019-08-26 23:15:36.277609-06
83	report_data	0004_auto_20180314_2352	2019-08-26 23:15:36.297749-06
84	report_data	0005_auto_20180315_0014	2019-08-26 23:15:36.31281-06
85	report_data	0006_reportfileversion_file	2019-08-26 23:15:36.323064-06
86	report_data	0007_auto_20180320_0346	2019-08-26 23:15:36.335994-06
87	report_data	0008_auto_20180320_0427	2019-08-26 23:15:36.352871-06
88	report_data	0004_reportfile_user	2019-08-26 23:15:36.409156-06
89	report_data	0009_merge_20180322_0012	2019-08-26 23:15:36.411249-06
90	report_data	0010_reportfileversion_user	2019-08-26 23:15:36.466848-06
91	report_data	0011_auto_20180322_0207	2019-08-26 23:15:36.505126-06
92	report_data	0012_auto_20180517_0247	2019-08-26 23:15:36.539723-06
93	report_data	0013_reportfilemetadata	2019-08-26 23:15:36.596209-06
94	sessions	0001_initial	2019-08-26 23:15:36.606334-06
95	users	0002_customgroup	2019-08-26 23:15:36.768566-06
96	users	0003_addPermissions	2019-08-26 23:15:36.895742-06
97	users	0004_addPermissions	2019-08-26 23:15:36.954674-06
98	users	0005_auto_20190322_2126	2019-08-26 23:15:37.091764-06
99	users	0006_addPermissions	2019-08-26 23:15:37.529686-06
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
\.


--
-- Data for Name: mccr_changelog; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mccr_changelog (id, date, previous_status, current_status, mccr_id, user_id) FROM stdin;
\.


--
-- Data for Name: mccr_mccrfile; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mccr_mccrfile (id, file, mccr_id, user_id, created, updated) FROM stdin;
\.


--
-- Data for Name: mccr_mccrregistry; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mccr_mccrregistry (id, user_type_id, mitigation_id, user_id, status, created, updated, fsm_state) FROM stdin;
\.


--
-- Data for Name: mccr_mccrregistryovvrelation; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mccr_mccrregistryovvrelation (id, status, created, updated, mccr_id, ovv_id) FROM stdin;
\.


--
-- Data for Name: mccr_mccrusertype; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mccr_mccrusertype (id, name) FROM stdin;
1	Registrator
2	Reviewer
\.


--
-- Data for Name: mccr_mccrworkflowstep; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mccr_mccrworkflowstep (id, name, entry_name, status, created, updated, mccr_id, user_id) FROM stdin;
\.


--
-- Data for Name: mccr_mccrworkflowstepfile; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mccr_mccrworkflowstepfile (id, created, updated, file, user_id, workflow_step_id) FROM stdin;
\.


--
-- Data for Name: mccr_ovv; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mccr_ovv (id, name, email, phone, created, updated) FROM stdin;
1	Test backend OVV	sinamec@grupoincocr.com	(506) 9309-2345	2019-08-26 23:15:30.642479-06	2019-08-26 23:15:30.6425-06
\.


--
-- Data for Name: mitigation_action_changelog; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mitigation_action_changelog (id, date, current_status, mitigation_action_id, previous_status, user_id) FROM stdin;
\.


--
-- Data for Name: mitigation_action_contact; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mitigation_action_contact (id, full_name, job_title, email, phone) FROM stdin;
\.


--
-- Data for Name: mitigation_action_finance; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mitigation_action_finance (id, source, status_id) FROM stdin;
\.


--
-- Data for Name: mitigation_action_financesourcetype; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mitigation_action_financesourcetype (id, name_en, name_es) FROM stdin;
3	Public Budget	Presupuesto público 
4	Private Finance	Financiamiento privado
5	Cooperation Project	Proyecto de cooperación
6	Loan	Préstamo
\.


--
-- Data for Name: mitigation_action_financestatus; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mitigation_action_financestatus (id, name_es, name_en) FROM stdin;
1	Por obtener	To obtain
2	Asegurado	Insured
\.


--
-- Data for Name: mitigation_action_geographicscale; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mitigation_action_geographicscale (id, name_en, name_es) FROM stdin;
4	National	Nacional
5	Regional	Regional
6	Local	Local
\.


--
-- Data for Name: mitigation_action_ingeicompliance; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mitigation_action_ingeicompliance (id, name_en, name_es) FROM stdin;
4	Agriculture, forestry and other land uses	Agricultura, silvicultura y otros usos de la tierra (AFOLU)
5	Industrial processes and use of products	Procesos industriales y uso de productos
6	Residue	Residuos
\.


--
-- Data for Name: mitigation_action_initiative; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mitigation_action_initiative (id, name, objective, description, goal, entity_responsible, budget, contact_id, finance_id, initiative_type_id, status_id) FROM stdin;
\.


--
-- Data for Name: mitigation_action_initiativefinance; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mitigation_action_initiativefinance (id, finance_source_type_id, status_id, source) FROM stdin;
\.


--
-- Data for Name: mitigation_action_initiativetype; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mitigation_action_initiativetype (id, initiative_type_es, initiative_type_en) FROM stdin;
1	Proyecto	Proyect
2	Política	Law
3	Meta	Goal
\.


--
-- Data for Name: mitigation_action_institution; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mitigation_action_institution (id, name) FROM stdin;
1	MINAE
2	SINAMECC
\.


--
-- Data for Name: mitigation_action_location; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mitigation_action_location (id, geographical_site, is_gis_annexed) FROM stdin;
\.


--
-- Data for Name: mitigation_action_maworkflowstep; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mitigation_action_maworkflowstep (id, name, entry_name, status, created, updated, mitigation_action_id, user_id) FROM stdin;
\.


--
-- Data for Name: mitigation_action_maworkflowstepfile; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mitigation_action_maworkflowstepfile (id, file, created, updated, user_id, workflow_step_id) FROM stdin;
\.


--
-- Data for Name: mitigation_action_mitigation; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mitigation_action_mitigation (id, strategy_name, name, purpose, start_date, end_date, gas_inventory, emissions_source, carbon_sinks, impact_plan, impact, calculation_methodology, is_international, international_participation, created, updated, contact_id, finance_id, geographic_scale_id, institution_id, location_id, progress_indicator_id, registration_type_id, status_id, user_id, review_count, fsm_state, initiative_id) FROM stdin;
\.


--
-- Data for Name: mitigation_action_mitigation_comments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mitigation_action_mitigation_comments (id, mitigation_id, comment_id) FROM stdin;
\.


--
-- Data for Name: mitigation_action_mitigation_ingei_compliances; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mitigation_action_mitigation_ingei_compliances (id, mitigation_id, ingeicompliance_id) FROM stdin;
\.


--
-- Data for Name: mitigation_action_progressindicator; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mitigation_action_progressindicator (id, type, unit, start_date, name) FROM stdin;
\.


--
-- Data for Name: mitigation_action_registrationtype; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mitigation_action_registrationtype (id, type_en, type_es, type_key) FROM stdin;
5	Registration for the first time	Inscripción por primera vez	new
6	Update of mitigation action information	Actualización de información de acción de mitigación	update
\.


--
-- Data for Name: mitigation_action_status; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mitigation_action_status (id, status_en, status_es) FROM stdin;
4	Planning	Planeación
5	Implementation	Implementación
6	Completed	Finalizada
\.


--
-- Data for Name: ppcn_changelog; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ppcn_changelog (id, date, previous_status, current_status, ppcn_id, user_id) FROM stdin;
\.


--
-- Data for Name: ppcn_emissionfactor; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ppcn_emissionfactor (id, name) FROM stdin;
\.


--
-- Data for Name: ppcn_geiactivitytype; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ppcn_geiactivitytype (id, activity_type, sector_id, sub_sector_id) FROM stdin;
\.


--
-- Data for Name: ppcn_geiorganization; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ppcn_geiorganization (id, ovv_id, emission_ovv_date, report_year, base_year) FROM stdin;
\.


--
-- Data for Name: ppcn_geiorganization_gei_activity_types; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ppcn_geiorganization_gei_activity_types (id, geiorganization_id, geiactivitytype_id) FROM stdin;
\.


--
-- Data for Name: ppcn_geographiclevel; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ppcn_geographiclevel (id, level_es, level_en) FROM stdin;
1	Cantonal	Cantonal
2	Organizacional	Organizational
\.


--
-- Data for Name: ppcn_inventorymethodology; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ppcn_inventorymethodology (id, name) FROM stdin;
\.


--
-- Data for Name: ppcn_organization; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ppcn_organization (id, name, representative_name, postal_code, fax, address, ciiu, contact_id, phone_organization) FROM stdin;
\.


--
-- Data for Name: ppcn_plusaction; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ppcn_plusaction (id, name) FROM stdin;
\.


--
-- Data for Name: ppcn_potentialglobalwarming; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ppcn_potentialglobalwarming (id, name) FROM stdin;
\.


--
-- Data for Name: ppcn_ppcn; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ppcn_ppcn (id, organization_id, created, updated, user_id, fsm_state, review_count, gei_organization_id, geographic_level_id, recognition_type_id, required_level_id) FROM stdin;
\.


--
-- Data for Name: ppcn_ppcn_comments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ppcn_ppcn_comments (id, ppcn_id, comment_id) FROM stdin;
\.


--
-- Data for Name: ppcn_ppcnfile; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ppcn_ppcnfile (id, file, created, updated, ppcn_form_id, user_id) FROM stdin;
\.


--
-- Data for Name: ppcn_ppcnworkflowstep; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ppcn_ppcnworkflowstep (id, name, entry_name, status, created, updated, ppcn_id, user_id) FROM stdin;
\.


--
-- Data for Name: ppcn_ppcnworkflowstepfile; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ppcn_ppcnworkflowstepfile (id, file, created, updated, user_id, workflow_step_id) FROM stdin;
\.


--
-- Data for Name: ppcn_quantifiedgas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ppcn_quantifiedgas (id, name) FROM stdin;
\.


--
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
-- Data for Name: ppcn_requiredlevel; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ppcn_requiredlevel (id, level_type_es, level_type_en) FROM stdin;
1	Solicitud inicial de incorporación al PPCN	Initial Request to incorporate with PPCN
2	Mantenimiento en el PPCN	Maintenance to PPCN
3	Renovación en el PPCN	Renovation in the PPCN
\.


--
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
-- Data for Name: report_data_reportfile; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.report_data_reportfile (id, name, created, updated, user_id) FROM stdin;
\.


--
-- Data for Name: report_data_reportfilemetadata; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.report_data_reportfilemetadata (id, name, value, report_file_id) FROM stdin;
\.


--
-- Data for Name: report_data_reportfileversion; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.report_data_reportfileversion (id, active, version, file, report_file_id, user_id) FROM stdin;
\.


--
-- Data for Name: users_customgroup; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users_customgroup (id, label, group_id) FROM stdin;
17	General Administrator	12
18	Registry Operator	13
19	Mitigation Action Provider	14
20	PPCN Provider	15
21	MCCR Provider	16
22	PGAI	17
23	Validation Organization	18
24	Government Representative	19
25	Data Analyst	20
26	Non-governmental Data Provider	21
27	Inventory Compiler	22
28	DCC PPCN Responsible	23
29	DCC Mitigation Action Responsible	24
30	DCC MCCR Responsible	25
31	DCC Executive Secretary	26
32	DCC Executive Committe	27
33	General Group DCC	28
\.


--
-- Data for Name: users_customuser; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users_customuser (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, is_administrador_dcc, is_provider) FROM stdin;
1	pbkdf2_sha256$36000$v7prYV05RYgX$jQ0KRqDkXLj+T6yr+Ad2EgcugCAGAYGTMG+a3beEXqQ=	\N	t	admin_sinamecc	Administrador	Sinamecc	sinamec@grupoincocr.com	t	t	2019-08-26 23:15:37.30209-06	t	t
2	pbkdf2_sha256$36000$vZG6icGq0SoW$3RHH/06iJ8FPLxU0XKsC9kpwkJ6zBgTXIZieP1qH+YM=	\N	f	dcc_general	DCC	Sinamecc	izcar@grupoincocr.com	t	t	2019-08-26 23:15:37.304807-06	t	f
3	pbkdf2_sha256$36000$5knnUddtVmWZ$XOV1LrHadlH26uejJmojEEV3hXp36nFfWkIQoLoTBgY=	\N	f	provider_general	Provider	Sinamecc	carlos@grupoincocr.com	t	t	2019-08-26 23:15:37.307113-06	f	t
\.


--
-- Data for Name: users_customuser_groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users_customuser_groups (id, customuser_id, group_id) FROM stdin;
1	1	12
2	2	12
3	1	13
4	2	13
5	1	14
6	3	14
7	1	15
8	3	15
9	1	16
10	3	16
11	1	17
12	2	17
13	1	18
14	2	18
15	1	19
16	2	19
17	1	20
18	2	20
19	1	21
20	2	21
21	1	22
22	2	22
23	1	23
24	2	23
25	1	24
26	2	24
27	1	25
28	2	25
29	1	26
30	2	26
31	1	27
32	2	27
33	1	28
34	2	28
\.


--
-- Data for Name: users_customuser_user_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users_customuser_user_permissions (id, customuser_id, permission_id) FROM stdin;
\.


--
-- Data for Name: workflow_comment; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.workflow_comment (id, comment) FROM stdin;
\.


--
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
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 28, true);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 18, true);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 180, true);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 56, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 99, true);


--
-- Name: mccr_changelog_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mccr_changelog_id_seq', 1, false);


--
-- Name: mccr_mccrregistryovvrelation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mccr_mccrregistryovvrelation_id_seq', 1, false);


--
-- Name: mccr_mccrusertype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mccr_mccrusertype_id_seq', 2, true);


--
-- Name: mccr_mccrworkflowstep_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mccr_mccrworkflowstep_id_seq', 1, false);


--
-- Name: mccr_mccrworkflowstepfile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mccr_mccrworkflowstepfile_id_seq', 1, false);


--
-- Name: mccr_ovv_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mccr_ovv_id_seq', 1, true);


--
-- Name: mitigation_action_changelog_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mitigation_action_changelog_id_seq', 1, false);


--
-- Name: mitigation_action_contact_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mitigation_action_contact_id_seq', 1, false);


--
-- Name: mitigation_action_finance_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mitigation_action_finance_id_seq', 2, true);


--
-- Name: mitigation_action_financesourcetype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mitigation_action_financesourcetype_id_seq', 6, true);


--
-- Name: mitigation_action_financestatus_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mitigation_action_financestatus_id_seq', 2, true);


--
-- Name: mitigation_action_geographicscale_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mitigation_action_geographicscale_id_seq', 6, true);


--
-- Name: mitigation_action_ingeicompliance_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mitigation_action_ingeicompliance_id_seq', 6, true);


--
-- Name: mitigation_action_initiative_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mitigation_action_initiative_id_seq', 1, false);


--
-- Name: mitigation_action_initiativefinance_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mitigation_action_initiativefinance_id_seq', 1, false);


--
-- Name: mitigation_action_initiativetype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mitigation_action_initiativetype_id_seq', 3, true);


--
-- Name: mitigation_action_institution_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mitigation_action_institution_id_seq', 2, true);


--
-- Name: mitigation_action_location_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mitigation_action_location_id_seq', 1, false);


--
-- Name: mitigation_action_maworkflowstep_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mitigation_action_maworkflowstep_id_seq', 1, false);


--
-- Name: mitigation_action_maworkflowstepfile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mitigation_action_maworkflowstepfile_id_seq', 1, false);


--
-- Name: mitigation_action_mitigation_comments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mitigation_action_mitigation_comments_id_seq', 1, false);


--
-- Name: mitigation_action_mitigation_ingei_compliances_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mitigation_action_mitigation_ingei_compliances_id_seq', 1, false);


--
-- Name: mitigation_action_progressindicator_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mitigation_action_progressindicator_id_seq', 1, false);


--
-- Name: mitigation_action_registrationtype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mitigation_action_registrationtype_id_seq', 6, true);


--
-- Name: mitigation_action_status_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mitigation_action_status_id_seq', 6, true);


--
-- Name: ppcn_changelog_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ppcn_changelog_id_seq', 1, false);


--
-- Name: ppcn_emissionfactor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ppcn_emissionfactor_id_seq', 1, false);


--
-- Name: ppcn_geiactivitytype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ppcn_geiactivitytype_id_seq', 1, false);


--
-- Name: ppcn_geiorganization_gei_activity_types_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ppcn_geiorganization_gei_activity_types_id_seq', 1, false);


--
-- Name: ppcn_geiorganization_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ppcn_geiorganization_id_seq', 1, false);


--
-- Name: ppcn_inventorymethodology_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ppcn_inventorymethodology_id_seq', 1, false);


--
-- Name: ppcn_level_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ppcn_level_id_seq', 2, true);


--
-- Name: ppcn_organization_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ppcn_organization_id_seq', 1, false);


--
-- Name: ppcn_plusaction_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ppcn_plusaction_id_seq', 1, false);


--
-- Name: ppcn_potentialglobalwarming_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ppcn_potentialglobalwarming_id_seq', 1, false);


--
-- Name: ppcn_ppcn_comments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ppcn_ppcn_comments_id_seq', 1, false);


--
-- Name: ppcn_ppcn_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ppcn_ppcn_id_seq', 1, false);


--
-- Name: ppcn_ppcnfile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ppcn_ppcnfile_id_seq', 1, false);


--
-- Name: ppcn_ppcnworkflowstep_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ppcn_ppcnworkflowstep_id_seq', 1, false);


--
-- Name: ppcn_ppcnworkflowstepfile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ppcn_ppcnworkflowstepfile_id_seq', 1, false);


--
-- Name: ppcn_quantifiedgas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ppcn_quantifiedgas_id_seq', 1, false);


--
-- Name: ppcn_recognitiontype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ppcn_recognitiontype_id_seq', 5, true);


--
-- Name: ppcn_requiredlevel_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ppcn_requiredlevel_id_seq', 3, true);


--
-- Name: ppcn_sector_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ppcn_sector_id_seq', 9, true);


--
-- Name: ppcn_subsector_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ppcn_subsector_id_seq', 40, true);


--
-- Name: report_data_reportfile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.report_data_reportfile_id_seq', 1, false);


--
-- Name: report_data_reportfilemetadata_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.report_data_reportfilemetadata_id_seq', 1, false);


--
-- Name: report_data_reportfileversion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.report_data_reportfileversion_id_seq', 1, false);


--
-- Name: users_customgroup_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_customgroup_id_seq', 33, true);


--
-- Name: users_customuser_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_customuser_groups_id_seq', 34, true);


--
-- Name: users_customuser_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_customuser_id_seq', 3, true);


--
-- Name: users_customuser_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_customuser_user_permissions_id_seq', 1, false);


--
-- Name: workflow_comment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.workflow_comment_id_seq', 1, false);


--
-- Name: workflow_reviewstatus_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.workflow_reviewstatus_id_seq', 5, true);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: mccr_changelog mccr_changelog_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_changelog
    ADD CONSTRAINT mccr_changelog_pkey PRIMARY KEY (id);


--
-- Name: mccr_mccrfile mccr_mccrfile_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_mccrfile
    ADD CONSTRAINT mccr_mccrfile_pkey PRIMARY KEY (id);


--
-- Name: mccr_mccrregistry mccr_mccrregistry_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_mccrregistry
    ADD CONSTRAINT mccr_mccrregistry_pkey PRIMARY KEY (id);


--
-- Name: mccr_mccrregistryovvrelation mccr_mccrregistryovvrelation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_mccrregistryovvrelation
    ADD CONSTRAINT mccr_mccrregistryovvrelation_pkey PRIMARY KEY (id);


--
-- Name: mccr_mccrusertype mccr_mccrusertype_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_mccrusertype
    ADD CONSTRAINT mccr_mccrusertype_pkey PRIMARY KEY (id);


--
-- Name: mccr_mccrworkflowstep mccr_mccrworkflowstep_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_mccrworkflowstep
    ADD CONSTRAINT mccr_mccrworkflowstep_pkey PRIMARY KEY (id);


--
-- Name: mccr_mccrworkflowstepfile mccr_mccrworkflowstepfile_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_mccrworkflowstepfile
    ADD CONSTRAINT mccr_mccrworkflowstepfile_pkey PRIMARY KEY (id);


--
-- Name: mccr_ovv mccr_ovv_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_ovv
    ADD CONSTRAINT mccr_ovv_pkey PRIMARY KEY (id);


--
-- Name: mitigation_action_changelog mitigation_action_changelog_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_changelog
    ADD CONSTRAINT mitigation_action_changelog_pkey PRIMARY KEY (id);


--
-- Name: mitigation_action_contact mitigation_action_contact_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_contact
    ADD CONSTRAINT mitigation_action_contact_pkey PRIMARY KEY (id);


--
-- Name: mitigation_action_finance mitigation_action_finance_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_finance
    ADD CONSTRAINT mitigation_action_finance_pkey PRIMARY KEY (id);


--
-- Name: mitigation_action_financesourcetype mitigation_action_financesourcetype_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_financesourcetype
    ADD CONSTRAINT mitigation_action_financesourcetype_pkey PRIMARY KEY (id);


--
-- Name: mitigation_action_financestatus mitigation_action_financestatus_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_financestatus
    ADD CONSTRAINT mitigation_action_financestatus_pkey PRIMARY KEY (id);


--
-- Name: mitigation_action_geographicscale mitigation_action_geographicscale_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_geographicscale
    ADD CONSTRAINT mitigation_action_geographicscale_pkey PRIMARY KEY (id);


--
-- Name: mitigation_action_ingeicompliance mitigation_action_ingeicompliance_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_ingeicompliance
    ADD CONSTRAINT mitigation_action_ingeicompliance_pkey PRIMARY KEY (id);


--
-- Name: mitigation_action_initiative mitigation_action_initiative_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_initiative
    ADD CONSTRAINT mitigation_action_initiative_pkey PRIMARY KEY (id);


--
-- Name: mitigation_action_initiativefinance mitigation_action_initiativefinance_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_initiativefinance
    ADD CONSTRAINT mitigation_action_initiativefinance_pkey PRIMARY KEY (id);


--
-- Name: mitigation_action_initiativetype mitigation_action_initiativetype_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_initiativetype
    ADD CONSTRAINT mitigation_action_initiativetype_pkey PRIMARY KEY (id);


--
-- Name: mitigation_action_institution mitigation_action_institution_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_institution
    ADD CONSTRAINT mitigation_action_institution_pkey PRIMARY KEY (id);


--
-- Name: mitigation_action_location mitigation_action_location_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_location
    ADD CONSTRAINT mitigation_action_location_pkey PRIMARY KEY (id);


--
-- Name: mitigation_action_maworkflowstep mitigation_action_maworkflowstep_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_maworkflowstep
    ADD CONSTRAINT mitigation_action_maworkflowstep_pkey PRIMARY KEY (id);


--
-- Name: mitigation_action_maworkflowstepfile mitigation_action_maworkflowstepfile_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_maworkflowstepfile
    ADD CONSTRAINT mitigation_action_maworkflowstepfile_pkey PRIMARY KEY (id);


--
-- Name: mitigation_action_mitigation_comments mitigation_action_mitiga_mitigation_id_comment_id_e062b2f1_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_mitigation_comments
    ADD CONSTRAINT mitigation_action_mitiga_mitigation_id_comment_id_e062b2f1_uniq UNIQUE (mitigation_id, comment_id);


--
-- Name: mitigation_action_mitigation_ingei_compliances mitigation_action_mitiga_mitigation_id_ingeicompl_f69646fe_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_mitigation_ingei_compliances
    ADD CONSTRAINT mitigation_action_mitiga_mitigation_id_ingeicompl_f69646fe_uniq UNIQUE (mitigation_id, ingeicompliance_id);


--
-- Name: mitigation_action_mitigation_comments mitigation_action_mitigation_comments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_mitigation_comments
    ADD CONSTRAINT mitigation_action_mitigation_comments_pkey PRIMARY KEY (id);


--
-- Name: mitigation_action_mitigation_ingei_compliances mitigation_action_mitigation_ingei_compliances_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_mitigation_ingei_compliances
    ADD CONSTRAINT mitigation_action_mitigation_ingei_compliances_pkey PRIMARY KEY (id);


--
-- Name: mitigation_action_mitigation mitigation_action_mitigationaction_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_mitigation
    ADD CONSTRAINT mitigation_action_mitigationaction_pkey PRIMARY KEY (id);


--
-- Name: mitigation_action_progressindicator mitigation_action_progressindicator_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_progressindicator
    ADD CONSTRAINT mitigation_action_progressindicator_pkey PRIMARY KEY (id);


--
-- Name: mitigation_action_registrationtype mitigation_action_registrationtype_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_registrationtype
    ADD CONSTRAINT mitigation_action_registrationtype_pkey PRIMARY KEY (id);


--
-- Name: mitigation_action_status mitigation_action_status_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_status
    ADD CONSTRAINT mitigation_action_status_pkey PRIMARY KEY (id);


--
-- Name: ppcn_changelog ppcn_changelog_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_changelog
    ADD CONSTRAINT ppcn_changelog_pkey PRIMARY KEY (id);


--
-- Name: ppcn_emissionfactor ppcn_emissionfactor_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_emissionfactor
    ADD CONSTRAINT ppcn_emissionfactor_pkey PRIMARY KEY (id);


--
-- Name: ppcn_geiactivitytype ppcn_geiactivitytype_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_geiactivitytype
    ADD CONSTRAINT ppcn_geiactivitytype_pkey PRIMARY KEY (id);


--
-- Name: ppcn_geiorganization_gei_activity_types ppcn_geiorganization_gei_activity_types_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_geiorganization_gei_activity_types
    ADD CONSTRAINT ppcn_geiorganization_gei_activity_types_pkey PRIMARY KEY (id);


--
-- Name: ppcn_geiorganization_gei_activity_types ppcn_geiorganization_gei_geiorganization_id_geiac_43936059_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_geiorganization_gei_activity_types
    ADD CONSTRAINT ppcn_geiorganization_gei_geiorganization_id_geiac_43936059_uniq UNIQUE (geiorganization_id, geiactivitytype_id);


--
-- Name: ppcn_geiorganization ppcn_geiorganization_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_geiorganization
    ADD CONSTRAINT ppcn_geiorganization_pkey PRIMARY KEY (id);


--
-- Name: ppcn_inventorymethodology ppcn_inventorymethodology_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_inventorymethodology
    ADD CONSTRAINT ppcn_inventorymethodology_pkey PRIMARY KEY (id);


--
-- Name: ppcn_geographiclevel ppcn_level_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_geographiclevel
    ADD CONSTRAINT ppcn_level_pkey PRIMARY KEY (id);


--
-- Name: ppcn_organization ppcn_organization_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_organization
    ADD CONSTRAINT ppcn_organization_pkey PRIMARY KEY (id);


--
-- Name: ppcn_plusaction ppcn_plusaction_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_plusaction
    ADD CONSTRAINT ppcn_plusaction_pkey PRIMARY KEY (id);


--
-- Name: ppcn_potentialglobalwarming ppcn_potentialglobalwarming_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_potentialglobalwarming
    ADD CONSTRAINT ppcn_potentialglobalwarming_pkey PRIMARY KEY (id);


--
-- Name: ppcn_ppcn_comments ppcn_ppcn_comments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcn_comments
    ADD CONSTRAINT ppcn_ppcn_comments_pkey PRIMARY KEY (id);


--
-- Name: ppcn_ppcn_comments ppcn_ppcn_comments_ppcn_id_comment_id_ccb4e106_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcn_comments
    ADD CONSTRAINT ppcn_ppcn_comments_ppcn_id_comment_id_ccb4e106_uniq UNIQUE (ppcn_id, comment_id);


--
-- Name: ppcn_ppcn ppcn_ppcn_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcn
    ADD CONSTRAINT ppcn_ppcn_pkey PRIMARY KEY (id);


--
-- Name: ppcn_ppcnfile ppcn_ppcnfile_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcnfile
    ADD CONSTRAINT ppcn_ppcnfile_pkey PRIMARY KEY (id);


--
-- Name: ppcn_ppcnworkflowstep ppcn_ppcnworkflowstep_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcnworkflowstep
    ADD CONSTRAINT ppcn_ppcnworkflowstep_pkey PRIMARY KEY (id);


--
-- Name: ppcn_ppcnworkflowstepfile ppcn_ppcnworkflowstepfile_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcnworkflowstepfile
    ADD CONSTRAINT ppcn_ppcnworkflowstepfile_pkey PRIMARY KEY (id);


--
-- Name: ppcn_quantifiedgas ppcn_quantifiedgas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_quantifiedgas
    ADD CONSTRAINT ppcn_quantifiedgas_pkey PRIMARY KEY (id);


--
-- Name: ppcn_recognitiontype ppcn_recognitiontype_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_recognitiontype
    ADD CONSTRAINT ppcn_recognitiontype_pkey PRIMARY KEY (id);


--
-- Name: ppcn_requiredlevel ppcn_requiredlevel_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_requiredlevel
    ADD CONSTRAINT ppcn_requiredlevel_pkey PRIMARY KEY (id);


--
-- Name: ppcn_sector ppcn_sector_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_sector
    ADD CONSTRAINT ppcn_sector_pkey PRIMARY KEY (id);


--
-- Name: ppcn_subsector ppcn_subsector_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_subsector
    ADD CONSTRAINT ppcn_subsector_pkey PRIMARY KEY (id);


--
-- Name: report_data_reportfile report_data_reportfile_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_data_reportfile
    ADD CONSTRAINT report_data_reportfile_pkey PRIMARY KEY (id);


--
-- Name: report_data_reportfilemetadata report_data_reportfilemetadata_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_data_reportfilemetadata
    ADD CONSTRAINT report_data_reportfilemetadata_pkey PRIMARY KEY (id);


--
-- Name: report_data_reportfileversion report_data_reportfileversion_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_data_reportfileversion
    ADD CONSTRAINT report_data_reportfileversion_pkey PRIMARY KEY (id);


--
-- Name: report_data_reportfileversion report_data_reportfileversion_version_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_data_reportfileversion
    ADD CONSTRAINT report_data_reportfileversion_version_key UNIQUE (version);


--
-- Name: users_customgroup users_customgroup_group_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_customgroup
    ADD CONSTRAINT users_customgroup_group_id_key UNIQUE (group_id);


--
-- Name: users_customgroup users_customgroup_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_customgroup
    ADD CONSTRAINT users_customgroup_pkey PRIMARY KEY (id);


--
-- Name: users_customuser_groups users_customuser_groups_customuser_id_group_id_76b619e3_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_customuser_groups
    ADD CONSTRAINT users_customuser_groups_customuser_id_group_id_76b619e3_uniq UNIQUE (customuser_id, group_id);


--
-- Name: users_customuser_groups users_customuser_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_customuser_groups
    ADD CONSTRAINT users_customuser_groups_pkey PRIMARY KEY (id);


--
-- Name: users_customuser users_customuser_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_customuser
    ADD CONSTRAINT users_customuser_pkey PRIMARY KEY (id);


--
-- Name: users_customuser_user_permissions users_customuser_user_pe_customuser_id_permission_7a7debf6_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_customuser_user_permissions
    ADD CONSTRAINT users_customuser_user_pe_customuser_id_permission_7a7debf6_uniq UNIQUE (customuser_id, permission_id);


--
-- Name: users_customuser_user_permissions users_customuser_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_customuser_user_permissions
    ADD CONSTRAINT users_customuser_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: users_customuser users_customuser_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_customuser
    ADD CONSTRAINT users_customuser_username_key UNIQUE (username);


--
-- Name: workflow_comment workflow_comment_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflow_comment
    ADD CONSTRAINT workflow_comment_pkey PRIMARY KEY (id);


--
-- Name: workflow_reviewstatus workflow_reviewstatus_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflow_reviewstatus
    ADD CONSTRAINT workflow_reviewstatus_pkey PRIMARY KEY (id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: mccr_changelog_ppcn_id_adeaca0d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mccr_changelog_ppcn_id_adeaca0d ON public.mccr_changelog USING btree (mccr_id);


--
-- Name: mccr_changelog_user_id_4678b3eb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mccr_changelog_user_id_4678b3eb ON public.mccr_changelog USING btree (user_id);


--
-- Name: mccr_mccrfile_mccr_id_08c07172; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mccr_mccrfile_mccr_id_08c07172 ON public.mccr_mccrfile USING btree (mccr_id);


--
-- Name: mccr_mccrfile_user_id_517351bd; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mccr_mccrfile_user_id_517351bd ON public.mccr_mccrfile USING btree (user_id);


--
-- Name: mccr_mccrregistry_mitigation_id_42e7601c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mccr_mccrregistry_mitigation_id_42e7601c ON public.mccr_mccrregistry USING btree (mitigation_id);


--
-- Name: mccr_mccrregistry_user_id_8ce12972; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mccr_mccrregistry_user_id_8ce12972 ON public.mccr_mccrregistry USING btree (user_id);


--
-- Name: mccr_mccrregistry_user_type_id_36dc1127; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mccr_mccrregistry_user_type_id_36dc1127 ON public.mccr_mccrregistry USING btree (user_type_id);


--
-- Name: mccr_mccrregistryovvrelation_mccr_id_6c978edf; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mccr_mccrregistryovvrelation_mccr_id_6c978edf ON public.mccr_mccrregistryovvrelation USING btree (mccr_id);


--
-- Name: mccr_mccrregistryovvrelation_ovv_id_25f87d39; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mccr_mccrregistryovvrelation_ovv_id_25f87d39 ON public.mccr_mccrregistryovvrelation USING btree (ovv_id);


--
-- Name: mccr_mccrworkflowstep_mccr_id_00c7d236; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mccr_mccrworkflowstep_mccr_id_00c7d236 ON public.mccr_mccrworkflowstep USING btree (mccr_id);


--
-- Name: mccr_mccrworkflowstep_user_id_c48a5841; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mccr_mccrworkflowstep_user_id_c48a5841 ON public.mccr_mccrworkflowstep USING btree (user_id);


--
-- Name: mccr_mccrworkflowstepfile_user_id_0c2c21c3; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mccr_mccrworkflowstepfile_user_id_0c2c21c3 ON public.mccr_mccrworkflowstepfile USING btree (user_id);


--
-- Name: mccr_mccrworkflowstepfile_workflow_step_id_a4e95d21; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mccr_mccrworkflowstepfile_workflow_step_id_a4e95d21 ON public.mccr_mccrworkflowstepfile USING btree (workflow_step_id);


--
-- Name: mitigation_action_changelog_mitigation_action_id_a4801a1b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_changelog_mitigation_action_id_a4801a1b ON public.mitigation_action_changelog USING btree (mitigation_action_id);


--
-- Name: mitigation_action_changelog_user_id_c0f7d427; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_changelog_user_id_c0f7d427 ON public.mitigation_action_changelog USING btree (user_id);


--
-- Name: mitigation_action_finance_status_id_a940da2d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_finance_status_id_a940da2d ON public.mitigation_action_finance USING btree (status_id);


--
-- Name: mitigation_action_initiati_finance_source_type_id_1d97a554; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_initiati_finance_source_type_id_1d97a554 ON public.mitigation_action_initiativefinance USING btree (finance_source_type_id);


--
-- Name: mitigation_action_initiative_contact_id_b4f438da; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_initiative_contact_id_b4f438da ON public.mitigation_action_initiative USING btree (contact_id);


--
-- Name: mitigation_action_initiative_finance_id_605f54db; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_initiative_finance_id_605f54db ON public.mitigation_action_initiative USING btree (finance_id);


--
-- Name: mitigation_action_initiative_initiative_type_id_54661d5b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_initiative_initiative_type_id_54661d5b ON public.mitigation_action_initiative USING btree (initiative_type_id);


--
-- Name: mitigation_action_initiative_status_id_44027193; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_initiative_status_id_44027193 ON public.mitigation_action_initiative USING btree (status_id);


--
-- Name: mitigation_action_initiativefinance_status_id_fa3cebf4; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_initiativefinance_status_id_fa3cebf4 ON public.mitigation_action_initiativefinance USING btree (status_id);


--
-- Name: mitigation_action_maworkflowstep_mitigation_action_id_e3bbba48; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_maworkflowstep_mitigation_action_id_e3bbba48 ON public.mitigation_action_maworkflowstep USING btree (mitigation_action_id);


--
-- Name: mitigation_action_maworkflowstep_user_id_f1494fbc; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_maworkflowstep_user_id_f1494fbc ON public.mitigation_action_maworkflowstep USING btree (user_id);


--
-- Name: mitigation_action_maworkflowstepfile_user_id_67fc87e2; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_maworkflowstepfile_user_id_67fc87e2 ON public.mitigation_action_maworkflowstepfile USING btree (user_id);


--
-- Name: mitigation_action_maworkflowstepfile_workflow_step_id_0cba48d8; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_maworkflowstepfile_workflow_step_id_0cba48d8 ON public.mitigation_action_maworkflowstepfile USING btree (workflow_step_id);


--
-- Name: mitigation_action_mitigati_ingeicompliance_id_3a83b0d9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_mitigati_ingeicompliance_id_3a83b0d9 ON public.mitigation_action_mitigation_ingei_compliances USING btree (ingeicompliance_id);


--
-- Name: mitigation_action_mitigati_mitigation_id_f4c4460f; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_mitigati_mitigation_id_f4c4460f ON public.mitigation_action_mitigation_ingei_compliances USING btree (mitigation_id);


--
-- Name: mitigation_action_mitigati_progress_indicator_id_a7e7a5fb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_mitigati_progress_indicator_id_a7e7a5fb ON public.mitigation_action_mitigation USING btree (progress_indicator_id);


--
-- Name: mitigation_action_mitigati_registration_type_id_794241da; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_mitigati_registration_type_id_794241da ON public.mitigation_action_mitigation USING btree (registration_type_id);


--
-- Name: mitigation_action_mitigation_comments_comment_id_d430a9a4; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_mitigation_comments_comment_id_d430a9a4 ON public.mitigation_action_mitigation_comments USING btree (comment_id);


--
-- Name: mitigation_action_mitigation_comments_mitigation_id_98b68b5f; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_mitigation_comments_mitigation_id_98b68b5f ON public.mitigation_action_mitigation_comments USING btree (mitigation_id);


--
-- Name: mitigation_action_mitigation_initiative_id_342cab00; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_mitigation_initiative_id_342cab00 ON public.mitigation_action_mitigation USING btree (initiative_id);


--
-- Name: mitigation_action_mitigationaction_contact_id_ad72c37c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_mitigationaction_contact_id_ad72c37c ON public.mitigation_action_mitigation USING btree (contact_id);


--
-- Name: mitigation_action_mitigationaction_finance_id_955ea6ac; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_mitigationaction_finance_id_955ea6ac ON public.mitigation_action_mitigation USING btree (finance_id);


--
-- Name: mitigation_action_mitigationaction_geographic_scale_id_a33fc61e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_mitigationaction_geographic_scale_id_a33fc61e ON public.mitigation_action_mitigation USING btree (geographic_scale_id);


--
-- Name: mitigation_action_mitigationaction_institution_id_b189af89; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_mitigationaction_institution_id_b189af89 ON public.mitigation_action_mitigation USING btree (institution_id);


--
-- Name: mitigation_action_mitigationaction_location_id_2770ab5d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_mitigationaction_location_id_2770ab5d ON public.mitigation_action_mitigation USING btree (location_id);


--
-- Name: mitigation_action_mitigationaction_status_id_4a0647fc; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_mitigationaction_status_id_4a0647fc ON public.mitigation_action_mitigation USING btree (status_id);


--
-- Name: mitigation_action_mitigationaction_user_id_b61093af; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mitigation_action_mitigationaction_user_id_b61093af ON public.mitigation_action_mitigation USING btree (user_id);


--
-- Name: ppcn_changelog_ppcn_id_59e2c714; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ppcn_changelog_ppcn_id_59e2c714 ON public.ppcn_changelog USING btree (ppcn_id);


--
-- Name: ppcn_changelog_user_id_bb4cef6f; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ppcn_changelog_user_id_bb4cef6f ON public.ppcn_changelog USING btree (user_id);


--
-- Name: ppcn_geiactivitytype_sector_id_c7f8fcfb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ppcn_geiactivitytype_sector_id_c7f8fcfb ON public.ppcn_geiactivitytype USING btree (sector_id);


--
-- Name: ppcn_geiactivitytype_sub_sector_id_c1e19ae2; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ppcn_geiactivitytype_sub_sector_id_c1e19ae2 ON public.ppcn_geiactivitytype USING btree (sub_sector_id);


--
-- Name: ppcn_geiorganization_gei_a_geiactivitytype_id_048f50be; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ppcn_geiorganization_gei_a_geiactivitytype_id_048f50be ON public.ppcn_geiorganization_gei_activity_types USING btree (geiactivitytype_id);


--
-- Name: ppcn_geiorganization_gei_a_geiorganization_id_82dd23c3; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ppcn_geiorganization_gei_a_geiorganization_id_82dd23c3 ON public.ppcn_geiorganization_gei_activity_types USING btree (geiorganization_id);


--
-- Name: ppcn_geiorganization_ovv_id_17530bac; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ppcn_geiorganization_ovv_id_17530bac ON public.ppcn_geiorganization USING btree (ovv_id);


--
-- Name: ppcn_organization_contact_id_d94c7c13; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ppcn_organization_contact_id_d94c7c13 ON public.ppcn_organization USING btree (contact_id);


--
-- Name: ppcn_ppcn_comments_comment_id_82a722c9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ppcn_ppcn_comments_comment_id_82a722c9 ON public.ppcn_ppcn_comments USING btree (comment_id);


--
-- Name: ppcn_ppcn_comments_ppcn_id_3a7defde; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ppcn_ppcn_comments_ppcn_id_3a7defde ON public.ppcn_ppcn_comments USING btree (ppcn_id);


--
-- Name: ppcn_ppcn_gei_organization_id_debbc419; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ppcn_ppcn_gei_organization_id_debbc419 ON public.ppcn_ppcn USING btree (gei_organization_id);


--
-- Name: ppcn_ppcn_geographic_level_id_c1066abb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ppcn_ppcn_geographic_level_id_c1066abb ON public.ppcn_ppcn USING btree (geographic_level_id);


--
-- Name: ppcn_ppcn_organization_id_7c48620d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ppcn_ppcn_organization_id_7c48620d ON public.ppcn_ppcn USING btree (organization_id);


--
-- Name: ppcn_ppcn_recognition_type_id_1bee6248; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ppcn_ppcn_recognition_type_id_1bee6248 ON public.ppcn_ppcn USING btree (recognition_type_id);


--
-- Name: ppcn_ppcn_required_level_id_da88f790; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ppcn_ppcn_required_level_id_da88f790 ON public.ppcn_ppcn USING btree (required_level_id);


--
-- Name: ppcn_ppcn_user_id_41508d8e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ppcn_ppcn_user_id_41508d8e ON public.ppcn_ppcn USING btree (user_id);


--
-- Name: ppcn_ppcnfile_ppcn_form_id_258b17a5; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ppcn_ppcnfile_ppcn_form_id_258b17a5 ON public.ppcn_ppcnfile USING btree (ppcn_form_id);


--
-- Name: ppcn_ppcnfile_user_id_de589eff; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ppcn_ppcnfile_user_id_de589eff ON public.ppcn_ppcnfile USING btree (user_id);


--
-- Name: ppcn_ppcnworkflowstep_ppcn_id_e0c05733; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ppcn_ppcnworkflowstep_ppcn_id_e0c05733 ON public.ppcn_ppcnworkflowstep USING btree (ppcn_id);


--
-- Name: ppcn_ppcnworkflowstep_user_id_33177343; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ppcn_ppcnworkflowstep_user_id_33177343 ON public.ppcn_ppcnworkflowstep USING btree (user_id);


--
-- Name: ppcn_ppcnworkflowstepfile_user_id_345e37d6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ppcn_ppcnworkflowstepfile_user_id_345e37d6 ON public.ppcn_ppcnworkflowstepfile USING btree (user_id);


--
-- Name: ppcn_ppcnworkflowstepfile_workflow_step_id_29a9efd3; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ppcn_ppcnworkflowstepfile_workflow_step_id_29a9efd3 ON public.ppcn_ppcnworkflowstepfile USING btree (workflow_step_id);


--
-- Name: ppcn_sector_geographicLevel_id_8827ad6c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "ppcn_sector_geographicLevel_id_8827ad6c" ON public.ppcn_sector USING btree ("geographicLevel_id");


--
-- Name: ppcn_subsector_sector_id_0a8366aa; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ppcn_subsector_sector_id_0a8366aa ON public.ppcn_subsector USING btree (sector_id);


--
-- Name: report_data_reportfile_user_id_96d75ab0; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX report_data_reportfile_user_id_96d75ab0 ON public.report_data_reportfile USING btree (user_id);


--
-- Name: report_data_reportfilemetadata_report_file_id_4f18b601; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX report_data_reportfilemetadata_report_file_id_4f18b601 ON public.report_data_reportfilemetadata USING btree (report_file_id);


--
-- Name: report_data_reportfileversion_report_file_id_3d0c13cb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX report_data_reportfileversion_report_file_id_3d0c13cb ON public.report_data_reportfileversion USING btree (report_file_id);


--
-- Name: report_data_reportfileversion_user_id_c0ab27e1; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX report_data_reportfileversion_user_id_c0ab27e1 ON public.report_data_reportfileversion USING btree (user_id);


--
-- Name: report_data_reportfileversion_version_16e5e2f7_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX report_data_reportfileversion_version_16e5e2f7_like ON public.report_data_reportfileversion USING btree (version varchar_pattern_ops);


--
-- Name: users_customuser_groups_customuser_id_958147bf; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX users_customuser_groups_customuser_id_958147bf ON public.users_customuser_groups USING btree (customuser_id);


--
-- Name: users_customuser_groups_group_id_01390b14; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX users_customuser_groups_group_id_01390b14 ON public.users_customuser_groups USING btree (group_id);


--
-- Name: users_customuser_user_permissions_customuser_id_5771478b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX users_customuser_user_permissions_customuser_id_5771478b ON public.users_customuser_user_permissions USING btree (customuser_id);


--
-- Name: users_customuser_user_permissions_permission_id_baaa2f74; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX users_customuser_user_permissions_permission_id_baaa2f74 ON public.users_customuser_user_permissions USING btree (permission_id);


--
-- Name: users_customuser_username_80452fdf_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX users_customuser_username_80452fdf_like ON public.users_customuser USING btree (username varchar_pattern_ops);


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_users_customuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_users_customuser_id FOREIGN KEY (user_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mccr_changelog mccr_changelog_mccr_id_1b6a3dff_fk_mccr_mccrregistry_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_changelog
    ADD CONSTRAINT mccr_changelog_mccr_id_1b6a3dff_fk_mccr_mccrregistry_id FOREIGN KEY (mccr_id) REFERENCES public.mccr_mccrregistry(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mccr_changelog mccr_changelog_user_id_4678b3eb_fk_users_customuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_changelog
    ADD CONSTRAINT mccr_changelog_user_id_4678b3eb_fk_users_customuser_id FOREIGN KEY (user_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mccr_mccrfile mccr_mccrfile_mccr_id_08c07172_fk_mccr_mccrregistry_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_mccrfile
    ADD CONSTRAINT mccr_mccrfile_mccr_id_08c07172_fk_mccr_mccrregistry_id FOREIGN KEY (mccr_id) REFERENCES public.mccr_mccrregistry(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mccr_mccrfile mccr_mccrfile_user_id_517351bd_fk_users_customuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_mccrfile
    ADD CONSTRAINT mccr_mccrfile_user_id_517351bd_fk_users_customuser_id FOREIGN KEY (user_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mccr_mccrregistry mccr_mccrregistry_mitigation_id_42e7601c_fk_mitigatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_mccrregistry
    ADD CONSTRAINT mccr_mccrregistry_mitigation_id_42e7601c_fk_mitigatio FOREIGN KEY (mitigation_id) REFERENCES public.mitigation_action_mitigation(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mccr_mccrregistry mccr_mccrregistry_user_id_8ce12972_fk_users_customuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_mccrregistry
    ADD CONSTRAINT mccr_mccrregistry_user_id_8ce12972_fk_users_customuser_id FOREIGN KEY (user_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mccr_mccrregistry mccr_mccrregistry_user_type_id_36dc1127_fk_mccr_mccrusertype_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_mccrregistry
    ADD CONSTRAINT mccr_mccrregistry_user_type_id_36dc1127_fk_mccr_mccrusertype_id FOREIGN KEY (user_type_id) REFERENCES public.mccr_mccrusertype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mccr_mccrregistryovvrelation mccr_mccrregistryovv_mccr_id_6c978edf_fk_mccr_mccr; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_mccrregistryovvrelation
    ADD CONSTRAINT mccr_mccrregistryovv_mccr_id_6c978edf_fk_mccr_mccr FOREIGN KEY (mccr_id) REFERENCES public.mccr_mccrregistry(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mccr_mccrregistryovvrelation mccr_mccrregistryovvrelation_ovv_id_25f87d39_fk_mccr_ovv_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_mccrregistryovvrelation
    ADD CONSTRAINT mccr_mccrregistryovvrelation_ovv_id_25f87d39_fk_mccr_ovv_id FOREIGN KEY (ovv_id) REFERENCES public.mccr_ovv(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mccr_mccrworkflowstepfile mccr_mccrworkflowste_user_id_0c2c21c3_fk_users_cus; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_mccrworkflowstepfile
    ADD CONSTRAINT mccr_mccrworkflowste_user_id_0c2c21c3_fk_users_cus FOREIGN KEY (user_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mccr_mccrworkflowstepfile mccr_mccrworkflowste_workflow_step_id_a4e95d21_fk_mccr_mccr; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_mccrworkflowstepfile
    ADD CONSTRAINT mccr_mccrworkflowste_workflow_step_id_a4e95d21_fk_mccr_mccr FOREIGN KEY (workflow_step_id) REFERENCES public.mccr_mccrworkflowstep(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mccr_mccrworkflowstep mccr_mccrworkflowstep_mccr_id_00c7d236_fk_mccr_mccrregistry_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_mccrworkflowstep
    ADD CONSTRAINT mccr_mccrworkflowstep_mccr_id_00c7d236_fk_mccr_mccrregistry_id FOREIGN KEY (mccr_id) REFERENCES public.mccr_mccrregistry(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mccr_mccrworkflowstep mccr_mccrworkflowstep_user_id_c48a5841_fk_users_customuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mccr_mccrworkflowstep
    ADD CONSTRAINT mccr_mccrworkflowstep_user_id_c48a5841_fk_users_customuser_id FOREIGN KEY (user_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitigation_action_changelog mitigation_action_ch_mitigation_action_id_a4801a1b_fk_mitigatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_changelog
    ADD CONSTRAINT mitigation_action_ch_mitigation_action_id_a4801a1b_fk_mitigatio FOREIGN KEY (mitigation_action_id) REFERENCES public.mitigation_action_mitigation(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitigation_action_changelog mitigation_action_ch_user_id_c0f7d427_fk_users_cus; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_changelog
    ADD CONSTRAINT mitigation_action_ch_user_id_c0f7d427_fk_users_cus FOREIGN KEY (user_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitigation_action_finance mitigation_action_fi_status_id_a940da2d_fk_mitigatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_finance
    ADD CONSTRAINT mitigation_action_fi_status_id_a940da2d_fk_mitigatio FOREIGN KEY (status_id) REFERENCES public.mitigation_action_financestatus(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitigation_action_initiative mitigation_action_in_contact_id_b4f438da_fk_mitigatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_initiative
    ADD CONSTRAINT mitigation_action_in_contact_id_b4f438da_fk_mitigatio FOREIGN KEY (contact_id) REFERENCES public.mitigation_action_contact(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitigation_action_initiative mitigation_action_in_finance_id_605f54db_fk_mitigatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_initiative
    ADD CONSTRAINT mitigation_action_in_finance_id_605f54db_fk_mitigatio FOREIGN KEY (finance_id) REFERENCES public.mitigation_action_initiativefinance(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitigation_action_initiativefinance mitigation_action_in_finance_source_type__1d97a554_fk_mitigatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_initiativefinance
    ADD CONSTRAINT mitigation_action_in_finance_source_type__1d97a554_fk_mitigatio FOREIGN KEY (finance_source_type_id) REFERENCES public.mitigation_action_financesourcetype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitigation_action_initiative mitigation_action_in_initiative_type_id_54661d5b_fk_mitigatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_initiative
    ADD CONSTRAINT mitigation_action_in_initiative_type_id_54661d5b_fk_mitigatio FOREIGN KEY (initiative_type_id) REFERENCES public.mitigation_action_initiativetype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitigation_action_initiative mitigation_action_in_status_id_44027193_fk_mitigatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_initiative
    ADD CONSTRAINT mitigation_action_in_status_id_44027193_fk_mitigatio FOREIGN KEY (status_id) REFERENCES public.mitigation_action_status(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitigation_action_initiativefinance mitigation_action_in_status_id_fa3cebf4_fk_mitigatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_initiativefinance
    ADD CONSTRAINT mitigation_action_in_status_id_fa3cebf4_fk_mitigatio FOREIGN KEY (status_id) REFERENCES public.mitigation_action_financestatus(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitigation_action_maworkflowstep mitigation_action_ma_mitigation_action_id_e3bbba48_fk_mitigatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_maworkflowstep
    ADD CONSTRAINT mitigation_action_ma_mitigation_action_id_e3bbba48_fk_mitigatio FOREIGN KEY (mitigation_action_id) REFERENCES public.mitigation_action_mitigation(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitigation_action_maworkflowstepfile mitigation_action_ma_user_id_67fc87e2_fk_users_cus; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_maworkflowstepfile
    ADD CONSTRAINT mitigation_action_ma_user_id_67fc87e2_fk_users_cus FOREIGN KEY (user_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitigation_action_maworkflowstep mitigation_action_ma_user_id_f1494fbc_fk_users_cus; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_maworkflowstep
    ADD CONSTRAINT mitigation_action_ma_user_id_f1494fbc_fk_users_cus FOREIGN KEY (user_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitigation_action_maworkflowstepfile mitigation_action_ma_workflow_step_id_0cba48d8_fk_mitigatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_maworkflowstepfile
    ADD CONSTRAINT mitigation_action_ma_workflow_step_id_0cba48d8_fk_mitigatio FOREIGN KEY (workflow_step_id) REFERENCES public.mitigation_action_maworkflowstep(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitigation_action_mitigation_comments mitigation_action_mi_comment_id_d430a9a4_fk_workflow_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_mitigation_comments
    ADD CONSTRAINT mitigation_action_mi_comment_id_d430a9a4_fk_workflow_ FOREIGN KEY (comment_id) REFERENCES public.workflow_comment(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitigation_action_mitigation mitigation_action_mi_contact_id_b84fb28c_fk_mitigatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_mitigation
    ADD CONSTRAINT mitigation_action_mi_contact_id_b84fb28c_fk_mitigatio FOREIGN KEY (contact_id) REFERENCES public.mitigation_action_contact(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitigation_action_mitigation mitigation_action_mi_finance_id_b7a14603_fk_mitigatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_mitigation
    ADD CONSTRAINT mitigation_action_mi_finance_id_b7a14603_fk_mitigatio FOREIGN KEY (finance_id) REFERENCES public.mitigation_action_finance(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitigation_action_mitigation mitigation_action_mi_geographic_scale_id_c6c7ec6a_fk_mitigatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_mitigation
    ADD CONSTRAINT mitigation_action_mi_geographic_scale_id_c6c7ec6a_fk_mitigatio FOREIGN KEY (geographic_scale_id) REFERENCES public.mitigation_action_geographicscale(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitigation_action_mitigation_ingei_compliances mitigation_action_mi_ingeicompliance_id_3a83b0d9_fk_mitigatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_mitigation_ingei_compliances
    ADD CONSTRAINT mitigation_action_mi_ingeicompliance_id_3a83b0d9_fk_mitigatio FOREIGN KEY (ingeicompliance_id) REFERENCES public.mitigation_action_ingeicompliance(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitigation_action_mitigation mitigation_action_mi_initiative_id_342cab00_fk_mitigatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_mitigation
    ADD CONSTRAINT mitigation_action_mi_initiative_id_342cab00_fk_mitigatio FOREIGN KEY (initiative_id) REFERENCES public.mitigation_action_initiative(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitigation_action_mitigation mitigation_action_mi_institution_id_06109e57_fk_mitigatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_mitigation
    ADD CONSTRAINT mitigation_action_mi_institution_id_06109e57_fk_mitigatio FOREIGN KEY (institution_id) REFERENCES public.mitigation_action_institution(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitigation_action_mitigation mitigation_action_mi_location_id_01de67fe_fk_mitigatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_mitigation
    ADD CONSTRAINT mitigation_action_mi_location_id_01de67fe_fk_mitigatio FOREIGN KEY (location_id) REFERENCES public.mitigation_action_location(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitigation_action_mitigation_comments mitigation_action_mi_mitigation_id_98b68b5f_fk_mitigatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_mitigation_comments
    ADD CONSTRAINT mitigation_action_mi_mitigation_id_98b68b5f_fk_mitigatio FOREIGN KEY (mitigation_id) REFERENCES public.mitigation_action_mitigation(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitigation_action_mitigation_ingei_compliances mitigation_action_mi_mitigation_id_f4c4460f_fk_mitigatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_mitigation_ingei_compliances
    ADD CONSTRAINT mitigation_action_mi_mitigation_id_f4c4460f_fk_mitigatio FOREIGN KEY (mitigation_id) REFERENCES public.mitigation_action_mitigation(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitigation_action_mitigation mitigation_action_mi_progress_indicator_i_a9ea5158_fk_mitigatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_mitigation
    ADD CONSTRAINT mitigation_action_mi_progress_indicator_i_a9ea5158_fk_mitigatio FOREIGN KEY (progress_indicator_id) REFERENCES public.mitigation_action_progressindicator(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitigation_action_mitigation mitigation_action_mi_registration_type_id_51575b17_fk_mitigatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_mitigation
    ADD CONSTRAINT mitigation_action_mi_registration_type_id_51575b17_fk_mitigatio FOREIGN KEY (registration_type_id) REFERENCES public.mitigation_action_registrationtype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitigation_action_mitigation mitigation_action_mi_status_id_820e5056_fk_mitigatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_mitigation
    ADD CONSTRAINT mitigation_action_mi_status_id_820e5056_fk_mitigatio FOREIGN KEY (status_id) REFERENCES public.mitigation_action_status(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mitigation_action_mitigation mitigation_action_mi_user_id_b61093af_fk_users_cus; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mitigation_action_mitigation
    ADD CONSTRAINT mitigation_action_mi_user_id_b61093af_fk_users_cus FOREIGN KEY (user_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ppcn_changelog ppcn_changelog_ppcn_id_59e2c714_fk_ppcn_ppcn_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_changelog
    ADD CONSTRAINT ppcn_changelog_ppcn_id_59e2c714_fk_ppcn_ppcn_id FOREIGN KEY (ppcn_id) REFERENCES public.ppcn_ppcn(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ppcn_changelog ppcn_changelog_user_id_bb4cef6f_fk_users_customuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_changelog
    ADD CONSTRAINT ppcn_changelog_user_id_bb4cef6f_fk_users_customuser_id FOREIGN KEY (user_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ppcn_geiactivitytype ppcn_geiactivitytype_sector_id_c7f8fcfb_fk_ppcn_sector_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_geiactivitytype
    ADD CONSTRAINT ppcn_geiactivitytype_sector_id_c7f8fcfb_fk_ppcn_sector_id FOREIGN KEY (sector_id) REFERENCES public.ppcn_sector(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ppcn_geiactivitytype ppcn_geiactivitytype_sub_sector_id_c1e19ae2_fk_ppcn_subs; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_geiactivitytype
    ADD CONSTRAINT ppcn_geiactivitytype_sub_sector_id_c1e19ae2_fk_ppcn_subs FOREIGN KEY (sub_sector_id) REFERENCES public.ppcn_subsector(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ppcn_geiorganization_gei_activity_types ppcn_geiorganization_geiactivitytype_id_048f50be_fk_ppcn_geia; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_geiorganization_gei_activity_types
    ADD CONSTRAINT ppcn_geiorganization_geiactivitytype_id_048f50be_fk_ppcn_geia FOREIGN KEY (geiactivitytype_id) REFERENCES public.ppcn_geiactivitytype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ppcn_geiorganization_gei_activity_types ppcn_geiorganization_geiorganization_id_82dd23c3_fk_ppcn_geio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_geiorganization_gei_activity_types
    ADD CONSTRAINT ppcn_geiorganization_geiorganization_id_82dd23c3_fk_ppcn_geio FOREIGN KEY (geiorganization_id) REFERENCES public.ppcn_geiorganization(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ppcn_geiorganization ppcn_geiorganization_ovv_id_17530bac_fk_mccr_ovv_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_geiorganization
    ADD CONSTRAINT ppcn_geiorganization_ovv_id_17530bac_fk_mccr_ovv_id FOREIGN KEY (ovv_id) REFERENCES public.mccr_ovv(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ppcn_organization ppcn_organization_contact_id_d94c7c13_fk_mitigatio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_organization
    ADD CONSTRAINT ppcn_organization_contact_id_d94c7c13_fk_mitigatio FOREIGN KEY (contact_id) REFERENCES public.mitigation_action_contact(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ppcn_ppcn_comments ppcn_ppcn_comments_comment_id_82a722c9_fk_workflow_comment_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcn_comments
    ADD CONSTRAINT ppcn_ppcn_comments_comment_id_82a722c9_fk_workflow_comment_id FOREIGN KEY (comment_id) REFERENCES public.workflow_comment(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ppcn_ppcn_comments ppcn_ppcn_comments_ppcn_id_3a7defde_fk_ppcn_ppcn_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcn_comments
    ADD CONSTRAINT ppcn_ppcn_comments_ppcn_id_3a7defde_fk_ppcn_ppcn_id FOREIGN KEY (ppcn_id) REFERENCES public.ppcn_ppcn(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ppcn_ppcn ppcn_ppcn_gei_organization_id_debbc419_fk_ppcn_geio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcn
    ADD CONSTRAINT ppcn_ppcn_gei_organization_id_debbc419_fk_ppcn_geio FOREIGN KEY (gei_organization_id) REFERENCES public.ppcn_geiorganization(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ppcn_ppcn ppcn_ppcn_geographic_level_id_c1066abb_fk_ppcn_geog; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcn
    ADD CONSTRAINT ppcn_ppcn_geographic_level_id_c1066abb_fk_ppcn_geog FOREIGN KEY (geographic_level_id) REFERENCES public.ppcn_geographiclevel(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ppcn_ppcn ppcn_ppcn_organization_id_7c48620d_fk_ppcn_organization_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcn
    ADD CONSTRAINT ppcn_ppcn_organization_id_7c48620d_fk_ppcn_organization_id FOREIGN KEY (organization_id) REFERENCES public.ppcn_organization(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ppcn_ppcn ppcn_ppcn_recognition_type_id_1bee6248_fk_ppcn_reco; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcn
    ADD CONSTRAINT ppcn_ppcn_recognition_type_id_1bee6248_fk_ppcn_reco FOREIGN KEY (recognition_type_id) REFERENCES public.ppcn_recognitiontype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ppcn_ppcn ppcn_ppcn_required_level_id_da88f790_fk_ppcn_requiredlevel_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcn
    ADD CONSTRAINT ppcn_ppcn_required_level_id_da88f790_fk_ppcn_requiredlevel_id FOREIGN KEY (required_level_id) REFERENCES public.ppcn_requiredlevel(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ppcn_ppcn ppcn_ppcn_user_id_41508d8e_fk_users_customuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcn
    ADD CONSTRAINT ppcn_ppcn_user_id_41508d8e_fk_users_customuser_id FOREIGN KEY (user_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ppcn_ppcnfile ppcn_ppcnfile_ppcn_form_id_258b17a5_fk_ppcn_ppcn_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcnfile
    ADD CONSTRAINT ppcn_ppcnfile_ppcn_form_id_258b17a5_fk_ppcn_ppcn_id FOREIGN KEY (ppcn_form_id) REFERENCES public.ppcn_ppcn(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ppcn_ppcnfile ppcn_ppcnfile_user_id_de589eff_fk_users_customuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcnfile
    ADD CONSTRAINT ppcn_ppcnfile_user_id_de589eff_fk_users_customuser_id FOREIGN KEY (user_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ppcn_ppcnworkflowstepfile ppcn_ppcnworkflowste_user_id_345e37d6_fk_users_cus; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcnworkflowstepfile
    ADD CONSTRAINT ppcn_ppcnworkflowste_user_id_345e37d6_fk_users_cus FOREIGN KEY (user_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ppcn_ppcnworkflowstepfile ppcn_ppcnworkflowste_workflow_step_id_29a9efd3_fk_ppcn_ppcn; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcnworkflowstepfile
    ADD CONSTRAINT ppcn_ppcnworkflowste_workflow_step_id_29a9efd3_fk_ppcn_ppcn FOREIGN KEY (workflow_step_id) REFERENCES public.ppcn_ppcnworkflowstep(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ppcn_ppcnworkflowstep ppcn_ppcnworkflowstep_ppcn_id_e0c05733_fk_ppcn_ppcn_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcnworkflowstep
    ADD CONSTRAINT ppcn_ppcnworkflowstep_ppcn_id_e0c05733_fk_ppcn_ppcn_id FOREIGN KEY (ppcn_id) REFERENCES public.ppcn_ppcn(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ppcn_ppcnworkflowstep ppcn_ppcnworkflowstep_user_id_33177343_fk_users_customuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_ppcnworkflowstep
    ADD CONSTRAINT ppcn_ppcnworkflowstep_user_id_33177343_fk_users_customuser_id FOREIGN KEY (user_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ppcn_sector ppcn_sector_geographicLevel_id_8827ad6c_fk_ppcn_geog; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_sector
    ADD CONSTRAINT "ppcn_sector_geographicLevel_id_8827ad6c_fk_ppcn_geog" FOREIGN KEY ("geographicLevel_id") REFERENCES public.ppcn_geographiclevel(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ppcn_subsector ppcn_subsector_sector_id_0a8366aa_fk_ppcn_sector_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ppcn_subsector
    ADD CONSTRAINT ppcn_subsector_sector_id_0a8366aa_fk_ppcn_sector_id FOREIGN KEY (sector_id) REFERENCES public.ppcn_sector(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: report_data_reportfileversion report_data_reportfi_report_file_id_3d0c13cb_fk_report_da; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_data_reportfileversion
    ADD CONSTRAINT report_data_reportfi_report_file_id_3d0c13cb_fk_report_da FOREIGN KEY (report_file_id) REFERENCES public.report_data_reportfile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: report_data_reportfilemetadata report_data_reportfi_report_file_id_4f18b601_fk_report_da; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_data_reportfilemetadata
    ADD CONSTRAINT report_data_reportfi_report_file_id_4f18b601_fk_report_da FOREIGN KEY (report_file_id) REFERENCES public.report_data_reportfile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: report_data_reportfileversion report_data_reportfi_user_id_c0ab27e1_fk_users_cus; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_data_reportfileversion
    ADD CONSTRAINT report_data_reportfi_user_id_c0ab27e1_fk_users_cus FOREIGN KEY (user_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: report_data_reportfile report_data_reportfile_user_id_96d75ab0_fk_users_customuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_data_reportfile
    ADD CONSTRAINT report_data_reportfile_user_id_96d75ab0_fk_users_customuser_id FOREIGN KEY (user_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_customgroup users_customgroup_group_id_444dc57a_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_customgroup
    ADD CONSTRAINT users_customgroup_group_id_444dc57a_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_customuser_groups users_customuser_gro_customuser_id_958147bf_fk_users_cus; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_customuser_groups
    ADD CONSTRAINT users_customuser_gro_customuser_id_958147bf_fk_users_cus FOREIGN KEY (customuser_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_customuser_groups users_customuser_groups_group_id_01390b14_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_customuser_groups
    ADD CONSTRAINT users_customuser_groups_group_id_01390b14_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_customuser_user_permissions users_customuser_use_customuser_id_5771478b_fk_users_cus; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_customuser_user_permissions
    ADD CONSTRAINT users_customuser_use_customuser_id_5771478b_fk_users_cus FOREIGN KEY (customuser_id) REFERENCES public.users_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_customuser_user_permissions users_customuser_use_permission_id_baaa2f74_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_customuser_user_permissions
    ADD CONSTRAINT users_customuser_use_permission_id_baaa2f74_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

