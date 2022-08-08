from .connection_to_db import connect
from datetime import datetime


def new_search_query(command: str, date_time: str, fk_user_id: int) -> int:
    """
    Функция создает новую запись о запросе пользователя

    :param command: команда выбранная пользователем
    :type command: str
    :param date_time: дата и время выдачи результатов пользователю
    :type date_time: str
    :param fk_user_id: id пользователя
    :type fk_user_id: int
    :return: возвращает id запроса из базы данных (int)
    """
    connection = connect()

    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            INSERT INTO search_query (command, date_time, fk_user_id) 
            VALUES 
            ('{command}', '{datetime.fromtimestamp(date_time)}', '{fk_user_id}')
            """
        )
        cursor.execute(
            f"""SELECT id FROM search_query WHERE fk_user_id = {fk_user_id}"""
        )

        db_list = cursor.fetchall()

        return db_list[-1][0]