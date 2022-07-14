from loader import bot
from telebot.types import Message
from keyboards.reply.default_keyboard import user_keyboard


# Еще не готово
@bot.message_handler(commands=["history"])
# @ex_wrapper
def history(message: Message) -> None:
    answer = f"<b>История поиска отелей</b>"
    bot.send_message(message.chat.id, answer, parse_mode='html',
                     reply_markup=user_keyboard())
