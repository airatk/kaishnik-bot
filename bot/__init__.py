from telebot import TeleBot
from telebot import apihelper

from bot.shared.data.helpers import load_data
from bot.shared.data.constants import USERS_FILE
from bot.shared.data.constants import KEYS_FILE
from bot.shared.metrics import Metrics

from config import Config


# Bypassing the lockout of Russian government
apihelper.proxy = { "https": "socks5://163.172.152.192:1080" }


# Initialising the bot components
keys = Config(open(KEYS_FILE))
bot = TeleBot(token=keys.TOKEN, threaded=False)
students = load_data(file=USERS_FILE)
metrics = Metrics()


# Importing all the commands
from bot import commands
