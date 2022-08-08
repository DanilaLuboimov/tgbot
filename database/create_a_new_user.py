from .connection_to_db import connect


def new_user(user_id: int) -> bool:
    """
    Функция проверяет наличие пользователя в базе данных.
    Если запись о нем отсутствует, создает новую.

    :param user_id: id пользователя
    :type user_id: int
    :return: bool
    """
    connection = connect()

    with connection.cursor() as cursor:
        cursor.execute(
            """SELECT user_id FROM users"""
        )
        db_dict = cursor.fetchall()

        for elem_tuple in db_dict:
            if user_id == elem_tuple[0]:
                return False

        cursor.execute(
            f"""INSERT INTO users (user_id) VALUES ('{user_id}')"""
        )
        return True
