--
-- PostgreSQL database dump
--

-- Dumped from database version 14.13 (Ubuntu 14.13-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.13 (Ubuntu 14.13-0ubuntu0.22.04.1)

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

--
-- Name: uuid-ossp; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;


--
-- Name: EXTENSION "uuid-ossp"; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';


--
-- Name: gender; Type: TYPE; Schema: public; Owner: wordsmanipulator
--

CREATE TYPE public.gender AS ENUM (
    'masculine',
    'feminine',
    'neuter',
    'common'
);


ALTER TYPE public.gender OWNER TO wordsmanipulator;

--
-- Name: number; Type: TYPE; Schema: public; Owner: wordsmanipulator
--

CREATE TYPE public.number AS ENUM (
    'singular',
    'plural'
);


ALTER TYPE public.number OWNER TO wordsmanipulator;

--
-- Name: person; Type: TYPE; Schema: public; Owner: wordsmanipulator
--

CREATE TYPE public.person AS ENUM (
    'first',
    'second',
    'third'
);


ALTER TYPE public.person OWNER TO wordsmanipulator;

--
-- Name: voice; Type: TYPE; Schema: public; Owner: wordsmanipulator
--

CREATE TYPE public.voice AS ENUM (
    'active',
    'passive'
);


ALTER TYPE public.voice OWNER TO wordsmanipulator;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: article; Type: TABLE; Schema: public; Owner: wordsmanipulator
--

CREATE TABLE public.article (
    article_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    article_form character varying(5) NOT NULL,
    article_fk_language_id uuid NOT NULL
);


ALTER TABLE public.article OWNER TO wordsmanipulator;

--
-- Name: declension; Type: TABLE; Schema: public; Owner: wordsmanipulator
--

CREATE TABLE public.declension (
    declension_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    declension_predecessor character varying(20),
    declension_person public.person NOT NULL,
    declension_form character varying(50) NOT NULL,
    declension_taken_at timestamp without time zone,
    declension_number public.number NOT NULL,
    declension_fk_word_id uuid NOT NULL
);


ALTER TABLE public.declension OWNER TO wordsmanipulator;

--
-- Name: frequency; Type: TABLE; Schema: public; Owner: wordsmanipulator
--

CREATE TABLE public.frequency (
    frequency_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    frequency_label character varying(50) NOT NULL,
    frequency_lowest_class integer NOT NULL,
    frequency_highest_class integer,
    CONSTRAINT check_frequency_highest_class CHECK ((frequency_highest_class >= 0)),
    CONSTRAINT check_frequency_highest_class_frequency_lowest_class CHECK ((frequency_highest_class > frequency_lowest_class)),
    CONSTRAINT check_frequency_lowest_class CHECK ((frequency_lowest_class >= 0)),
    CONSTRAINT frequency_check CHECK ((frequency_highest_class > frequency_lowest_class)),
    CONSTRAINT frequency_frequency_highest_class_check CHECK ((frequency_highest_class >= 0)),
    CONSTRAINT frequency_frequency_lowest_class_check CHECK ((frequency_lowest_class >= 0))
);


ALTER TABLE public.frequency OWNER TO wordsmanipulator;

--
-- Name: language; Type: TABLE; Schema: public; Owner: wordsmanipulator
--

CREATE TABLE public.language (
    language_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    language_name character varying(20) NOT NULL,
    language_set_1_code character(3) NOT NULL,
    language_set_2t_code character(2) NOT NULL
);


ALTER TABLE public.language OWNER TO wordsmanipulator;

--
-- Name: mood; Type: TABLE; Schema: public; Owner: wordsmanipulator
--

CREATE TABLE public.mood (
    mood_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    mood_name character varying(50) NOT NULL,
    mood_fk_language_id uuid NOT NULL
);


ALTER TABLE public.mood OWNER TO wordsmanipulator;

--
-- Name: nouns; Type: TABLE; Schema: public; Owner: wordsmanipulator
--

CREATE TABLE public.nouns (
    noun_fk_word_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    noun_fk_article_id uuid NOT NULL,
    noun_plural character varying(50) NOT NULL,
    noun_plural_taken_at timestamp without time zone,
    noun_article_taken_at timestamp without time zone
);


ALTER TABLE public.nouns OWNER TO wordsmanipulator;

--
-- Name: sentence; Type: TABLE; Schema: public; Owner: wordsmanipulator
--

CREATE TABLE public.sentence (
    sentence_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    sentence_form text NOT NULL,
    sentence_source_id uuid
);


ALTER TABLE public.sentence OWNER TO wordsmanipulator;

--
-- Name: speech_part; Type: TABLE; Schema: public; Owner: wordsmanipulator
--

CREATE TABLE public.speech_part (
    speech_part_model_name character varying(10) NOT NULL,
    speech_part_name character varying(30) NOT NULL,
    speech_part_id uuid DEFAULT public.uuid_generate_v4() NOT NULL
);


ALTER TABLE public.speech_part OWNER TO wordsmanipulator;

--
-- Name: tense; Type: TABLE; Schema: public; Owner: wordsmanipulator
--

CREATE TABLE public.tense (
    tense_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    tense_name character varying(70) NOT NULL,
    tense_fk_language_id uuid NOT NULL
);


ALTER TABLE public.tense OWNER TO wordsmanipulator;

--
-- Name: translation; Type: TABLE; Schema: public; Owner: wordsmanipulator
--

CREATE TABLE public.translation (
    translation_source_id uuid NOT NULL,
    translation_target_id uuid NOT NULL
);


ALTER TABLE public.translation OWNER TO wordsmanipulator;

--
-- Name: verb_conjugation; Type: TABLE; Schema: public; Owner: wordsmanipulator
--

CREATE TABLE public.verb_conjugation (
    verb_conjugation_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    verb_conjugation_voice public.voice NOT NULL,
    verb_conjugation_fk_tense_id uuid NOT NULL,
    verb_conjugation_fk_mood_id uuid NOT NULL,
    verb_conjugation_form character varying(100) NOT NULL,
    verb_conjugation_person public.person NOT NULL,
    verb_conjugation_gender public.gender,
    verb_conjugation_number public.number NOT NULL,
    verb_conjugation_fk_word_id uuid NOT NULL,
    verb_conjugation_taken_at timestamp with time zone
);


ALTER TABLE public.verb_conjugation OWNER TO wordsmanipulator;

--
-- Name: word; Type: TABLE; Schema: public; Owner: wordsmanipulator
--

CREATE TABLE public.word (
    word_lemma character varying(50) NOT NULL,
    word_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    word_fk_speech_part_id uuid,
    word_initial_form character varying(100) NOT NULL,
    word_fk_frequency_id uuid,
    word_frequency_class integer,
    word_fk_language_id uuid NOT NULL,
    word_taken_at timestamp with time zone,
    CONSTRAINT check_word_frequency_class CHECK ((word_frequency_class >= 0))
);


ALTER TABLE public.word OWNER TO wordsmanipulator;

--
-- Name: word_sentence; Type: TABLE; Schema: public; Owner: wordsmanipulator
--

CREATE TABLE public.word_sentence (
    word_id uuid NOT NULL,
    sentence_id uuid NOT NULL
);


ALTER TABLE public.word_sentence OWNER TO wordsmanipulator;

--
-- Data for Name: article; Type: TABLE DATA; Schema: public; Owner: wordsmanipulator
--

COPY public.article (article_id, article_form, article_fk_language_id) FROM stdin;
\.


--
-- Data for Name: declension; Type: TABLE DATA; Schema: public; Owner: wordsmanipulator
--

COPY public.declension (declension_id, declension_predecessor, declension_person, declension_form, declension_taken_at, declension_number, declension_fk_word_id) FROM stdin;
\.


--
-- Data for Name: frequency; Type: TABLE DATA; Schema: public; Owner: wordsmanipulator
--

COPY public.frequency (frequency_id, frequency_label, frequency_lowest_class, frequency_highest_class) FROM stdin;
2e9d0bcc-91cc-4ee7-8d11-2586773a45bd	common	0	3
ff59eb98-e477-4c07-9181-9d98d9526e7f	regular	4	6
c37f211a-75d3-4f2e-8e89-48230c60d070	frequent	7	11
2daa03b2-2c65-40ea-8de8-474df8a5fe6d	occasional	12	15
2e6760b9-fb1f-48e1-964c-7fe52411e304	rare	16	19
cb5c7b6a-105d-4f5b-ab06-93b350cd54d1	specialized	20	\N
\.


--
-- Data for Name: language; Type: TABLE DATA; Schema: public; Owner: wordsmanipulator
--

COPY public.language (language_id, language_name, language_set_1_code, language_set_2t_code) FROM stdin;
\.


--
-- Data for Name: mood; Type: TABLE DATA; Schema: public; Owner: wordsmanipulator
--

COPY public.mood (mood_id, mood_name, mood_fk_language_id) FROM stdin;
\.


--
-- Data for Name: nouns; Type: TABLE DATA; Schema: public; Owner: wordsmanipulator
--

COPY public.nouns (noun_fk_word_id, noun_fk_article_id, noun_plural, noun_plural_taken_at, noun_article_taken_at) FROM stdin;
\.


--
-- Data for Name: sentence; Type: TABLE DATA; Schema: public; Owner: wordsmanipulator
--

COPY public.sentence (sentence_id, sentence_form, sentence_source_id) FROM stdin;
\.


--
-- Data for Name: speech_part; Type: TABLE DATA; Schema: public; Owner: wordsmanipulator
--

COPY public.speech_part (speech_part_model_name, speech_part_name, speech_part_id) FROM stdin;
ADJ	adjective	f884547d-e184-4f71-a388-7d7979bc63b4
ADP	adposition	f2f01e90-62c1-4fcd-92d7-8c9e46c2da21
ADV	adverb	29f54e2f-4c0d-44a9-bd6c-cc6a2b57c726
AUX	auxiliary	0108d7ff-47be-48b9-8106-caebe92909da
CONJ	conjunction	ae77c2a8-9335-4d09-8856-d483eae398f7
CCONJ	coordinating conjunction	e9d07113-c16a-44e8-8923-bed60912660e
DET	determiner	41496771-c0ae-48ef-840e-41b92c953ff2
INTJ	interjection	174572b2-c3a2-4230-b53a-406d893412ca
NOUN	noun	65274b75-011d-42d8-8c69-af139d8d03c8
NUM	numeral	33c7d91c-e56f-4923-bce4-7f40368f1860
PART	particle	5a503015-a13b-41f1-9aa0-448ff28ef240
PRON	pronoun	d6d067aa-78a4-4c1f-90bb-15d30f39df1a
PROPN	proper noun	937a71c7-2687-4e74-a6d4-eb84962b3e27
PUNCT	punctuation	2dc8ca2d-b9d6-4cdd-8d22-0dda613f98a1
SCONJ	subordinating conjunction	349c28dd-3266-416b-aff1-0fbcc3d3a820
SYM	symbol	ee896409-a6d7-4ad3-81dd-2663911a1b6a
VERB	verb	8615e2ee-5f34-4bff-8584-949d2fb66e87
X	other	cc0d2b72-0055-4020-84fe-23b6665b317b
EOL	end of line	2d3c55a0-19c0-4805-a4e8-3a4b6593aa2f
SPACE	space	34b43a4f-46ee-4c2e-b052-0dcd667294f0
PHR	phrase	6c97113b-e183-49e2-94bb-88366d43fb17
\.


--
-- Data for Name: tense; Type: TABLE DATA; Schema: public; Owner: wordsmanipulator
--

COPY public.tense (tense_id, tense_name, tense_fk_language_id) FROM stdin;
\.


--
-- Data for Name: translation; Type: TABLE DATA; Schema: public; Owner: wordsmanipulator
--

COPY public.translation (translation_source_id, translation_target_id) FROM stdin;
\.


--
-- Data for Name: verb_conjugation; Type: TABLE DATA; Schema: public; Owner: wordsmanipulator
--

COPY public.verb_conjugation (verb_conjugation_id, verb_conjugation_voice, verb_conjugation_fk_tense_id, verb_conjugation_fk_mood_id, verb_conjugation_form, verb_conjugation_person, verb_conjugation_gender, verb_conjugation_number, verb_conjugation_fk_word_id, verb_conjugation_taken_at) FROM stdin;
\.


--
-- Data for Name: word; Type: TABLE DATA; Schema: public; Owner: wordsmanipulator
--

COPY public.word (word_lemma, word_id, word_fk_speech_part_id, word_initial_form, word_fk_frequency_id, word_frequency_class, word_fk_language_id, word_taken_at) FROM stdin;
\.


--
-- Data for Name: word_sentence; Type: TABLE DATA; Schema: public; Owner: wordsmanipulator
--

COPY public.word_sentence (word_id, sentence_id) FROM stdin;
\.


--
-- Name: article article_pkey; Type: CONSTRAINT; Schema: public; Owner: wordsmanipulator
--

ALTER TABLE ONLY public.article
    ADD CONSTRAINT article_pkey PRIMARY KEY (article_id);


--
-- Name: declension declension_pkey; Type: CONSTRAINT; Schema: public; Owner: wordsmanipulator
--

ALTER TABLE ONLY public.declension
    ADD CONSTRAINT declension_pkey PRIMARY KEY (declension_id);


--
-- Name: frequency frequency_pk; Type: CONSTRAINT; Schema: public; Owner: wordsmanipulator
--

ALTER TABLE ONLY public.frequency
    ADD CONSTRAINT frequency_pk PRIMARY KEY (frequency_id);


--
-- Name: frequency frequency_unique; Type: CONSTRAINT; Schema: public; Owner: wordsmanipulator
--

ALTER TABLE ONLY public.frequency
    ADD CONSTRAINT frequency_unique UNIQUE (frequency_label);


--
-- Name: frequency frequency_unique_1; Type: CONSTRAINT; Schema: public; Owner: wordsmanipulator
--

ALTER TABLE ONLY public.frequency
    ADD CONSTRAINT frequency_unique_1 UNIQUE (frequency_lowest_class);


--
-- Name: language language_language_name_key; Type: CONSTRAINT; Schema: public; Owner: wordsmanipulator
--

ALTER TABLE ONLY public.language
    ADD CONSTRAINT language_language_name_key UNIQUE (language_name);


--
-- Name: language language_language_set_1_code_key; Type: CONSTRAINT; Schema: public; Owner: wordsmanipulator
--

ALTER TABLE ONLY public.language
    ADD CONSTRAINT language_language_set_1_code_key UNIQUE (language_set_1_code);


--
-- Name: language language_language_set_2t_code_key; Type: CONSTRAINT; Schema: public; Owner: wordsmanipulator
--

ALTER TABLE ONLY public.language
    ADD CONSTRAINT language_language_set_2t_code_key UNIQUE (language_set_2t_code);


--
-- Name: language language_pkey; Type: CONSTRAINT; Schema: public; Owner: wordsmanipulator
--

ALTER TABLE ONLY public.language
    ADD CONSTRAINT language_pkey PRIMARY KEY (language_id);


--
-- Name: mood mood_pkey; Type: CONSTRAINT; Schema: public; Owner: wordsmanipulator
--

ALTER TABLE ONLY public.mood
    ADD CONSTRAINT mood_pkey PRIMARY KEY (mood_id);


--
-- Name: nouns nouns_pkey; Type: CONSTRAINT; Schema: public; Owner: wordsmanipulator
--

ALTER TABLE ONLY public.nouns
    ADD CONSTRAINT nouns_pkey PRIMARY KEY (noun_fk_word_id);


--
-- Name: sentence sentence_pkey; Type: CONSTRAINT; Schema: public; Owner: wordsmanipulator
--

ALTER TABLE ONLY public.sentence
    ADD CONSTRAINT sentence_pkey PRIMARY KEY (sentence_id);


--
-- Name: speech_part speech_part_pkey; Type: CONSTRAINT; Schema: public; Owner: wordsmanipulator
--

ALTER TABLE ONLY public.speech_part
    ADD CONSTRAINT speech_part_pkey PRIMARY KEY (speech_part_id);


--
-- Name: speech_part speech_part_speech_part_model_name_key; Type: CONSTRAINT; Schema: public; Owner: wordsmanipulator
--

ALTER TABLE ONLY public.speech_part
    ADD CONSTRAINT speech_part_speech_part_model_name_key UNIQUE (speech_part_model_name);


--
-- Name: speech_part speech_part_speech_part_name_key; Type: CONSTRAINT; Schema: public; Owner: wordsmanipulator
--

ALTER TABLE ONLY public.speech_part
    ADD CONSTRAINT speech_part_speech_part_name_key UNIQUE (speech_part_name);


--
-- Name: tense tense_pkey; Type: CONSTRAINT; Schema: public; Owner: wordsmanipulator
--

ALTER TABLE ONLY public.tense
    ADD CONSTRAINT tense_pkey PRIMARY KEY (tense_id);


--
-- Name: translation translation_pkey; Type: CONSTRAINT; Schema: public; Owner: wordsmanipulator
--

ALTER TABLE ONLY public.translation
    ADD CONSTRAINT translation_pkey PRIMARY KEY (translation_source_id, translation_target_id);


--
-- Name: verb_conjugation verb_conjugation_pkey; Type: CONSTRAINT; Schema: public; Owner: wordsmanipulator
--

ALTER TABLE ONLY public.verb_conjugation
    ADD CONSTRAINT verb_conjugation_pkey PRIMARY KEY (verb_conjugation_id);


--
-- Name: word word_pkey; Type: CONSTRAINT; Schema: public; Owner: wordsmanipulator
--

ALTER TABLE ONLY public.word
    ADD CONSTRAINT word_pkey PRIMARY KEY (word_id);


--
-- Name: word_sentence word_sentence_pkey; Type: CONSTRAINT; Schema: public; Owner: wordsmanipulator
--

ALTER TABLE ONLY public.word_sentence
    ADD CONSTRAINT word_sentence_pkey PRIMARY KEY (word_id, sentence_id);


--
-- Name: word word_unique_word_data; Type: CONSTRAINT; Schema: public; Owner: wordsmanipulator
--

ALTER TABLE ONLY public.word
    ADD CONSTRAINT word_unique_word_data UNIQUE (word_initial_form);


--
-- Name: article article_article_fk_language_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wordsmanipulator
--

ALTER TABLE ONLY public.article
    ADD CONSTRAINT article_article_fk_language_id_fkey FOREIGN KEY (article_fk_language_id) REFERENCES public.language(language_id);


--
-- Name: declension declension_declension_fk_word_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wordsmanipulator
--

ALTER TABLE ONLY public.declension
    ADD CONSTRAINT declension_declension_fk_word_id_fkey FOREIGN KEY (declension_fk_word_id) REFERENCES public.word(word_id);


--
-- Name: mood mood_mood_fk_language_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wordsmanipulator
--

ALTER TABLE ONLY public.mood
    ADD CONSTRAINT mood_mood_fk_language_id_fkey FOREIGN KEY (mood_fk_language_id) REFERENCES public.language(language_id);


--
-- Name: nouns nouns_noun_fk_article_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wordsmanipulator
--

ALTER TABLE ONLY public.nouns
    ADD CONSTRAINT nouns_noun_fk_article_id_fkey FOREIGN KEY (noun_fk_article_id) REFERENCES public.article(article_id);


--
-- Name: nouns nouns_noun_fk_word_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wordsmanipulator
--

ALTER TABLE ONLY public.nouns
    ADD CONSTRAINT nouns_noun_fk_word_id_fkey FOREIGN KEY (noun_fk_word_id) REFERENCES public.word(word_id);


--
-- Name: sentence sentence_sentence_source_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wordsmanipulator
--

ALTER TABLE ONLY public.sentence
    ADD CONSTRAINT sentence_sentence_source_id_fkey FOREIGN KEY (sentence_source_id) REFERENCES public.sentence(sentence_id);


--
-- Name: tense tense_tense_fk_language_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wordsmanipulator
--

ALTER TABLE ONLY public.tense
    ADD CONSTRAINT tense_tense_fk_language_id_fkey FOREIGN KEY (tense_fk_language_id) REFERENCES public.language(language_id);


--
-- Name: translation translation_translation_source_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wordsmanipulator
--

ALTER TABLE ONLY public.translation
    ADD CONSTRAINT translation_translation_source_id_fkey FOREIGN KEY (translation_source_id) REFERENCES public.word(word_id);


--
-- Name: translation translation_translation_target_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wordsmanipulator
--

ALTER TABLE ONLY public.translation
    ADD CONSTRAINT translation_translation_target_id_fkey FOREIGN KEY (translation_target_id) REFERENCES public.word(word_id);


--
-- Name: verb_conjugation verb_conjugation_verb_conjugation_fk_mood_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wordsmanipulator
--

ALTER TABLE ONLY public.verb_conjugation
    ADD CONSTRAINT verb_conjugation_verb_conjugation_fk_mood_id_fkey FOREIGN KEY (verb_conjugation_fk_mood_id) REFERENCES public.mood(mood_id);


--
-- Name: verb_conjugation verb_conjugation_verb_conjugation_fk_tense_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wordsmanipulator
--

ALTER TABLE ONLY public.verb_conjugation
    ADD CONSTRAINT verb_conjugation_verb_conjugation_fk_tense_id_fkey FOREIGN KEY (verb_conjugation_fk_tense_id) REFERENCES public.tense(tense_id);


--
-- Name: verb_conjugation verb_conjugation_verb_conjugation_fk_word_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wordsmanipulator
--

ALTER TABLE ONLY public.verb_conjugation
    ADD CONSTRAINT verb_conjugation_verb_conjugation_fk_word_id_fkey FOREIGN KEY (verb_conjugation_fk_word_id) REFERENCES public.word(word_id);


--
-- Name: word word_frequency_fk; Type: FK CONSTRAINT; Schema: public; Owner: wordsmanipulator
--

ALTER TABLE ONLY public.word
    ADD CONSTRAINT word_frequency_fk FOREIGN KEY (word_fk_frequency_id) REFERENCES public.frequency(frequency_id);


--
-- Name: word word_language_fk; Type: FK CONSTRAINT; Schema: public; Owner: wordsmanipulator
--

ALTER TABLE ONLY public.word
    ADD CONSTRAINT word_language_fk FOREIGN KEY (word_fk_language_id) REFERENCES public.language(language_id);


--
-- Name: word_sentence word_sentence_sentence_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wordsmanipulator
--

ALTER TABLE ONLY public.word_sentence
    ADD CONSTRAINT word_sentence_sentence_id_fkey FOREIGN KEY (sentence_id) REFERENCES public.sentence(sentence_id);


--
-- Name: word_sentence word_sentence_word_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wordsmanipulator
--

ALTER TABLE ONLY public.word_sentence
    ADD CONSTRAINT word_sentence_word_id_fkey FOREIGN KEY (word_id) REFERENCES public.word(word_id);


--
-- Name: word word_word_fk_speech_part_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wordsmanipulator
--

ALTER TABLE ONLY public.word
    ADD CONSTRAINT word_word_fk_speech_part_id_fkey FOREIGN KEY (word_fk_speech_part_id) REFERENCES public.speech_part(speech_part_id);


--
-- PostgreSQL database dump complete
--

