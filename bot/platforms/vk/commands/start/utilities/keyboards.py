from vkwave.bots.utils.keyboards import Keyboard

from bot.platforms.vk.utilities.types import CommandOfVK

from bot.utilities.types import Command


def make_login() -> str:
    make_login_keyboard: Keyboard = Keyboard(one_time=True, inline=True)
    
    make_login_keyboard.add_text_button(text=CommandOfVK.LOGIN_NEW_USER.value, payload={ "callback": Command.LOGIN.value })
    
    make_login_keyboard.add_row()
    make_login_keyboard.add_text_button(text=CommandOfVK.LOGIN_VIA_TELEGRAM.value, payload={ "callback": Command.LOGIN_PLATFORM.value })
    
    return make_login_keyboard.get_keyboard()
