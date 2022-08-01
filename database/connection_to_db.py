from loader import host, user, password, db_name, port

import psycopg2


def connect():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name,
            port=port
        )
        connection.autocommit = True
    except Exception as _ex:
        print(f"[INFO] Error while working with PostgreSQL {_ex}")
    else:
        return connection
