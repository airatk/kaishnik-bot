from vkwave.bots.utils.keyboards import Keyboard
from vkwave.bots.utils.keyboards import ButtonColor

from bot.platforms.vk.utilities.keyboards import menu_button
from bot.platforms.vk.utilities.keyboards import cancel_button
from bot.platforms.vk.utilities.types import CommandOfVK

from bot.models.settings import Settings

from bot.utilities.types import Command
from bot.utilities.types import SettingsOption


def action_chooser() -> str:
    action_chooser_keyboard: Keyboard = Keyboard(one_time=True, inline=True)
    
    action_chooser_keyboard.add_text_button(text="Изменить отображение", payload={ "callback": Command.SETTINGS_APPEARANCE.value })
    
    action_chooser_keyboard.add_row()
    action_chooser_keyboard.add_text_button(text="Сменить аккаунт", payload={ "callback": Command.LOGIN.value })

    action_chooser_keyboard.add_row()
    action_chooser_keyboard.add_text_button(text="Удалить аккаунт", payload={ "callback": Command.DELETE_ACCOUNT.value })

    action_chooser_keyboard.add_row()
    action_chooser_keyboard.add_text_button(text="Показать код", payload={ "callback": Command.SETTINGS_PLATFORM_CODE.value })

    action_chooser_keyboard.add_row()
    action_chooser_keyboard.add_text_button(**menu_button())
    
    return action_chooser_keyboard.get_keyboard()

def appearance_chooser(settings: Settings) -> str:
    appearance_chooser_keyboard: Keyboard = Keyboard(one_time=True, inline=True)
    
    appearance_chooser_keyboard.add_text_button(text="Cбросить", color=ButtonColor.NEGATIVE, payload={ "callback": Command.SETTINGS_APPEARANCE_DROP.value })
    appearance_chooser_keyboard.add_text_button(text="Готово", color=ButtonColor.SECONDARY, payload={ "callback": Command.SETTINGS_APPEARANCE_DONE.value })
    
    appearance_chooser_keyboard.add_row()
    appearance_chooser_keyboard.add_text_button(
        text="Полное расписание" if settings.is_schedule_size_full else "Компактное расписание",
        payload={ Command.SETTINGS_APPEARANCE.value: SettingsOption.IS_SCHEDULE_SIZE_FULL.value }
    )
    
    return appearance_chooser_keyboard.get_keyboard()

def deletion_confirmer() -> str:
    deletion_confirmer_keyboard: Keyboard = Keyboard(one_time=True, inline=True)

    deletion_confirmer_keyboard.add_text_button(**cancel_button())

    deletion_confirmer_keyboard.add_row()
    deletion_confirmer_keyboard.add_text_button(
        text="Да, удалить аккаунт", 
        color=ButtonColor.NEGATIVE, 
        payload={ "callback": Command.DELETE_ACCOUNT_CONFIRM.value }
    )

    return deletion_confirmer_keyboard.get_keyboard()

def make_start() -> str:
    make_start_keyboard: Keyboard = Keyboard(one_time=True)
    
    make_start_keyboard.add_text_button(text=CommandOfVK.START.value)

    return make_start_keyboard.get_keyboard()
