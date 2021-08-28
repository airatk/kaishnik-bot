from aiogram.types import CallbackQuery
from aiogram.types import ParseMode

from bot.platforms.telegram import dispatcher
from bot.platforms.telegram import guards

from bot.platforms.telegram.commands.settings.utilities.keyboards import deletion_confirmer

from bot.models.user import User

from bot.utilities.types import Command


@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Command.SETTINGS.value and
        callback.data == Command.DELETE_ACCOUNT.value
)
async def deletion(callback: CallbackQuery):
    await callback.message.edit_text(
        text="Ты точно хочешь удалить свой аккаунт со *всеми* заметками и настройками?",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=deletion_confirmer()
    )

@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Command.SETTINGS.value and
        callback.data == Command.DELETE_ACCOUNT_CONFIRM.value
)
async def deletion_confirm(callback: CallbackQuery):
    User.delete().where(User.telegram_id == callback.message.chat.id).execute()
    
    guards[callback.message.chat.id].drop()
    
    await callback.message.edit_text(text="Аккаунт удалён. Для создания нового отправь /start")
