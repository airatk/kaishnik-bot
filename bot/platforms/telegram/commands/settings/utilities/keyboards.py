from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

from bot.platforms.telegram.utilities.keyboards import cancel_button

from bot.models.settings import Settings

from bot.utilities.types import Command
from bot.utilities.types import SettingsOption


def action_chooser() -> InlineKeyboardMarkup:
    action_chooser_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    
    action_chooser_keyboard.add(
        cancel_button(),
        InlineKeyboardButton(text="изменить отображение", callback_data=Command.SETTINGS_APPEARANCE.value),
        InlineKeyboardButton(text="сменить аккаунт", callback_data=Command.LOGIN.value),
        InlineKeyboardButton(text="удалить аккаунт", callback_data=Command.DELETE_ACCOUNT.value),
        InlineKeyboardButton(text="показать код", callback_data=Command.SETTINGS_PLATFORM_CODE.value)
    )
    
    return action_chooser_keyboard

def appearance_chooser(settings: Settings) -> InlineKeyboardMarkup:
    appearance_chooser_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=2)
    
    appearance_chooser_keyboard.add(
        InlineKeyboardButton(text="сбросить", callback_data=Command.SETTINGS_APPEARANCE_DROP.value),
        InlineKeyboardButton(text="готово", callback_data=Command.SETTINGS_APPEARANCE_DONE.value)
    )
    
    appearance_chooser_keyboard.row(
        InlineKeyboardButton(
            text="• полное расписание" if settings.is_schedule_size_full else "компактное расписание •",
            callback_data=" ".join([ Command.SETTINGS_APPEARANCE.value, SettingsOption.IS_SCHEDULE_SIZE_FULL.value ])
        )
    )
    
    return appearance_chooser_keyboard

def deletion_confirmer() -> InlineKeyboardMarkup:
    deletion_confirmer_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)

    deletion_confirmer_keyboard.add(
        cancel_button(),
        InlineKeyboardButton(text="Да, удалить аккаунт", callback_data=Command.DELETE_ACCOUNT_CONFIRM.value)
    )

    return deletion_confirmer_keyboard
