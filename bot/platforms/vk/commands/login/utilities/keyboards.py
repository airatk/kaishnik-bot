from typing import List
from typing import Tuple

from vkwave.bots import Keyboard

from bot.platforms.vk.utilities.types import CommandsOfVK
from bot.platforms.vk.utilities.keyboards import cancel_button

from bot.utilities.types import Commands
from bot.utilities.api.constants import INSTITUTES


def login_way_chooser(is_old: bool) -> str:
    setup_way_chooser_keyboard: Keyboard = Keyboard(one_time=True, inline=True)
    
    setup_way_chooser_keyboard.add_text_button(text=CommandsOfVK.LOGIN_BB.value, payload={ "callback": Commands.LOGIN_BB.value })
    
    setup_way_chooser_keyboard.add_row()
    setup_way_chooser_keyboard.add_text_button(text=CommandsOfVK.LOGIN_COMPACT.value, payload={ "callback": Commands.LOGIN_COMPACT.value })    
    
    if is_old:
        setup_way_chooser_keyboard.add_row()
        setup_way_chooser_keyboard.add_text_button(**cancel_button())
    
    return setup_way_chooser_keyboard.get_keyboard()


def institute_setter() -> str:
    institute_setter_keyboard: Keyboard = Keyboard(one_time=True, inline=True)

    for (institute_id, institute) in INSTITUTES.items():
        institute_setter_keyboard.add_text_button(text=institute, payload={ 
            "callback": Commands.LOGIN_SET_INSTITUTE.value,
            "institute_id": institute_id
        })
        institute_setter_keyboard.add_row()

    institute_setter_keyboard.add_text_button(**cancel_button())
    
    return institute_setter_keyboard.get_keyboard()

def year_setter(years: List[Tuple[str, str]]) -> str:
    year_setter_keyboard: Keyboard = Keyboard(one_time=True, inline=True)

    for (year, _) in years:
        year_setter_keyboard.add_text_button(text=year, payload={
            "callback": Commands.LOGIN_SET_YEAR.value, 
            "year": year
        })
        year_setter_keyboard.add_row()

    year_setter_keyboard.add_text_button(**cancel_button())
    
    return year_setter_keyboard.get_keyboard()

def group_setter(groups: List[Tuple[str, str]]) -> str:
    group_setter_keyboard: Keyboard = Keyboard(one_time=True, inline=True)
    
    for (group, group_id) in groups:
        group_setter_keyboard.add_text_button(text=group, payload={
            "callback": Commands.LOGIN_SET_GROUP.value, 
            "group": group,
            "group_id": group_id
        })
        group_setter_keyboard.add_row()
    
    group_setter_keyboard.add_text_button(**cancel_button())

    return group_setter_keyboard.get_keyboard()

def name_setter(names: List[Tuple[str, str]]) -> str:
    name_setter_keyboard: Keyboard = Keyboard(one_time=True, inline=True)
    
    for (name_id, name) in names:
        name_setter_keyboard.add_text_button(text=name, payload={
            "callback": Commands.LOGIN_SET_NAME.value, 
            "name_id": name_id
        })
        name_setter_keyboard.add_row()
    
    name_setter_keyboard.add_text_button(**cancel_button())
    
    return name_setter_keyboard.get_keyboard()


def againer() -> str:
    againer_keyboard: Keyboard = Keyboard(one_time=True, inline=True)
    
    againer_keyboard.add_text_button(text=CommandsOfVK.CONTINUE.value, payload={ "callback": Commands.LOGIN_COMPACT.value })
    
    againer_keyboard.add_row()
    againer_keyboard.add_text_button(**cancel_button())
    
    return againer_keyboard.get_keyboard()
