from vk_api import VkApi

from vk_api.utils import get_random_id

from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType

from vk_api.keyboard import VkKeyboard
from vk_api.keyboard import VkKeyboardColor

from datetime import datetime

from .schedule import get_schedule

from .constants import TOKEN
from .constants import GROUP_ID
from .constants import WEEKDAYS


class Bot:
    def __init__(self):
        self._token = TOKEN
        self._group_id = GROUP_ID
        
        self._session = VkApi(token=self._token)
        self._api = self._session.get_api()
        
        self._longpoll = VkBotLongPoll(self._session, self._group_id)
    
    def start(self):
        print("Launched!")
        
        for event in self._longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if "анятия" in event.object.text:
                    keyboard = VkKeyboard(one_time=True)
                    
                    keyboard.add_button("сегодня", color=VkKeyboardColor.PRIMARY)
                    keyboard.add_button("завтра", color=VkKeyboardColor.PRIMARY)
                    
                    keyboard.add_line(); keyboard.add_button("текущую неделю", color=VkKeyboardColor.DEFAULT)
                    keyboard.add_line(); keyboard.add_button("следующую неделю", color=VkKeyboardColor.DEFAULT)
                
                    self._api.messages.send(
                        peer_id=event.object.from_id,
                        random_id=get_random_id(),
                        keyboard=keyboard.get_keyboard(),
                        message="Тебе нужно расписание занятий на:"
                    )
                elif event.object.text == "сегодня":
                    self._api.messages.send(
                        peer_id=event.object.from_id,
                        random_id=get_random_id(),
                        message=get_schedule(
                            type="classes",
                            weekday=datetime.today().isoweekday()
                        )
                    )
                elif event.object.text == "завтра":
                    self._api.messages.send(
                        peer_id=event.object.from_id,
                        random_id=get_random_id(),
                        message=get_schedule(
                            type="classes",
                            weekday=datetime.today().isoweekday() + 1
                        )
                    )
                elif event.object.text == "текущую неделю":
                    for weekday in WEEKDAYS:
                        self._api.messages.send(
                            peer_id=event.object.from_id,
                            random_id=get_random_id(),
                            message=get_schedule(
                                type="classes",
                                weekday=weekday
                            )
                        )
                elif event.object.text == "следующую неделю":
                    for weekday in WEEKDAYS:
                        self._api.messages.send(
                            peer_id=event.object.from_id,
                            random_id=get_random_id(),
                            message=get_schedule(
                                type="classes",
                                weekday=weekday,
                                next=True
                            )
                        )
                elif "кзамены" in event.object.text:
                    self._api.messages.send(
                        peer_id=event.object.from_id,
                        random_id=get_random_id(),
                        message=get_schedule(type="exams")
                    )
                else:
                    keyboard = VkKeyboard(one_time=True)
                    
                    keyboard.add_button("занятия", color=VkKeyboardColor.PRIMARY)
                    keyboard.add_button("экзамены", color=VkKeyboardColor.PRIMARY)
                
                    self._api.messages.send(
                        peer_id=event.object.from_id,
                        random_id=get_random_id(),
                        keyboard=keyboard.get_keyboard(),
                        message="Занятия или экзамены?"
                    )
