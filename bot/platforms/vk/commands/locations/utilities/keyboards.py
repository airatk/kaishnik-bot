from vkwave.bots.utils.keyboards import Keyboard

from bot.platforms.vk.utilities.keyboards import menu_button

from bot.utilities.api.constants import BUILDINGS
from bot.utilities.api.constants import LIBRARIES
from bot.utilities.api.constants import SPORTSCOMPLEX
from bot.utilities.api.constants import DORMS
from bot.utilities.api.types import LocationType


def location_type_chooser() -> str:
    location_type_chooser_keyboard: Keyboard = Keyboard(one_time=True, inline=True)
    
    location_type_chooser_keyboard.add_text_button(text="Учебные здания", payload={ "callback": LocationType.BUILDING.value })
    
    location_type_chooser_keyboard.add_row()
    location_type_chooser_keyboard.add_text_button(text="Библиотеки", payload={ "callback": LocationType.LIBRARY.value })
    
    location_type_chooser_keyboard.add_row()
    location_type_chooser_keyboard.add_text_button(text="СК Олимп", payload={ "callback": LocationType.SPORTSCOMPLEX.value })
    
    location_type_chooser_keyboard.add_row()
    location_type_chooser_keyboard.add_text_button(text="Общежития", payload={ "callback": LocationType.DORM.value })
    
    location_type_chooser_keyboard.add_row()
    location_type_chooser_keyboard.add_text_button(**menu_button())
    
    return location_type_chooser_keyboard.get_keyboard()


def buildings_dialer() -> str:
    buildings_dialer_keyboard: Keyboard = Keyboard(one_time=True, inline=True)
    
    for (number, building) in enumerate(BUILDINGS):
        buildings_dialer_keyboard.add_text_button(text=building["button"], payload={
            "callback": LocationType.BUILDING.value, 
            "building": str(number)
        })
        
        if (number + 1) % 4 == 0:
            buildings_dialer_keyboard.add_row()
    
    buildings_dialer_keyboard.add_text_button(text="Показать все", payload={
        "callback": LocationType.BUILDING.value, 
        "building": ",".join([ str(number) for number in range(len(BUILDINGS)) ])
    })

    buildings_dialer_keyboard.add_row()
    buildings_dialer_keyboard.add_text_button(**menu_button())
    
    return buildings_dialer_keyboard.get_keyboard()

def libraries_dialer() -> str:
    libraries_dialer_keyboard: Keyboard = Keyboard(one_time=True, inline=True)
    
    for (number, library) in enumerate(LIBRARIES):
        libraries_dialer_keyboard.add_text_button(text=library["button"] if number < 4 else library["title"], payload={
            "callback": LocationType.LIBRARY.value, 
            "library": str(number)
        })
        
        if (number + 1) % 4 == 0:
            libraries_dialer_keyboard.add_row()
    
    libraries_dialer_keyboard.add_row()
    libraries_dialer_keyboard.add_text_button(text="Показать все", payload={
        "callback": LocationType.LIBRARY.value, 
        "library": ",".join([ str(number) for number in range(len(LIBRARIES)) ])
    })

    libraries_dialer_keyboard.add_row()
    libraries_dialer_keyboard.add_text_button(**menu_button())
    
    return libraries_dialer_keyboard.get_keyboard()

def sportscomplex_dialer() -> str:
    sportscomplex_dialer_keyboard: Keyboard = Keyboard(one_time=True, inline=True)
    
    for (number, sportscomplex_building) in enumerate(SPORTSCOMPLEX):
        sportscomplex_dialer_keyboard.add_text_button(text=sportscomplex_building["button"], payload={
            "callback": LocationType.SPORTSCOMPLEX.value, 
            "sportscomplex": str(number)
        })
        sportscomplex_dialer_keyboard.add_row()
    
    sportscomplex_dialer_keyboard.add_text_button(text="Показать все", payload={
        "callback": LocationType.SPORTSCOMPLEX.value, 
        "sportscomplex": ",".join([ str(number) for number in range(len(SPORTSCOMPLEX)) ])
    })

    sportscomplex_dialer_keyboard.add_row()
    sportscomplex_dialer_keyboard.add_text_button(**menu_button())
    
    return sportscomplex_dialer_keyboard.get_keyboard()

def dorms_dialer() -> str:
    dorms_dialer_keyboard: Keyboard = Keyboard(one_time=True, inline=True)
    
    for (number, dorm) in enumerate(DORMS):
        dorms_dialer_keyboard.add_text_button(text=dorm["button"], payload={
            "callback": LocationType.DORM.value, 
            "dorm": str(number)
        })
        
        if (number + 1) % 4 == 0:
            dorms_dialer_keyboard.add_row()
    
    dorms_dialer_keyboard.add_row()
    dorms_dialer_keyboard.add_text_button(text="Показать все", payload={
        "callback": LocationType.DORM.value, 
        "dorm": ",".join([ str(number) for number in range(len(DORMS)) ])
    })

    dorms_dialer_keyboard.add_row()
    dorms_dialer_keyboard.add_text_button(**menu_button())
    
    return dorms_dialer_keyboard.get_keyboard()
