from loader import bot
from telebot.types import Message
from keyboards.reply.default_keyboard import user_keyboard
from utils.info import info


@bot.message_handler(commands=["help"])
def help_info(message: Message) -> None:
    answer = info()
    bot.send_message(message.chat.id, answer, parse_mode='html',
                     reply_markup=user_keyboard())
