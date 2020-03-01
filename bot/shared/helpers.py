from aiogram.types import CallbackQuery

from typing import Callable


# Used to show "Loading..." notification on the top in a cleverer way
def top_notification(callback_handler: Callable):
    async def wrapper(callback: CallbackQuery):
        await callback_handler(callback)
        
        await callback.answer(cache_time=0)
    
    return wrapper
