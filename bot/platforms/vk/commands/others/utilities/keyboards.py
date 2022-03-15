from vkwave.bots.utils.keyboards import Keyboard
from vkwave.bots.utils.keyboards import VKPayActionTransferToGroup

from bot.platforms.vk.utilities.keyboards import menu_button

from bot.utilities.constants import KEYS


def via_vk_pay() -> str:
    vk_pay_keyboard: Keyboard = Keyboard(one_time=True, inline=True)

    vk_pay_keyboard.add_vkpay_button(hash_action=VKPayActionTransferToGroup(group_id=KEYS["VK_GROUP"]))

    vk_pay_keyboard.add_row()
    vk_pay_keyboard.add_text_button(**menu_button())

    return vk_pay_keyboard.get_keyboard()
