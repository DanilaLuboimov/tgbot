from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def hotel_website(hotel_name: str, hotel_id: str, check_in: str,
                  check_out: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()

    hotel_site = InlineKeyboardButton(text=hotel_name,
                                      url=f"https://www.hotels.com/ho{hotel_id}/?q-check-in={check_in}&q-check-out={check_out}&q-rooms=1&q-room-0-adults=1&q-room-0-children=0&f-hotel-id={hotel_id}")

    markup.add(hotel_site)

    return markup
