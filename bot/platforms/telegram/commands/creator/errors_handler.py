from aiogram.types import Update
from aiogram.types import ParseMode

from bot.platforms.telegram import dispatcher

from bot.utilities.constants import KEYS


@dispatcher.errors_handler()
async def handle_errors(update: Update, exception: Exception):
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
