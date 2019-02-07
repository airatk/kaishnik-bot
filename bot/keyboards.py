from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton
from telebot.types import ReplyKeyboardMarkup
from telebot.types import KeyboardButton
from telebot.types import ReplyKeyboardRemove

def schedule_type():
    schedule_type_keyboard = InlineKeyboardMarkup()

    schedule_type_keyboard.row(
        InlineKeyboardButton(text="сегодня", callback_data="today's"),
        InlineKeyboardButton(text="завтра", callback_data="tomorrow's")
    )
    schedule_type_keyboard.row(InlineKeyboardButton(text="текущую неделю", callback_data="weekly current"))
    schedule_type_keyboard.row(InlineKeyboardButton(text="следующую неделю", callback_data="weekly next"))

    return schedule_type_keyboard

def choose_location_type():
    location_type_keyboard = InlineKeyboardMarkup()

    location_type_keyboard.row(InlineKeyboardButton(text="Учебные здания и СК", callback_data="buildings"))
    location_type_keyboard.row(InlineKeyboardButton(text="Библиотеки", callback_data="libraries"))
    location_type_keyboard.row(InlineKeyboardButton(text="Общежития", callback_data="dorms"))

    return location_type_keyboard

def buildings_dailer():
    buildings_dailer_keyboard = InlineKeyboardMarkup()
    
    buildings_dailer_keyboard.row(
        InlineKeyboardButton(text="1", callback_data="b_s first"),
        InlineKeyboardButton(text="2", callback_data="b_s second"),
        InlineKeyboardButton(text="3", callback_data="b_s third"),
        InlineKeyboardButton(text="4", callback_data="b_s fourth")
    )
    buildings_dailer_keyboard.row(
        InlineKeyboardButton(text="5", callback_data="b_s fifth"),
        InlineKeyboardButton(text="6", callback_data="b_s sixth"),
        InlineKeyboardButton(text="7", callback_data="b_s seventh"),
        InlineKeyboardButton(text="8", callback_data="b_s eighth")
    )
    buildings_dailer_keyboard.row(
        InlineKeyboardButton(text="СК Олимп", callback_data="b_s olymp")
    )

    return buildings_dailer_keyboard

def libraries_dailer():
    libraries_dailer_keyboard = InlineKeyboardMarkup()
    
    libraries_dailer_keyboard.row(
        InlineKeyboardButton(text="1", callback_data="l_s first"),
        InlineKeyboardButton(text="2", callback_data="l_s second"),
        InlineKeyboardButton(text="3", callback_data="l_s third"),
        InlineKeyboardButton(text="9", callback_data="l_s ninth")
    )
    libraries_dailer_keyboard.row(
        InlineKeyboardButton(text="научно-техническая", callback_data="l_s sci-tech")
    )

    return libraries_dailer_keyboard

def dorms_dailer():
    dorms_dailer_keyboard = InlineKeyboardMarkup()
    
    dorms_dailer_keyboard.row(
        InlineKeyboardButton(text="1", callback_data="d_s first"),
        InlineKeyboardButton(text="2", callback_data="d_s second"),
        InlineKeyboardButton(text="3", callback_data="d_s third"),
        InlineKeyboardButton(text="4", callback_data="d_s fourth")
    )
    dorms_dailer_keyboard.row(
        InlineKeyboardButton(text="5", callback_data="d_s fifth"),
        InlineKeyboardButton(text="6", callback_data="d_s sixth"),
        InlineKeyboardButton(text="7", callback_data="d_s seventh")
    )

    return dorms_dailer_keyboard

def settings_entry():
    settings_entry_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    
    settings_entry_keyboard.row(KeyboardButton(text="/settings"))
    
    return settings_entry_keyboard

def remove_keyboard():
    return ReplyKeyboardRemove()
