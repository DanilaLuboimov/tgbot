from deep_translator import GoogleTranslator
from .general_request import get_response


def get_city(message_text: str) -> tuple:
    """
    Функция может принимать сообщение от пользователя, как на русском языке,
    так и на английском. В случае с русским языком программа переводит текст
    на английский. После чего отправляет запрос к api и если запрос успешный
    получает id города. Функция возвращает название города и его id.

    :param message_text: сообщение от пользователя.
    :type message_text: str
    :return: tuple
    """
    alphabet_ru = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    name_city = message_text

    for letter in message_text.lower():
        if letter in alphabet_ru:
            name_city = GoogleTranslator(source='auto', target='en').translate(
                message_text.title())
            break

    url = "https://hotels4.p.rapidapi.com/locations/v2/search"
    querystring = {"query": name_city.lower(), "locale": "en_US",
                   "currency": "USD"}

    data = get_response(url=url, querystring=querystring)

    for i in data["suggestions"]:
        if len(i["entities"]) > 0:
            city_id = i["entities"][0]["destinationId"]
            city_name = i["entities"][0]["name"]
            return city_id, city_name
