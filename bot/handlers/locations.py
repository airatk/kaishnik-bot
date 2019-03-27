from bot import kaishnik
from bot import metrics

from bot.constants import BUILDINGS
from bot.constants import LIBRARIES
from bot.constants import DORMS

from bot.keyboards import choose_location_type
from bot.keyboards import buildings_dailer
from bot.keyboards import libraries_dailer
from bot.keyboards import dorms_dailer


@kaishnik.message_handler(commands=["locations"])
def locations(message):
    kaishnik.send_chat_action(chat_id=message.chat.id, action="typing")
    
    metrics.increment("locations")
    
    kaishnik.send_message(
        chat_id=message.chat.id,
        text="Аж три варианта на выбор:",
        reply_markup=choose_location_type()
    )


# Buildings
@kaishnik.callback_query_handler(
    func=lambda callback:
        callback.data == "buildings_type"
)
def b_s(callback):
    kaishnik.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="У родного КАИ 8 учебных зданий и 1 спортивный комплекс:",
        reply_markup=buildings_dailer()
    )

@kaishnik.callback_query_handler(
    func=lambda callback:
        "buildings" in callback.data
)
def send_building(callback):
    kaishnik.send_chat_action(chat_id=callback.message.chat.id, action="find_location")

    kaishnik.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )
    
    number = callback.data.replace("buildings ", "")
    
    kaishnik.send_venue(
        chat_id=callback.message.chat.id,
        latitude=BUILDINGS[number]["latitude"],
        longitude=BUILDINGS[number]["longitude"],
        title=BUILDINGS[number]["title"],
        address=BUILDINGS[number]["address"]
    )
    kaishnik.send_message(
        chat_id=callback.message.chat.id,
        text=BUILDINGS[number]["description"],
        parse_mode="Markdown"
    )


# Libraries
@kaishnik.callback_query_handler(
    func=lambda callback:
        callback.data == "libraries_type"
)
def l_s(callback):
    kaishnik.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="У родного КАИ 5 библиотек:",
        reply_markup=libraries_dailer()
    )

@kaishnik.callback_query_handler(
    func=lambda callback:
        "libraries" in callback.data
)
def send_library(callback):
    kaishnik.send_chat_action(chat_id=callback.message.chat.id, action="find_location")
    
    kaishnik.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )
    
    number = callback.data.replace("libraries ", "")
    building = LIBRARIES[number]["building"]
    
    kaishnik.send_venue(
        chat_id=callback.message.chat.id,
        latitude=BUILDINGS[building]["latitude"],
        longitude=BUILDINGS[building]["longitude"],
        title=LIBRARIES[number]["title"],
        address=BUILDINGS[building]["address"]
    )
    kaishnik.send_message(
        chat_id=callback.message.chat.id,
        text=LIBRARIES[number]["description"],
        parse_mode="Markdown"
    )


# Dormitories
@kaishnik.callback_query_handler(
    func=lambda callback:
        callback.data == "dorms_type"
)
def d_s(callback):
    kaishnik.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="У родного КАИ 7 общежитий:",
        reply_markup=dorms_dailer()
    )

@kaishnik.callback_query_handler(
    func=lambda callback:
        "dorms" in callback.data
)
def send_dorm(callback):
    kaishnik.send_chat_action(chat_id=callback.message.chat.id, action="find_location")
    
    kaishnik.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )
    
    number = callback.data.replace("dorms ", "")
    
    kaishnik.send_venue(
        chat_id=callback.message.chat.id,
        latitude=DORMS[number]["latitude"],
        longitude=DORMS[number]["longitude"],
        title=DORMS[number]["title"],
        address=DORMS[number]["address"]
    )
    kaishnik.send_message(
        chat_id=callback.message.chat.id,
        text=DORMS[number]["description"],
        parse_mode="Markdown"
    )
