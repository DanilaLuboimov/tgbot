from loader import bot
from loader import headers
from telebot.types import Message

import requests
import json


def get_properties(message: Message) -> dict:
    url = "https://hotels4.p.rapidapi.com/properties/list"

    with bot.retrieve_data(user_id=message.from_user.id,
                           chat_id=message.chat.id) as data:
        city_id = data["city_id"]
        check_in = data["check_in"]
        check_out = data["check_out"]
        price_min = data["price_min"]
        price_max = data["price_max"]
        user_filter = data["user_filter"]

    querystring = {
        "destinationId": city_id,
        "pageNumber": "1",
        "pageSize": "25",
        "checkIn": check_in,
        "checkOut": check_out,
        "adults1": "1",
        "priceMin": price_min,
        "priceMax": price_max,
        "sortOrder": user_filter,
        "locale": "en_US",
        "currency": "USD",
        "accommodationIds": "12,1"
    }

    response = requests.get(url=url, headers=headers,
                            params=querystring, timeout=15)

    if response.status_code == requests.codes.ok:

        hotels_j = json.loads(response.text)

    return hotels_j, data
