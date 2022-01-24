# Logger setup
from logging import basicConfig
from logging import NOTSET

basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=NOTSET, encoding="utf-8")


# Database setup
from bot.utilities.database.helpers import setup_database_tables

setup_database_tables()


# Launching bot on all platforms
from aiogram import executor

from bot.platforms.telegram import dispatcher
from bot.platforms.vk import vk_bot

dispatcher.loop.create_task(vk_bot.run())
executor.start_polling(dispatcher=dispatcher)
