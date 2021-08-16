from logging import basicConfig
from logging import NOTSET

from aiogram import executor

from bot.platforms.telegram import dispatcher
from bot.platforms.vk import vk_bot

from bot.utilities.database.helpers import setup_database_tables


if __name__ == "__main__":
    # Logger setup
    basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=NOTSET)
    
    # Database setup
    setup_database_tables()
    
    # Launching bot on all platforms
    dispatcher.loop.create_task(vk_bot.run())
    executor.start_polling(dispatcher=dispatcher)
