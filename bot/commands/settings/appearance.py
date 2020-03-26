from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup

from bot import dispatcher
from bot import students

from bot.commands.settings.utilities.keyboards import appearance_chooser

from bot.shared.helpers import top_notification
from bot.shared.api.student import Settings
from bot.shared.data.helpers import save_data
from bot.shared.data.constants import USERS_FILE
from bot.shared.commands import Commands


@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.SETTINGS.value and
        callback.data.split()[0] == Commands.SETTINGS_APPEARANCE.value
)
@top_notification
async def appearance(callback: CallbackQuery):
    if Settings.Option.IS_SCHEDULE_SIZE_FULL.value in callback.data:
        students[callback.message.chat.id].settings.is_schedule_size_full = not students[callback.message.chat.id].settings.is_schedule_size_full
    elif Settings.Option.ARE_CLASSES_ON_DATES.value in callback.data:
        students[callback.message.chat.id].settings.are_classes_on_dates = not students[callback.message.chat.id].settings.are_classes_on_dates
    
    reply_markup: InlineKeyboardMarkup = appearance_chooser(settings=students[callback.message.chat.id].settings)
    
    if callback.data == Commands.SETTINGS_APPEARANCE.value:
        await callback.message.edit_text(
            text="Нажми на одну из опций, чтобы изменить значение на противоположное:",
            reply_markup=reply_markup
        )
    else:
        await callback.message.edit_reply_markup(reply_markup=reply_markup)

@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.SETTINGS.value and
        callback.data == Commands.SETTINGS_APPEARANCE_DROP.value
)
@top_notification
async def appearance_drop(callback: CallbackQuery):
    students[callback.message.chat.id].settings.drop()
    
    await appearance_done(callback=callback)

@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.SETTINGS.value and
        callback.data == Commands.SETTINGS_APPEARANCE_DONE.value
)
@top_notification
async def appearance_done(callback: CallbackQuery):
    await callback.message.edit_text(text="Сохранено!")
    
    students[callback.message.chat.id].guard.drop()
    
    save_data(file=USERS_FILE, object=students)
