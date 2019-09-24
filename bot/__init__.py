from telebot import TeleBot
from telebot import apihelper

from bot.shared.constants import TOKEN
from bot.shared.data.helpers import load_data
from bot.shared.data.constants import USERS_FILE
from bot.shared.metrics import Metrics


# Bypassing the lockout of Russian government
apihelper.proxy = { "https": "socks5://163.172.152.192:1080" }


# Initialising the bot components
bot = TeleBot(token=TOKEN)
students = load_data(file=USERS_FILE)
metrics = Metrics()


# Importing all the commands
from bot import commands
