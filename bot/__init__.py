from aiogram import Bot
from aiogram import Dispatcher

from bot.shared.constants import PROXY
from bot.shared.api.student import Student
from bot.shared.data.helpers import load_data
from bot.shared.data.constants import USERS_FILE
from bot.shared.data.constants import KEYS_FILE
from bot.shared.metrics import Metrics

from config import Config
from logging import basicConfig
from logging import NOTSET


# Logger setup
basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=NOTSET)


# Initialising the bot components
with open(KEYS_FILE) as keys_file:
    keys: Config = Config(keys_file)

bot: Bot = Bot(token=keys.TOKEN, proxy=PROXY)
dispatcher: Dispatcher = Dispatcher(bot)

students: {int: Student} = load_data(file=USERS_FILE)
metrics: Metrics = Metrics()


# Importing all the commands
from bot import commands
