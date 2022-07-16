from loader import headers
from deep_translator import GoogleTranslator

import requests
import json


def get_city(message_text: str) -> tuple:
    url = "https://hotels4.p.rapidapi.com/locations/v2/search"

    alphabet_ru = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    name_city = message_text

    for letter in message_text.lower():
        if letter in alphabet_ru:
            name_city = GoogleTranslator(source='auto', target='en').translate(
                message_text.title())
            break

    querystring = {"query": name_city.lower(), "locale": "en_US",
                   "currency": "USD"}
    response = requests.get(url=url, headers=headers,
                            params=querystring, timeout=15)

    if response.status_code == requests.codes.ok:
        data = json.loads(response.text)

        for i in data["suggestions"]:
            if len(i["entities"]) > 0:
                city_id = i["entities"][0]["destinationId"]
                city_name = i["entities"][0]["name"]
                break

    return city_id, city_name
