from aiogram import executor

from bot.platforms.telegram import dispatcher


executor.start_polling(dispatcher=dispatcher)
