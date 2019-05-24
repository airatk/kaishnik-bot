from telebot import TeleBot
from telebot import apihelper

from bot.constants import TOKEN

from bot.helpers import load_from
from bot.helpers import Metrics

from sys import argv

from random import choice


# Because Telegram is officially blocked in Russia, that's why
apihelper.proxy = { "https": "socks5://163.172.152.192:1080" }


# Main data setup
kbot = TeleBot(TOKEN, threaded=False)
students = load_from(filename="data/users")
metrics = Metrics()


# Used to show "Loading..." notification on the top in a cleverer way
def top_notification(callback_handler):
    def wrapper(callback):
        callback_handler(callback)
        
        apihelper.answer_callback_query(
            token=TOKEN,
            callback_query_id=callback.id,
            cache_time=0
        )
    
    return wrapper


# Polling launcher
def main():
    if len(argv) == 1:
        print("Launched in test mode")
        kbot.polling()
    elif argv[1] == "i":
        print("Launched in infinity mode")
        kbot.infinity_polling(True)
    else:
        print(
            "\n  Incorrect options!\n\n"
              "- python3 startup.py     - to launch in test mode\n"
              "- python3 startup.py i   - to launch in infinity mode\n"
        )


# All the commands & other stuff handlers
from bot import handlers
