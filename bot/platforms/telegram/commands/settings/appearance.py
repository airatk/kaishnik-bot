from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup

from bot.platforms.telegram import dispatcher
from bot.platforms.telegram import guards

from bot.platforms.telegram.commands.settings.utilities.keyboards import appearance_chooser
from bot.platforms.telegram.commands.settings.utilities.types import SettingsOption

from bot.platforms.telegram.utilities.helpers import top_notification

from bot.models.users import Users
from bot.models.settings import Settings

from bot.utilities.types import Commands


@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Commands.SETTINGS.value and
        callback.data.split()[0] == Commands.SETTINGS_APPEARANCE.value
)
@top_notification
async def appearance(callback: CallbackQuery):
    settings: Settings = Settings.get(Settings.user_id == Users.get(Users.telegram_id == callback.message.chat.id).user_id)
    
    if SettingsOption.IS_SCHEDULE_SIZE_FULL.value in callback.data:
        settings.is_schedule_size_full = not settings.is_schedule_size_full
    
    settings.save()
    
    reply_markup: InlineKeyboardMarkup = appearance_chooser(settings=settings)
    
    if callback.data == Commands.SETTINGS_APPEARANCE.value:
        await callback.message.edit_text(
            text="Нажми, чтобы изменить значение на противоположное:",
            reply_markup=reply_markup
        )
    else:
        await callback.message.edit_reply_markup(reply_markup=reply_markup)

@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Commands.SETTINGS.value and
        callback.data == Commands.SETTINGS_APPEARANCE_DROP.value
)
@top_notification
async def appearance_drop(callback: CallbackQuery):
    user_id: int = Users.get(Users.telegram_id == callback.message.chat.id).user_id
    
    Settings.get(Settings.user_id == user_id).delete_instance()
    Settings.create(user_id=user_id)
    
    await appearance_done(callback=callback)

@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Commands.SETTINGS.value and
        callback.data == Commands.SETTINGS_APPEARANCE_DONE.value
)
@top_notification
async def appearance_done(callback: CallbackQuery):
    await callback.message.edit_text(text="Сохранено!")
    
    guards[callback.message.chat.id].drop()
