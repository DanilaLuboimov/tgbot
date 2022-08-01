from loader import bot
from states.user_information import UserInfoState
from telebot.types import Message


@bot.message_handler(commands=["highprice"])
# @ex_wrapper
def highprice(message: Message) -> None:
    bot.delete_state(user_id=message.from_user.id, chat_id=message.chat.id)

    answer = f"В какой <b>город</b> отправляемся?"

    bot.set_state(user_id=message.from_user.id, state=UserInfoState.city_name,
                  chat_id=message.chat.id)
    bot.send_message(chat_id=message.chat.id, text=answer, parse_mode="html")
    with bot.retrieve_data(user_id=message.from_user.id,
                           chat_id=message.chat.id) as data:
        data["user_id"] = message.from_user.id
        data["user_filter"] = "PRICE_HIGHEST_FIRST"
        data["price_min"] = "0"
        data["price_max"] = "5000"
        data["command"] = message.text
        data["date"] = message.date
