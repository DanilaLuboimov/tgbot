from .connection_to_db import connect


def get_tables() -> None:
    connection = connect()
    with connection.cursor() as cursor:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS public.users
            (
                id integer NOT NULL DEFAULT nextval('users_id_seq'::regclass),
                user_id integer NOT NULL,
                CONSTRAINT users_pkey PRIMARY KEY (user_id)
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS public.search_query
            (
                id integer NOT NULL DEFAULT nextval('search_query_id_seq'::regclass),
                command text COLLATE pg_catalog."default" NOT NULL,
                date_time timestamp without time zone NOT NULL,
                fk_user_id integer NOT NULL,
                CONSTRAINT search_query_pkey PRIMARY KEY (id),
                CONSTRAINT search_query_fk_user_id_fkey FOREIGN KEY (fk_user_id)
                    REFERENCES public.users (user_id) MATCH SIMPLE
                    ON UPDATE NO ACTION
                    ON DELETE NO ACTION
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS public.results
            (
                id integer NOT NULL DEFAULT nextval('result_id_seq'::regclass),
                hotel_url text COLLATE pg_catalog."default",
                fk_search_id integer NOT NULL,
                hotel_name text COLLATE pg_catalog."default",
                CONSTRAINT result_pkey PRIMARY KEY (id),
                CONSTRAINT result_fk_serch_id_fkey FOREIGN KEY (fk_search_id)
                    REFERENCES public.search_query (id) MATCH SIMPLE
                    ON UPDATE NO ACTION
                    ON DELETE NO ACTION
            )
            """
        )
