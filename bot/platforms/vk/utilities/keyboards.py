from typing import Dict

from vkwave.bots.utils.keyboards import Keyboard
from vkwave.bots.utils.keyboards import ButtonColor

from bot.platforms.vk.utilities.types import CommandsOfVK

from bot.utilities.types import Commands


def make_login() -> str:
    make_login_keyboard: Keyboard = Keyboard(one_time=True, inline=True)
    
    make_login_keyboard.add_text_button(text=CommandsOfVK.LOGIN_NEW_USER.value, payload={ "callback": Commands.LOGIN.value })
    
    make_login_keyboard.add_row()
    make_login_keyboard.add_text_button(text=CommandsOfVK.LOGIN_VIA_TELEGRAM.value, payload={ "callback": Commands.LOGIN_PLATFORM.value })
    
    return make_login_keyboard.get_keyboard()

def make_start() -> str:
    make_start_keyboard: Keyboard = Keyboard(one_time=True)
    
    make_start_keyboard.add_text_button(text=CommandsOfVK.START.value)

    return make_start_keyboard.get_keyboard()


def menu_button() -> Dict[str, str]:
    return dict(text=CommandsOfVK.MENU.value, color=ButtonColor.SECONDARY)

def to_menu() -> str:
    to_menu_keyboard: Keyboard = Keyboard(one_time=True, inline=True)

    to_menu_keyboard.add_text_button(**menu_button())

    return to_menu_keyboard.get_keyboard()

def menu() -> str:
    menu_keyboard: Keyboard = Keyboard(one_time=True, inline=True)
    
    menu_keyboard.add_text_button(text=CommandsOfVK.CLASSES.value)
    # menu_keyboard.add_text_button(text=CommandsOfVK.SCORE.value)

    menu_keyboard.add_row()
    menu_keyboard.add_text_button(text=CommandsOfVK.LECTURERS.value)

    menu_keyboard.add_row()
    menu_keyboard.add_text_button(text=CommandsOfVK.EXAMS.value)

    menu_keyboard.add_row()
    menu_keyboard.add_text_button(text=CommandsOfVK.NOTES.value)
    menu_keyboard.add_text_button(text=CommandsOfVK.WEEK.value)

    menu_keyboard.add_row()
    menu_keyboard.add_text_button(text=CommandsOfVK.LOCATIONS.value)
    menu_keyboard.add_text_button(text=CommandsOfVK.BRS.value)

    menu_keyboard.add_row()
    menu_keyboard.add_text_button(text=CommandsOfVK.MORE.value, color=ButtonColor.SECONDARY)
    
    return menu_keyboard.get_keyboard()

def additional_menu() -> str:
    additional_menu_keyboard: Keyboard = Keyboard(one_time=True, inline=True)
    
    additional_menu_keyboard.add_text_button(text=CommandsOfVK.SETTINGS.value)
    
    additional_menu_keyboard.add_row()
    additional_menu_keyboard.add_text_button(text=CommandsOfVK.HELP.value)

    additional_menu_keyboard.add_row()
    additional_menu_keyboard.add_text_button(text=CommandsOfVK.DONATE.value, color=ButtonColor.SECONDARY)

    additional_menu_keyboard.add_row()
    additional_menu_keyboard.add_text_button(**menu_button())

    return additional_menu_keyboard.get_keyboard()


def cancel_button() -> Dict[str, str]:
    return dict(text=CommandsOfVK.CANCEL.value, color=ButtonColor.SECONDARY, payload={ "callback": Commands.CANCEL.value })

def canceler() -> str:
    canceler_keyboard: Keyboard = Keyboard(one_time=True, inline=True)
    
    canceler_keyboard.add_text_button(**cancel_button())
    
    return canceler_keyboard.get_keyboard()
