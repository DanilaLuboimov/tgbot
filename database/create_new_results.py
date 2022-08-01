from .connection_to_db import connect


def new_results(search_id: int, hotel_url: None | str = None,
                hotel_name: str | None = None) -> None:
    hotel_name = hotel_name.replace("'", "''")

    connection = connect()
    with connection.cursor() as cursor:
        if hotel_url is not None:
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
