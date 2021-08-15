from vkwave.bots.utils.keyboards import Keyboard
from vkwave.bots.utils.keyboards import ButtonColor

from bot.platforms.vk.utilities.keyboards import menu_button
from bot.platforms.vk.utilities.keyboards import cancel_button

from bot.models.settings import Settings

from bot.utilities.types import Commands
from bot.utilities.types import SettingsOption


def action_chooser() -> str:
    action_chooser_keyboard: Keyboard = Keyboard(one_time=True, inline=True)
    
    action_chooser_keyboard.add_text_button(text="Изменить отображение", payload={ "callback": Commands.SETTINGS_APPEARANCE.value })
    
    action_chooser_keyboard.add_row()
    action_chooser_keyboard.add_text_button(text="Сменить аккаунт", payload={ "callback": Commands.LOGIN.value })

    action_chooser_keyboard.add_row()
    action_chooser_keyboard.add_text_button(text="Удалить аккаунт", payload={ "callback": Commands.DELETE_ACCOUNT.value })

    action_chooser_keyboard.add_row()
    action_chooser_keyboard.add_text_button(text="Показать код", payload={ "callback": Commands.SETTINGS_PLATFORM_CODE.value })

    action_chooser_keyboard.add_row()
    action_chooser_keyboard.add_text_button(**menu_button())
    
    return action_chooser_keyboard.get_keyboard()

def appearance_chooser(settings: Settings) -> str:
    appearance_chooser_keyboard: Keyboard = Keyboard(one_time=True, inline=True)
    
    appearance_chooser_keyboard.add_text_button(text="Cбросить", color=ButtonColor.NEGATIVE, payload={ "callback": Commands.SETTINGS_APPEARANCE_DROP.value })
    appearance_chooser_keyboard.add_text_button(text="Готово", color=ButtonColor.SECONDARY, payload={ "callback": Commands.SETTINGS_APPEARANCE_DONE.value })
    
    appearance_chooser_keyboard.add_row()
    appearance_chooser_keyboard.add_text_button(
        text="Полное расписание" if settings.is_schedule_size_full else "Компактное расписание",
        payload={ Commands.SETTINGS_APPEARANCE.value: SettingsOption.IS_SCHEDULE_SIZE_FULL.value }
    )
    
    return appearance_chooser_keyboard.get_keyboard()

def deletion_confirmer() -> str:
    deletion_confirmer_keyboard: Keyboard = Keyboard(one_time=True, inline=True)

    deletion_confirmer_keyboard.add_text_button(**cancel_button())

    deletion_confirmer_keyboard.add_row()
    deletion_confirmer_keyboard.add_text_button(text="Да, удалить аккаунт", color=ButtonColor.NEGATIVE, payload={ "callback": Commands.DELETE_ACCOUNT_CONFIRM.value })

    return deletion_confirmer_keyboard.get_keyboard()
