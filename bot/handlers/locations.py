from bot import kbot
from bot import students
from bot import metrics
from bot import hide_loading_notification

from bot.constants import BUILDINGS
from bot.constants import LIBRARIES
from bot.constants import DORMS

from bot.keyboards.locations import choose_location_type
from bot.keyboards.locations import buildings_dialer
from bot.keyboards.locations import libraries_dialer
from bot.keyboards.locations import dorms_dialer


@kbot.message_handler(
    commands=["locations"],
    func=lambda message: students[message.chat.id].previous_message is None
)
def locations(message):
    kbot.send_chat_action(chat_id=message.chat.id, action="typing")
    
    metrics.increment("locations")
    
    students[message.chat.id].previous_message = "/locations"  # Gates System (GS)
    
    kbot.send_message(
        chat_id=message.chat.id,
        text="Аж три варианта на выбор:",
        reply_markup=choose_location_type()
    )


@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/locations" and
        callback.data == "buildings_type"
)
def b_s(callback):
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="У родного КАИ 8 учебных зданий и 1 спортивный комплекс:",
        reply_markup=buildings_dialer()
    )
    
    hide_loading_notification(id=callback.id)

@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/locations" and
        "buildings" in callback.data
)
def send_building(callback):
    kbot.send_chat_action(chat_id=callback.message.chat.id, action="find_location")
    
    number = callback.data.replace("buildings ", "")
    
    kbot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )
    kbot.send_venue(
        chat_id=callback.message.chat.id,
        latitude=BUILDINGS[number]["latitude"],
        longitude=BUILDINGS[number]["longitude"],
        title=BUILDINGS[number]["title"],
        address=BUILDINGS[number]["address"]
    )
    kbot.send_message(
        chat_id=callback.message.chat.id,
        text=BUILDINGS[number]["description"],
        parse_mode="Markdown"
    )
    
    students[callback.message.chat.id].previous_message = None  # Gates System (GS)
    
    hide_loading_notification(id=callback.id)


@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/locations" and
        callback.data == "libraries_type"
)
def l_s(callback):
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="У родного КАИ 5 библиотек:",
        reply_markup=libraries_dialer()
    )
    
    hide_loading_notification(id=callback.id)

@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/locations" and
        "libraries" in callback.data
)
def send_library(callback):
    kbot.send_chat_action(chat_id=callback.message.chat.id, action="find_location")
    
    number = callback.data.replace("libraries ", "")
    building = LIBRARIES[number]["building"]
    
    kbot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )
    kbot.send_venue(
        chat_id=callback.message.chat.id,
        latitude=BUILDINGS[building]["latitude"],
        longitude=BUILDINGS[building]["longitude"],
        title=LIBRARIES[number]["title"],
        address=BUILDINGS[building]["address"]
    )
    kbot.send_message(
        chat_id=callback.message.chat.id,
        text=LIBRARIES[number]["description"],
        parse_mode="Markdown"
    )
    
    students[callback.message.chat.id].previous_message = None  # Gates System (GS)
    
    hide_loading_notification(id=callback.id)


@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/locations" and
        callback.data == "dorms_type"
)
def d_s(callback):
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="У родного КАИ 7 общежитий:",
        reply_markup=dorms_dialer()
    )
    
    hide_loading_notification(id=callback.id)

@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/locations" and
        "dorms" in callback.data
)
def send_dorm(callback):
    kbot.send_chat_action(chat_id=callback.message.chat.id, action="find_location")
    
    number = callback.data.replace("dorms ", "")
    
    kbot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )
    kbot.send_venue(
        chat_id=callback.message.chat.id,
        latitude=DORMS[number]["latitude"],
        longitude=DORMS[number]["longitude"],
        title=DORMS[number]["title"],
        address=DORMS[number]["address"]
    )
    kbot.send_message(
        chat_id=callback.message.chat.id,
        text=DORMS[number]["description"],
        parse_mode="Markdown"
    )
    
    students[callback.message.chat.id].previous_message = None  # Gates System (GS)
    
    hide_loading_notification(id=callback.id)


@kbot.message_handler(func=lambda message: students[message.chat.id].previous_message == "/locations")
def gs_locations(message): kbot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
