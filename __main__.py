from aiogram import executor

from bot import dispatcher


if __name__ == "__main__":
    executor.start_polling(dispatcher)
