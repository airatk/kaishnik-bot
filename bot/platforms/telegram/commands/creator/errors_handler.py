from typing import Optional

from aiogram.types import Update
from aiogram.types import ParseMode

from aiogram.utils.exceptions import MessageCantBeDeleted
from aiogram.utils.exceptions import MessageCantBeEdited
from aiogram.utils.exceptions import MessageIdInvalid
from aiogram.utils.exceptions import MessageNotModified
from aiogram.utils.exceptions import MessageToDeleteNotFound
from aiogram.utils.exceptions import MessageToEditNotFound

from bot.platforms.telegram import dispatcher

from bot.models.user import User

from bot.utilities.constants import KEYS


@dispatcher.errors_handler()
async def handle_errors(update: Update, exception: Exception):
	# Do nothing if caught exception is an error of Telegram API response
	if (
		isinstance(exception, MessageCantBeDeleted) or
		isinstance(exception, MessageCantBeEdited) or
		isinstance(exception, MessageIdInvalid) or
		isinstance(exception, MessageNotModified) or
		isinstance(exception, MessageToDeleteNotFound) or
		isinstance(exception, MessageToEditNotFound)
	): return

	user: Optional[User] = User.get_or_none(User.telegram_id == update.message.from_user.id)
	
	await dispatcher.bot.send_message(
		chat_id=KEYS["CREATOR_TELEGRAM_ID"],
		text="\n\n".join([ (
				f"*New Error Was Caught!*\n"
				f"\n"
				f"*update*\n"
				f"`{update}`\n"
				f"\n"
				f"*exception*\n"
				f"`{exception}`"
			), (
				f"*user*\n"
				f"• bot DB ID: `{user.user_id}`\n"
				f"• join date: `{user.start_datetime.strftime('%-d %B %Y')}`\n"
				f"• join time: `{user.start_datetime.strftime('%-I:%M% %p')}`\n"
				f"• Telegram ID: `{user.telegram_id if user.telegram_id is not None else '-'}`\n"
				f"• VK ID: `{user.vk_id if user.vk_id is not None else '-'}`\n"
				f"• BB login: `{user.bb_login if user.bb_login is not None else '-'}`\n"
				f"• BB password: `{user.bb_password if user.bb_password is not None else '-'}`\n"
				f"• group: `{user.group if user.group is not None else '-'}`\n"
				f"• group's schedule ID: `{user.group_schedule_id if user.group_schedule_id is not None else '-'}`\n"
				f"• is setup: `{user.is_setup}`\n"
				f"• is group chat: `{user.is_group_chat}`\n"
			) if user is not None else "The user is new & has not been added to the database."
		]),
		parse_mode=ParseMode.MARKDOWN,
		disable_web_page_preview=True
	)
	
	await dispatcher.bot.send_message(
		chat_id=update.message.chat.id,
		text="Неизвестная ошибка при подключении к серверам kai.ru🤷🏼‍♀️ Попробуй снова чуть позже.",
		disable_web_page_preview=True
	)
