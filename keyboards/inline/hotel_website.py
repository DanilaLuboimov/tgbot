from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def hotel_website(hotels: list) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()

    for button in hotels:
        hotel_url = button[0]
        hotel_name = button[1]

        hotel_site = InlineKeyboardButton(text=hotel_name, url=hotel_url)

        markup.add(hotel_site)

    return markup
