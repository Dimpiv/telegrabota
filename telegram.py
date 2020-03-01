import fire
import sys
from telebot import TeleBot, apihelper
import exapi


def telgram(token: str):
    if token:
        bot = TeleBot(token)
    else:
        sys.exit(0)

    apihelper.CONNECT_TIMEOUT = 10
    # apihelper.proxy = {'https': 'socks5h://139.59.169.246:1080'}

    @bot.message_handler(commands=['list', 'lst'])
    def send_welcome(message):
        bot.reply_to(message, "Test!")

    @bot.message_handler(commands=['history'])
    def send_welcome(message):
        bot.reply_to(message, "Test!")

    @bot.message_handler(commands=['exchange'])
    def echo_all(message):
        bot.reply_to(message, message.text)

    bot.polling()


if __name__ == '__main__':
    fire.Fire(telgram)
