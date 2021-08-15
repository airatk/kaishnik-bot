from typing import List
from typing import Optional

from datetime import date

from bot.models.metrics import Metrics

from bot.utilities.constants import POSSIBLE_PLATFORM_CODE_CHARACTERS, USER_ID_MODIFIER
from bot.utilities.constants import DIGIT_MODIFIER
from bot.utilities.constants import PLATFORM_CODE_SUFFIX
from bot.utilities.types import Commands


def increment_command_metrics(command: Commands):
    def outter(func):
        async def inner(arg):
            (last_metrics, _) = Metrics.get_or_create(date=date.today().strftime("%Y-%m-%d"))
            
            if command is Commands.NO_PERMISSIONS: last_metrics.no_permissions += 1
            elif command is Commands.CANCEL: last_metrics.cancel += 1
            elif command is Commands.START: last_metrics.start += 1
            elif command is Commands.RESTART: last_metrics.restart += 1
            elif command is Commands.LOGIN: last_metrics.login += 1
            elif command is Commands.UNLOGIN: last_metrics.unlogin += 1
            elif command is Commands.MENU: last_metrics.menu += 1
            elif command is Commands.MORE: last_metrics.more += 1
            elif command is Commands.CLASSES: last_metrics.classes += 1
            elif command is Commands.EXAMS: last_metrics.exams += 1
            elif command is Commands.LECTURERS: last_metrics.lecturers += 1
            elif command is Commands.SCORE: last_metrics.score += 1
            elif command is Commands.NOTES: last_metrics.notes += 1
            elif command is Commands.LOCATIONS: last_metrics.locations += 1
            elif command is Commands.WEEK: last_metrics.week += 1
            elif command is Commands.BRS: last_metrics.brs += 1
            elif command is Commands.HELP: last_metrics.help += 1
            elif command is Commands.DONATE: last_metrics.donate += 1
            elif command is Commands.DICE: last_metrics.dice += 1
            elif command is Commands.SETTINGS: last_metrics.settings += 1
            elif command is Commands.EDIT: last_metrics.edit += 1
            elif command is Commands.UNKNOWN_NONTEXT_MESSAGE: last_metrics.unknown_nontext_message += 1
            elif command is Commands.UNKNOWN_TEXT_MESSAGE: last_metrics.unknown_text_message += 1
            elif command is Commands.UNKNOWN_CALLBACK: last_metrics.unknown_callback += 1
            
            last_metrics.save()
            
            await func(arg)
        return inner
    return outter


def clarify_markdown(string: str) -> str:
    index: int = 0
    is_single: bool = False
    
    for (letter_index, letter) in enumerate(string):
        if letter in [ "*", "_" ]:
            (index, is_single) = (letter_index, not is_single)
    
    return "\\".join([ string[:index], string[index:] ]) if is_single else string

def remove_markdown(string: str) -> str:
    return string.replace("*", "").replace("_", "").replace("`", "")


def generate_platform_code(user_id: int) -> str:
    modified_user_id_digits: List[int] = list(map(int, str(user_id + USER_ID_MODIFIER)))
    plarform_code_characters: List[str] = list(map(lambda digit: chr(digit + DIGIT_MODIFIER), modified_user_id_digits))
    
    return "".join([ "".join(plarform_code_characters), PLATFORM_CODE_SUFFIX ])

def decode_platform_code(platform_code: str) -> Optional[int]:
    if not platform_code.endswith(PLATFORM_CODE_SUFFIX): return None

    platform_code = platform_code.replace(PLATFORM_CODE_SUFFIX, "")

    if any([ 
        platform_code_character not in POSSIBLE_PLATFORM_CODE_CHARACTERS 
        for platform_code_character in platform_code 
    ]): return None

    modified_user_id_digits: List[int] = list(map(lambda character: ord(character) - DIGIT_MODIFIER, platform_code))
    modified_user_id: int = int("".join(map(lambda digit: str(digit), modified_user_id_digits)))

    return (modified_user_id - USER_ID_MODIFIER)
