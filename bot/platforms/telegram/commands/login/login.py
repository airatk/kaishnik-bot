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
from bot.utilities.constants import GROUP_NUMBER_PATTERN
from bot.utilities.types import Command
from bot.utilities.api.constants import LOADING_REPLIES
from bot.utilities.api.types import ResponseError
from bot.utilities.api.student import get_group_schedule_id
from bot.utilities.api.student import authenticate_user_via_kai_cas


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
    
    guess: Match = search(pattern=GROUP_NUMBER_PATTERN, string=callback.message.chat.title)
    
    # If group chat title doesn't match the exact pattern, go the usual login way
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
    lambda callback:
        guards[callback.message.chat.id].text == Command.LOGIN.value and
        callback.data == Command.LOGIN_BB.value
)
@top_notification
async def login_bb(callback: CallbackQuery):
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
        text="Отправь логин от ББ.",
        reply_markup=canceler()
    )
    
    guards[callback.message.chat.id].text = Command.LOGIN_SET_BB_LOGIN.value
    guards[callback.message.chat.id].message = guard_message

@dispatcher.message_handler(
    lambda message: guards[message.chat.id].text == Command.LOGIN_SET_BB_LOGIN.value
)
async def set_bb_login(message: Message):
    await message.delete()

    User.update(
        bb_login=message.text
    ).where(
        User.telegram_id == message.chat.id
    ).execute()
    
    await guards[message.chat.id].message.edit_text(
        text="Отправь пароль от ББ.",
        reply_markup=canceler()
    )
    
    guards[message.chat.id].text = Command.LOGIN_SET_BB_PASSWORD.value

@dispatcher.message_handler(
    lambda message: guards[message.chat.id].text == Command.LOGIN_SET_BB_PASSWORD.value
)
async def set_bb_password(message: Message):
    await message.delete()
    await guards[message.chat.id].message.edit_text(
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )

    user: User = User.get(telegram_id=message.chat.id)
    user.bb_password = message.text
    user.save()
    
    (_, response_error) = authenticate_user_via_kai_cas(user=user)

    if response_error is not None:
        if response_error is not ResponseError.INCORRECT_BB_CREDENTIALS:
            await guards[message.chat.id].message.edit_text(text=response_error.value)

            guards[message.chat.id].drop()
            return
        
        await guards[message.chat.id].message.edit_text(
            text="\n\n".join([ response_error.value, "Отправь логин от ББ." ]),
            reply_markup=canceler()
        )

        guards[message.chat.id].text = Command.LOGIN_SET_BB_LOGIN.value
        return

    await guards[message.chat.id].message.edit_text(
        text="Отправь номер своей группы.",
        reply_markup=canceler()
    )
    
    guards[message.chat.id].text = Command.LOGIN_SET_GROUP.value


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
    
    guards[callback.message.chat.id].text = Command.LOGIN_SET_GROUP.value
    guards[callback.message.chat.id].message = guard_message

@dispatcher.message_handler(
    lambda message:
        message.chat.type != ChatType.PRIVATE and (
            message.text is not None and message.text.startswith(BOT_ADDRESSING) or
            message.reply_to_message is not None and message.reply_to_message.from_user.is_bot
        ) and guards[message.chat.id].text == Command.LOGIN_SET_GROUP.value
)
@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        guards[message.chat.id].text == Command.LOGIN_SET_GROUP.value
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
            await guards[message.chat.id].message.edit_text(
                text=response_error.value,
                disable_web_page_preview=True
            )

            guards[message.chat.id].drop()
            return
        
        await guards[message.chat.id].message.edit_text(
            text="\n\n".join([ response_error.value, "Попробуешь снова?" ]),
            reply_markup=againer(),
            disable_web_page_preview=True
        )
        
        guards[message.chat.id].text = Command.LOGIN.value
        return
    
    User.update(
        group=message.text,
        group_schedule_id=group_schedule_id,
    ).where(
        User.telegram_id == message.chat.id
    ).execute()
    
    await finish_login(message=message)
