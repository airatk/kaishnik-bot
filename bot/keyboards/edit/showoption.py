from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton

from bot.helpers.constants import WEEKDAYS


def edited_classes_weektype_dialer(edited_classes):
    edited_classes_weektype_dialer_keyboard = InlineKeyboardMarkup(row_width=1)
    
    edited_classes_weektype_dialer_keyboard.row(InlineKeyboardButton(text="отменить", callback_data="cancel-edit"))
    
    edited_classes_weektype_dialer_keyboard.row(InlineKeyboardButton(text="показать все", callback_data="show-all-edit-all"))
    
    weektypes = { "even": 0, "odd": 0, "none": 0 }
    
    for edited_class in edited_classes:
        if edited_class.is_even is True: weektypes["even"] += 1
        elif edited_class.is_even is False: weektypes["odd"] += 1
        elif edited_class.is_even is None: weektypes["none"] += 1
    
    if weektypes["even"] != 0: edited_classes_weektype_dialer_keyboard.row(
        InlineKeyboardButton(
            text="чётная ({})".format(weektypes["even"]),
            callback_data="show-weektype-even"
        )
    )
    if weektypes["odd"] != 0: edited_classes_weektype_dialer_keyboard.row(
        InlineKeyboardButton(
            text="нечётная ({})".format(weektypes["odd"]),
            callback_data="show-weektype-odd"
        )
    )
    if weektypes["none"] != 0: edited_classes_weektype_dialer_keyboard.row(
        InlineKeyboardButton(
            text="каждая ({})".format(weektypes["none"]),
            callback_data="show-weektype-none"
        )
    )
    
    return edited_classes_weektype_dialer_keyboard

def edited_classes_weekday_dialer(weektype, edited_classes):
    edited_classes_weekday_dialer_keyboard = InlineKeyboardMarkup(row_width=1)
    
    edited_classes_weekday_dialer_keyboard.row(InlineKeyboardButton(text="отменить", callback_data="cancel-edit"))
    
    edited_classes_weekday_dialer_keyboard.row(InlineKeyboardButton(text="Показать все", callback_data="show-all-edit-{}-all".format(weektype)))
    
    if weektype == "even": is_even = True
    elif weektype == "odd": is_even = False
    elif weektype == "none": is_even = None
    
    for weekday, weekday_name in WEEKDAYS.items():
        edited_classes_number = 0
        
        for edited_class in edited_classes:
            if edited_class.is_even is is_even and edited_class.weekday == weekday:
                edited_classes_number += 1
    
        if edited_classes_number != 0:
            edited_classes_weekday_dialer_keyboard.add(*[
                InlineKeyboardButton(
                    text="{} ({})".format(weekday_name, edited_classes_number),
                    callback_data="show-weekday-{}-{}".format(weekday, weektype)
                )
            ])
    
    return edited_classes_weekday_dialer_keyboard

def edited_classes_one_dialer(weektype, weekday, edited_classes):
    edited_classes_one_dialer_keyboard = InlineKeyboardMarkup(row_width=1)
    
    edited_classes_one_dialer_keyboard.row(InlineKeyboardButton(text="отменить", callback_data="cancel-edit"))
    
    edited_classes_one_dialer_keyboard.row(InlineKeyboardButton(text="Показать все", callback_data="show-all-edit-{}-{}-all".format(weektype, weekday)))
    
    if weektype == "even": is_even = True
    elif weektype == "odd": is_even = False
    elif weektype == "none": is_even = None
    
    edited_classes_one_dialer_keyboard.add(*[
        InlineKeyboardButton(
            text=edited_class.get_simple(),
            callback_data="show-one-{}".format(index)
        ) for index, edited_class in enumerate(edited_classes) if (
            edited_class.is_even is is_even and edited_class.weekday == weekday
        )
    ])
    
    return edited_classes_one_dialer_keyboard
