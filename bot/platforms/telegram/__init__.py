from typing import Dict

from asyncio import get_event_loop

from aiogram import Bot
from aiogram import Dispatcher

from bot.models.users import Users

from bot.utilities.constants import KEYS
from bot.utilities.types import Guard
from bot.utilities.types import State


telegram_bot: Bot = Bot(token=KEYS.TELEGRAM_TOKEN)
dispatcher: Dispatcher = Dispatcher(bot=telegram_bot, loop=get_event_loop())

guards: Dict[int, Guard] = { user.telegram_id: Guard() for user in Users.select(Users.telegram_id) }
states: Dict[int, State] = { user.telegram_id: State() for user in Users.select(Users.telegram_id) }


from bot.platforms.telegram import commands
