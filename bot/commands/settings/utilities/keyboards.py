from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

from bot.shared.keyboards import cancel_button
from bot.shared.api.student import Settings
from bot.shared.commands import Commands


def action_chooser() -> InlineKeyboardMarkup:
    action_chooser_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    
    action_chooser_keyboard.add(*[
        cancel_button(),
        
        InlineKeyboardButton(text="Изменить отображение", callback_data=Commands.SETTINGS_APPEARANCE.value),
        InlineKeyboardButton(text="Сменить аккаунт", callback_data=Commands.LOGIN.value)
    ])
    
    return action_chooser_keyboard

def appearance_chooser(settings: Settings) -> InlineKeyboardMarkup:
    appearance_chooser_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=2)
    
    appearance_chooser_keyboard.add(*[
        InlineKeyboardButton(text="Сбросить", callback_data=Commands.SETTINGS_APPEARANCE_DROP.value),
        InlineKeyboardButton(text="Готово", callback_data=Commands.SETTINGS_APPEARANCE_DONE.value)
    ])
    
    appearance_chooser_keyboard.row(InlineKeyboardButton(
        text="• полное расписание" if settings.is_schedule_size_full else "компактное расписание •",
        callback_data=" ".join([ Commands.SETTINGS_APPEARANCE.value, Settings.Option.IS_SCHEDULE_SIZE_FULL.value ])
    ))
    
    appearance_chooser_keyboard.row(InlineKeyboardButton(
        text="• пары по датам" if settings.are_classes_on_dates else "все пары •",
        callback_data=" ".join([ Commands.SETTINGS_APPEARANCE.value, Settings.Option.ARE_CLASSES_ON_DATES.value ])
    ))
    
    return appearance_chooser_keyboard
