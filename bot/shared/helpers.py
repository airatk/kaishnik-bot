from aiogram import executor

from bot import bot
from bot import dispatcher
from bot import keys


# Used to show "Loading..." notification on the top in a cleverer way
def top_notification(callback_handler):
    async def wrapper(callback):
        await callback_handler(callback)
        
        await bot.answer_callback_query(callback_query_id=callback.id,cache_time=0)

    return wrapper


# Launcher
def main():
    executor.start_polling(dispatcher)
