from random import choice

from re import Match
from re import search

from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram.types import ChatType
from aiogram.types import ParseMode

from bot.platforms.telegram import dispatcher
from bot.platforms.telegram import guards

from bot.platforms.telegram.commands.login.menu import finish_login
from bot.platforms.telegram.commands.login.utilities.keyboards import againer
from bot.platforms.telegram.commands.login.utilities.keyboards import guess_approver

from bot.platforms.telegram.utilities.keyboards import canceler
from bot.platforms.telegram.utilities.helpers import top_notification

from bot.models.user import User

from bot.utilities.constants import BOT_ADDRESSING
from bot.utilities.types import Command
from bot.utilities.api.constants import LOADING_REPLIES
from bot.utilities.api.types import ResponseError
from bot.utilities.api.student import get_group_schedule_id


@dispatcher.callback_query_handler(
    lambda callback:
        callback.message.chat.type != ChatType.PRIVATE and
        guards[callback.message.chat.id].text == Command.LOGIN.value and
        callback.data == Command.LOGIN_COMPACT.value
)
@top_notification
async def login_compact_guess_group(callback: CallbackQuery):
    await callback.message.edit_text(
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    guess: Match = search("[0-9][0-9][0-9][0-9][0-9]?[0-9]?", callback.message.chat.title)
    
    # If input is unusual, go the usual login way
    if guess is None:
        await login_compact(callback=callback)
        return
    
    (group_schedule_id, _) = get_group_schedule_id(group=guess.group())
    
    # If the guess was unsuccessful, go the usual login way
    if group_schedule_id is None:
        await login_compact(callback=callback)
        return
    
    User.update(
        group=guess.group(),
        group_schedule_id=group_schedule_id,
        bb_login=None,
        bb_password=None,
        is_setup=False
    ).where(
        User.telegram_id == callback.message.chat.id
    ).execute()

    await callback.message.edit_text(
        text="*{possible_group}* — это твоя группа, верно?".format(possible_group=guess.group()),
        reply_markup=guess_approver(),
        parse_mode=ParseMode.MARKDOWN
    )
    
    guards[callback.message.chat.id].text = Command.LOGIN_COMPACT.value
    guards[callback.message.chat.id].message = callback.message

@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Command.LOGIN_COMPACT.value and
        callback.data == Command.LOGIN_CORRECT_GROUP_GUESS.value
)
@top_notification
async def finish_login_compact_with_correct_group_guess(callback: CallbackQuery):
    await finish_login(message=callback.message)


@dispatcher.callback_query_handler(
    lambda callback: (
        guards[callback.message.chat.id].text == Command.LOGIN.value and
        callback.data == Command.LOGIN_COMPACT.value
    ) or (
        guards[callback.message.chat.id].text == Command.LOGIN_COMPACT.value and
        callback.data == Command.LOGIN_WRONG_GROUP_GUESS.value
    )
)
@top_notification
async def login_compact(callback: CallbackQuery):
    if callback.message.chat.type == ChatType.PRIVATE:
        User.update(
            group=None,
            group_schedule_id=None,
            bb_login=None,
            bb_password=None,
            is_setup=False
        ).where(
            User.telegram_id == callback.message.chat.id
        ).execute()
    
    guard_message: Message = await callback.message.edit_text(
        text="Отправь номер своей группы.",
        reply_markup=canceler()
    )
    
    guards[callback.message.chat.id].text = Command.LOGIN_COMPACT.value
    guards[callback.message.chat.id].message = guard_message

@dispatcher.message_handler(
    lambda message:
        message.chat.type != ChatType.PRIVATE and (
            message.text is not None and message.text.startswith(BOT_ADDRESSING) or
            message.reply_to_message is not None and message.reply_to_message.from_user.is_bot
        ) and guards[message.chat.id].text == Command.LOGIN_COMPACT.value
)
@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        guards[message.chat.id].text == Command.LOGIN_COMPACT.value
)
async def set_group(message: Message):
    # Getting rid of the bot addressing
    if message.chat.type != ChatType.PRIVATE:
        message.text = message.text.replace(BOT_ADDRESSING, "")
    
    await message.delete()
    await guards[message.chat.id].message.edit_text(
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    (group_schedule_id, response_error) = get_group_schedule_id(group=message.text)
    
    if group_schedule_id is None:
        if response_error is ResponseError.NO_RESPONSE:
            (text, reply_markup) = (response_error.value, None)
        else:
            (text, reply_markup) = ("\n\n".join([ response_error.value, "Попробуешь снова?" ]), againer())
        
        await guards[message.chat.id].message.edit_text(
            text=text, reply_markup=reply_markup,
            disable_web_page_preview=True
        )
        
        guards[message.chat.id].text = Command.LOGIN.value
        return
    
    user_id: int = User.get(User.telegram_id == message.chat.id).user_id
    
    User.update(
        group=message.text,
        group_schedule_id=group_schedule_id,
    ).where(
        User.telegram_id == message.chat.id
    ).execute()
    
    await finish_login(message=message)
