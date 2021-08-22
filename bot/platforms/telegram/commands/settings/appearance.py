from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup

from bot.platforms.telegram import dispatcher
from bot.platforms.telegram import guards

from bot.platforms.telegram.commands.settings.utilities.keyboards import appearance_chooser

from bot.platforms.telegram.utilities.helpers import top_notification

from bot.models.user import User
from bot.models.settings import Settings

from bot.utilities.types import Command
from bot.utilities.types import SettingsOption


@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Command.SETTINGS.value and
        callback.data.split()[0] == Command.SETTINGS_APPEARANCE.value
)
@top_notification
async def appearance(callback: CallbackQuery):
    user: User = User.get(User.telegram_id == callback.message.chat.id)
    settings: Settings = Settings.get(Settings.user == user)
    
    if SettingsOption.IS_SCHEDULE_SIZE_FULL.value in callback.data:
        settings.is_schedule_size_full = not settings.is_schedule_size_full
    
    settings.save()
    
    reply_markup: InlineKeyboardMarkup = appearance_chooser(settings=settings)
    
    if callback.data == Command.SETTINGS_APPEARANCE.value:
        await callback.message.edit_text(
            text="Нажми на нужную опцию, чтобы изменить её:",
            reply_markup=reply_markup
        )
    else:
        await callback.message.edit_reply_markup(reply_markup=reply_markup)

@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Command.SETTINGS.value and
        callback.data == Command.SETTINGS_APPEARANCE_DROP.value
)
@top_notification
async def appearance_drop(callback: CallbackQuery):
    user: User = User.get(User.telegram_id == callback.message.chat.id)
    
    Settings.delete().where(Settings.user == user).execute()
    Settings.insert(user=user).execute()
    
    await appearance_done(callback=callback)

@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Command.SETTINGS.value and
        callback.data == Command.SETTINGS_APPEARANCE_DONE.value
)
@top_notification
async def appearance_done(callback: CallbackQuery):
    await callback.message.edit_text(text="Сохранено!")
    
    guards[callback.message.chat.id].drop()
