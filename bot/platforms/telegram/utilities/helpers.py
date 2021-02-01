from typing import Callable

from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import InvalidQueryID


# Used to show "Loading..." notification on the top in a cleverer way
def top_notification(callback_handler: Callable):
    async def wrapper(callback: CallbackQuery):
        await callback_handler(callback)
        
        try:
            await callback.answer(cache_time=0)
        except InvalidQueryID:
            pass
    
    return wrapper
