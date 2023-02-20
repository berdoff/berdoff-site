import telebot;
from config import token_tg
import telebot;

bot = telebot.TeleBot(token_tg);

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/id_be":
        bot.send_message(message.chat.id,"Я тебе ебало сломаю")

bot.polling(none_stop=True, interval=0)