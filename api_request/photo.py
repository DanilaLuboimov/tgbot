from telebot.types import InputMediaPhoto
from re import sub
from .general_request import get_response


def get_photos(hotel_id: str, count: int) -> dict:
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
    querystring = {"id": hotel_id}

    photo_json = get_response(url=url, querystring=querystring)

    photo_list = list()

    for p in photo_json["hotelImages"][:count:]:
        photo = sub(r"{size}", r"z", p["baseUrl"])
        hotel_photo = InputMediaPhoto(photo)
        photo_list.append(hotel_photo)

    return photo_list
