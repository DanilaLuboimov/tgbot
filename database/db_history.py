from .connection_to_db import connect


def get_history_result(user_id: int, search_id: int) -> list:
    connection = connect()

    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            SELECT hotel_url, hotel_name FROM results r
            JOIN search_query s ON r.fk_search_id = s.id
            JOIN users u ON s.fk_user_id = u.user_id
            WHERE u.user_id = {user_id} and s.id = {search_id}
            """
        )

        db_list = cursor.fetchall()

        return db_list


def get_search_query(user_id: int) -> list:
    connection = connect()

    with connection.cursor() as cursor:
        cursor.execute(
            f"""
                SELECT command, date_time, s.id FROM search_query s
                JOIN users u ON s.fk_user_id = u.user_id
                WHERE u.user_id = {user_id}
                """
        )

        db_list = cursor.fetchall()

        return db_list
