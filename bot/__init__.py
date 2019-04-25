from telebot import TeleBot
from telebot import apihelper

from bot.constants import TOKEN

from bot.helpers import load_from
from bot.helpers import Metrics

from sys import argv

# Because Telegram is officially blocked in Russia, that's why
apihelper.proxy = { "https": "socks5://163.172.152.192:1080" }

# Used to show "Loading..." notification on the top in a cleverer way
on_callback_query = lambda id: apihelper.answer_callback_query(token=TOKEN, callback_query_id=id, cache_time=0)

kaishnik = TeleBot(TOKEN, threaded=False)
students = load_from(filename="data/users")
metrics = Metrics()

from bot import handlers

def main():
    if len(argv) == 1:
        print("Launched in test mode")
        kaishnik.polling()
    else:
        print("Launched in infinite mode")
        kaishnik.infinity_polling(True)
