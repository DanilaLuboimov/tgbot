from .connection_to_db import connect


def new_results(search_id: int, hotel_url: str | None = None,
                hotel_name: str | None = None) -> None:
    """
    Запись результатов в базу данных,
    полученных по запросу пользователя.

    :param search_id: id запроса
    :type search_id: int
    :param hotel_url: url отеля
    :type hotel_url: [str, None]
    :param hotel_name: название отеля
    :type hotel_name: [str, None]
    :return: None
    """
    connection = connect()

    with connection.cursor() as cursor:
        if hotel_url is not None:
            hotel_name = hotel_name.replace("'", "''")
            cursor.execute(
                f"""
                INSERT INTO results (hotel_url, fk_search_id, hotel_name)
                VALUES
                ('{hotel_url}', '{search_id}', '{hotel_name}')
                """
            )
        else:
            cursor.execute(
                f"""
                INSERT INTO results (fk_search_id)
                VALUES
                ('{search_id}')
                """
            )
