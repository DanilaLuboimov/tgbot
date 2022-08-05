from loader import headers
from requests.exceptions import ReadTimeout

import requests
import json


def get_response(url: str, querystring: dict) -> dict:
    """
    Основная функция для отправки запросов к api.
    Формирует json файл и возвращает его.

    :param url: url запроса.
    :type url: str
    :param querystring: параметры запроса
    :type querystring: dict
    :return: list
    """
    try:
        response = requests.get(url=url, headers=headers,
                                params=querystring, timeout=17)
    except ReadTimeout:
        print("Время запроса к api истекло")
    else:
        if response.status_code == requests.codes.ok:
            data = json.loads(response.text)
            return data
