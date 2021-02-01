from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

from bot.platforms.telegram.commands.settings.utilities.types import SettingsOption

from bot.platforms.telegram.utilities.keyboards import cancel_button

from bot.models.settings import Settings

from bot.utilities.types import Commands


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
        callback_data=" ".join([ Commands.SETTINGS_APPEARANCE.value, SettingsOption.IS_SCHEDULE_SIZE_FULL.value ])
    ))
    
    return appearance_chooser_keyboard
