from typing import Dict

from vkwave.bots.utils.keyboards import Keyboard
from vkwave.bots.utils.keyboards import ButtonColor

from bot.platforms.vk.utilities.types import CommandOfVK

from bot.utilities.types import Command


def menu_button() -> Dict[str, str]:
    return dict(text=CommandOfVK.MENU.value, color=ButtonColor.SECONDARY)

def to_menu() -> str:
    to_menu_keyboard: Keyboard = Keyboard(one_time=True, inline=True)

    to_menu_keyboard.add_text_button(**menu_button())

    return to_menu_keyboard.get_keyboard()

def menu() -> str:
    menu_keyboard: Keyboard = Keyboard(one_time=True, inline=True)
    
    menu_keyboard.add_text_button(text=CommandOfVK.CLASSES.value)
    menu_keyboard.add_text_button(text=CommandOfVK.SCORE.value)

    menu_keyboard.add_row()
    menu_keyboard.add_text_button(text=CommandOfVK.LECTURERS.value)

    menu_keyboard.add_row()
    menu_keyboard.add_text_button(text=CommandOfVK.EXAMS.value)

    menu_keyboard.add_row()
    menu_keyboard.add_text_button(text=CommandOfVK.NOTES.value)
    menu_keyboard.add_text_button(text=CommandOfVK.WEEK.value)

    menu_keyboard.add_row()
    menu_keyboard.add_text_button(text=CommandOfVK.LOCATIONS.value)
    menu_keyboard.add_text_button(text=CommandOfVK.BRS.value)

    menu_keyboard.add_row()
    menu_keyboard.add_text_button(text=CommandOfVK.MORE.value, color=ButtonColor.SECONDARY)
    
    return menu_keyboard.get_keyboard()

def additional_menu() -> str:
    additional_menu_keyboard: Keyboard = Keyboard(one_time=True, inline=True)
    
    additional_menu_keyboard.add_text_button(text=CommandOfVK.SETTINGS.value)
    
    additional_menu_keyboard.add_row()
    additional_menu_keyboard.add_text_button(text=CommandOfVK.HELP.value)

    additional_menu_keyboard.add_row()
    additional_menu_keyboard.add_text_button(text=CommandOfVK.DONATE.value, color=ButtonColor.SECONDARY)

    additional_menu_keyboard.add_row()
    additional_menu_keyboard.add_text_button(**menu_button())

    return additional_menu_keyboard.get_keyboard()


def cancel_button() -> Dict[str, str]:
    return dict(text=CommandOfVK.CANCEL.value, color=ButtonColor.SECONDARY, payload={ "callback": Command.CANCEL.value })

def canceler() -> str:
    canceler_keyboard: Keyboard = Keyboard(one_time=True, inline=True)
    
    canceler_keyboard.add_text_button(**cancel_button())
    
    return canceler_keyboard.get_keyboard()
