from typing import List
from typing import Tuple

from vkwave.bots import Keyboard

from bot.platforms.vk.utilities.types import CommandOfVK
from bot.platforms.vk.utilities.keyboards import cancel_button

from bot.utilities.types import Command


def login_way_chooser(is_old: bool) -> str:
    setup_way_chooser_keyboard: Keyboard = Keyboard(one_time=True, inline=True)
    
    setup_way_chooser_keyboard.add_text_button(text=CommandOfVK.LOGIN_BB.value, payload={ "callback": Command.LOGIN_BB.value })
    
    setup_way_chooser_keyboard.add_row()
    setup_way_chooser_keyboard.add_text_button(text=CommandOfVK.LOGIN_COMPACT.value, payload={ "callback": Command.LOGIN_COMPACT.value })    
    
    if is_old:
        setup_way_chooser_keyboard.add_row()
        setup_way_chooser_keyboard.add_text_button(**cancel_button())
    
    return setup_way_chooser_keyboard.get_keyboard()


def againer() -> str:
    againer_keyboard: Keyboard = Keyboard(one_time=True, inline=True)
    
    againer_keyboard.add_text_button(text=CommandOfVK.CONTINUE.value, payload={ "callback": Command.LOGIN_COMPACT.value })
    
    againer_keyboard.add_row()
    againer_keyboard.add_text_button(**cancel_button())
    
    return againer_keyboard.get_keyboard()
