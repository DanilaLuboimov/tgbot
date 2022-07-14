from loader import bot
from telebot.types import Message
from keyboards.reply.default_keyboard import user_keyboard


@bot.message_handler(content_types=["text"])
# @ex_wrapper
def another_message(message: Message) -> None:
    answer = "<b>Я тебя не понимаю, воспользуйся <u>/help</u></b>"
    bot.send_message(chat_id=message.chat.id, text=answer, parse_mode='html',
                     reply_markup=user_keyboard())
