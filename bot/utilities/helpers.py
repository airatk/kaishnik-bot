from typing import List
from typing import Optional

from datetime import datetime

from peewee import ModelSelect

from aiogram.types import Message
from aiogram.types import CallbackQuery
from vkwave.bots import SimpleBotEvent

from bot.models.user import User
from bot.models.metrics import Metrics
from bot.models.donation import Donation

from bot.utilities.constants import MAX_SYMBOLS_NUMBER
from bot.utilities.constants import POSSIBLE_PLATFORM_CODE_CHARACTERS
from bot.utilities.constants import USER_ID_MODIFIER
from bot.utilities.constants import DIGIT_MODIFIER
from bot.utilities.constants import PLATFORM_CODE_SUFFIX
from bot.utilities.constants import TOP_DONATORS_NUMBER
from bot.utilities.types import Platform
from bot.utilities.types import Command


def note_metrics(platform: Platform, command: Command):
    def outer(func):
        async def inner(arg):
            user_platform_id: int = 0

            if isinstance(arg, Message):
                user_platform_id = arg.chat.id
            elif isinstance(arg, CallbackQuery):
                user_platform_id = arg.message.chat.id
            elif isinstance(arg, SimpleBotEvent):
                user_platform_id = arg.object.object.message.peer_id
            
            user: Optional[User] = None
            
            if platform is Platform.TELEGRAM:
                user = User.get_or_none(User.telegram_id == user_platform_id)
            elif platform is Platform.VK:
                user = User.get_or_none(User.vk_id == user_platform_id)
            
            (last_metrics, is_newly_created) = Metrics.get_or_create(
                user=user,
                platform=platform.value,
                action=command.value,
                perform_datetime=datetime.now().strftime("%Y-%m-%d %H:%M")
            )
            
            if not is_newly_created:
                last_metrics.usage_number += 1
                last_metrics.save()
            
            await func(arg)
        return inner
    return outer


def clarify_markdown(string: str) -> str:
    index: int = 0
    is_single: bool = False
    
    for (letter_index, letter) in enumerate(string):
        if letter in [ "*", "_", "`" ]:
            (index, is_single) = (letter_index, not is_single)
    
    return "\\".join([ string[:index], string[index:] ]) if is_single else string

def remove_markdown(string: str) -> str:
    return string.replace("*", "").replace("_", "").replace("`", "").replace("~", "").replace("\\", "")


def shorten(string: str) -> str:
    return "{main_part}{ellipsis}".format(
        main_part=remove_markdown(string[:MAX_SYMBOLS_NUMBER]).strip(),
        ellipsis="…" if len(string) > MAX_SYMBOLS_NUMBER else ""
    )


def get_top_donators() -> str:
    top_donations_list: ModelSelect = Donation.select().order_by(
        Donation.amount.desc(),
        Donation.date.desc(),
        Donation.donation_id.desc()
    ).limit(value=TOP_DONATORS_NUMBER)
    
    top_donators: str = "\n".join([
        "Большое спасибо всем тем, кто внёс свой донат♥️\n",
        "Особенное спасибо за большую поддержку топу донатеров:",
        "\n".join([ 
            f"*{index + 1}.* {donation.donator} — {donation.amount:,.2f} ₽" 
            for (index, donation) in enumerate(top_donations_list) 
        ]),
        "\n"
    ]) if len(top_donations_list) > 0 else ""

    return top_donators


def generate_platform_code(user_id: int) -> str:
    modified_user_id_digits: List[int] = list(map(int, str(user_id + USER_ID_MODIFIER)))
    platform_code_characters: List[str] = list(map(lambda digit: chr(digit + DIGIT_MODIFIER), modified_user_id_digits))
    
    return "".join([ "".join(platform_code_characters), PLATFORM_CODE_SUFFIX ])

def decode_platform_code(platform_code: str) -> Optional[int]:
    if not platform_code.endswith(PLATFORM_CODE_SUFFIX): return None

    platform_code = platform_code.replace(PLATFORM_CODE_SUFFIX, "")

    if any(platform_code_character not in POSSIBLE_PLATFORM_CODE_CHARACTERS for platform_code_character in platform_code): return None

    modified_user_id_digits: List[int] = list(map(lambda character: ord(character) - DIGIT_MODIFIER, platform_code))
    modified_user_id: int = int("".join(map(str, modified_user_id_digits)))

    return modified_user_id - USER_ID_MODIFIER
