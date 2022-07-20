from loader import bot
from telebot.types import Message
from keyboards.reply.default_keyboard import user_keyboard
from utils.info import info


@bot.message_handler(commands=["start"])
# @ex_wrapper
def start(message: Message) -> None:
    answer = f"Привет, {message.from_user.first_name}! " \
             f"Вот что я умею:\n{info()}"
    bot.send_message(chat_id=message.chat.id, text=answer, parse_mode='html',
                     reply_markup=user_keyboard())
