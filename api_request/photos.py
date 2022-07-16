from loader import bot
from loader import headers
from telebot.types import Message

import requests
import json


def get_photos(hotel_id: str) -> dict:
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"

    querystring = {"id": hotel_id}

    response = requests.get(url=url, headers=headers,
                            params=querystring)
    photo_json = json.loads(response.text)

    return photo_json
