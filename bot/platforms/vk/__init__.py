from typing import Dict

from vkwave.bots import SimpleLongPollBot

from bot.models.user import User

from bot.utilities.constants import KEYS
from bot.utilities.types import Guard
from bot.utilities.types import State


vk_bot: SimpleLongPollBot = SimpleLongPollBot(
    tokens=[ 
        KEYS.VK_TOKEN_1,
        KEYS.VK_TOKEN_2,
        KEYS.VK_TOKEN_3,
        KEYS.VK_TOKEN_4
    ], 
    group_id=KEYS.VK_GROUP
)

guards: Dict[int, Guard] = { user.vk_id: Guard() for user in User.select(User.vk_id) }
states: Dict[int, State] = { user.vk_id: State() for user in User.select(User.vk_id) }


from bot.platforms.vk import commands
