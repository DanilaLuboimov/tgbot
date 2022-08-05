from loader import bot
from telebot.types import Message
from keyboards.reply.default_keyboard import user_keyboard
from utils.logging import ex_log


@bot.message_handler(func=lambda message: True,
                     content_types=['audio', 'photo', 'voice', 'video',
                                    'document',
                                    'text', 'location', 'contact', 'sticker'])
@ex_log
def another_message(message: Message) -> None:
    """
    Функция отправляет пользователю сообщение о неизвестной команде

    :param message: Сообщение от пользователя
    :type message: Message
    :return: None
    """
    answer = "<b>Я тебя не понимаю, воспользуйся <u>/help</u></b>"

    bot.send_message(chat_id=message.chat.id, text=answer, parse_mode='html',
                     reply_markup=user_keyboard())
