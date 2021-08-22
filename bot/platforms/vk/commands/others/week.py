from datetime import datetime

from vkwave.bots import SimpleBotEvent

from bot.platforms.vk import vk_bot
from bot.platforms.vk import guards

from bot.platforms.vk.utilities.keyboards import to_menu
from bot.platforms.vk.utilities.types import CommandOfVK

from bot.utilities.helpers import note_metrics
from bot.utilities.types import Platform
from bot.utilities.types import Command
from bot.utilities.calendar.helpers import is_week_even
from bot.utilities.calendar.helpers import weekday_date
from bot.utilities.calendar.helpers import get_week_number


@vk_bot.message_handler(
    lambda event:
        guards[event.object.object.message.peer_id].text is None and
        event.object.object.message.text.capitalize() == CommandOfVK.WEEK.value
)
@note_metrics(platform=Platform.VK, command=Command.WEEK)
async def week(event: SimpleBotEvent):
    (weekday, date) = weekday_date()
    
    week_number: int = get_week_number(day_date=datetime.today())
    
    if week_number > 0:
        week_message: str = (
            "Текущая неделя {type},\n"
            "#{number} с начала семестра.".format(
                type="чётная" if is_week_even(day_date=datetime.today()) else "нечётная",
                number=week_number
            )
        )
    else:
        week_number = 1 - week_number
        
        week_message: str = "До начала семестра меньше {week_number} недел{ending}.".format(
            week_number=week_number,
            ending="и" if week_number == 1 else "ь"
        )
    
    await event.answer(
        message="\n\n".join([
            "{weekday}, {date}".format(weekday=weekday, date=date),
            week_message
        ]),
        keyboard=to_menu()
    )
