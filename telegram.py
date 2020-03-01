import fire
import sys
import re
from telebot import TeleBot, apihelper
import exapi


ex = exapi.ExApi('USD')


def check_string(data: str) -> int:
    result = "".join(re.findall(r'\d+', data))
    return int(result)


def dict_to_str(data: dict) -> str:
    result = str()
    for k, v in data.items():
        result += f"{k}: {v}\n"
    return result


def telgram(token: str, proxy_addr: str = "", proxy_port: str = ""):
    if token:
        bot = TeleBot(token)
    else:
        sys.exit(0)

    apihelper.CONNECT_TIMEOUT = 10

    if proxy_addr and proxy_port:
        apihelper.proxy = {'https': f'socks5h://{proxy_addr}:{proxy_port}'}

    @bot.message_handler(commands=['list', 'lst'])
    def send_welcome(message):
        if ex.check_time(10):
            result = ex.local_rates()
        else:
            result = ex.get_rates()
        bot.reply_to(message, dict_to_str(result))

    @bot.message_handler(commands=['exchange'])
    def echo_all(message):
        val = check_string(message.text)
        result = ex.convert_usd_to_cad(val)
        bot.reply_to(message, str(result))

    @bot.message_handler(commands=['history'])
    def send_welcome(message):
        data = ex.get_statistic(7)
        if data:
            with open('./bar_chart.svg', 'rb') as chart:
                bot.send_photo(message, chart)
        else:
            bot.reply_to(message, "No exchange rate data is available for the selected currency")

    bot.polling()


if __name__ == '__main__':
    fire.Fire(telgram)
