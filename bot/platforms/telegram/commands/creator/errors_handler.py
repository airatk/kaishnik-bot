from aiogram.types import Update
from aiogram.types import ParseMode

from aiogram.utils.exceptions import MessageCantBeDeleted
from aiogram.utils.exceptions import MessageCantBeEdited
from aiogram.utils.exceptions import MessageIdInvalid
from aiogram.utils.exceptions import MessageNotModified
from aiogram.utils.exceptions import MessageToDeleteNotFound
from aiogram.utils.exceptions import MessageToEditNotFound

from bot.platforms.telegram import dispatcher

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
	
	await dispatcher.bot.send_message(
		chat_id=KEYS.CREATOR_TELEGRAM_ID,
		text=(
			f"*New Error Was Caught!*\n"
			f"\n"
			f"*update*\n"
			f"`{update}`\n"
			f"\n"
			f"*exception*\n"
			f"`{exception}`"
		),
		parse_mode=ParseMode.MARKDOWN,
		disable_web_page_preview=True
	)
