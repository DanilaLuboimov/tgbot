from loader import bot
from telebot.types import Message
from keyboards.reply.default_keyboard import user_keyboard
from utils.info import info
from database.create_a_new_user import new_user


@bot.message_handler(commands=["start"])
# @ex_wrapper
def start(message: Message) -> None:
    if new_user(message.from_user.id):
        answer = f"Привет, {message.from_user.first_name}! " \
             f"Вот что я умею:\n{info()}"
    else:
        answer = f"Вы уже зарегистрированы! " \
             f"Вот что я умею:\n{info()}"

    bot.send_message(chat_id=message.chat.id, text=answer, parse_mode='html',
                     reply_markup=user_keyboard())
