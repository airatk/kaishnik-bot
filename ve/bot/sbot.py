from vk_api import VkApi

from vk_api.utils import get_random_id

from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType

from vk_api.keyboard import VkKeyboard
from vk_api.keyboard import VkKeyboardColor

from datetime import datetime
from random import choice

from schedule import every
from schedule import run_pending

from time import sleep

from .schedule import get_schedule

from .constants import TOKEN
from .constants import GROUP_ID
from .constants import PEER_ID

from .constants import WEEKDAYS
from .constants import REPLIES_TO_UNKNOWN_MESSAGE


class Bot:
    def __init__(self):
        self._token = TOKEN
        self._group_id = GROUP_ID
        self._peer_id = PEER_ID
        
        self._session = VkApi(token=self._token)
        self._api = self._session.get_api()
        
        self._longpoll = VkBotLongPoll(self._session, self._group_id)
    
    def notification(self):
        every().day.at("18:00").do(self.tomorrow, True)
        
        while True:
            run_pending()
            sleep(1)
    
    def tomorrow(self, is_pin=False):
        self._api.messages.send(
            peer_id=self._peer_id,
            random_id=get_random_id(),
            message=get_schedule(
                type="classes",
                weekday=datetime.today().isoweekday() + 1
            )
        )
    
        #if is_pin:
        #    self._api.messages.pin(
        #        peer_id=self._peer_id,
        #        message_id=self._api.messages.get_history(
        #            peer_id=self._peer_id,
        #            count=1
        #        )[0].id
        #    )
    
    def start(self):
        print("Launched!")
        
        for event in self._longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if "|" in event.object.text:
                    try:
                        event.object.text = event.object.text.split()[1]
                    except Exception:
                        pass

                if "команды" in event.object.text:
                    self._api.messages.send(
                        peer_id=event.object.peer_id,
                        random_id=get_random_id(),
                        message=(
                            "Команды:\n"
                            "• сегодня\n"
                            "• завтра\n"
                            "• чётная\n"
                            "• нечётная\n"
                            "◦ экзамены\n"
                        )
                    )
                elif "сегодня" in event.object.text:
                    self._api.messages.send(
                        peer_id=event.object.peer_id,
                        random_id=get_random_id(),
                        message=get_schedule(
                            type="classes",
                            weekday=datetime.today().isoweekday()
                        )
                    )
                elif "завтра" in event.object.text:
                    self.tomorrow()
                elif "чётная" in event.object.text:
                    for weekday in WEEKDAYS:
                        self._api.messages.send(
                            peer_id=event.object.peer_id,
                            random_id=get_random_id(),
                            message=get_schedule(
                                type="classes",
                                weekday=weekday
                            )
                        )
                elif "нечётная" in event.object.text:
                    for weekday in WEEKDAYS:
                        self._api.messages.send(
                            peer_id=event.object.peer_id,
                            random_id=get_random_id(),
                            message=get_schedule(
                                type="classes",
                                weekday=weekday,
                                next=True
                            )
                        )
                elif "экзамены" in event.object.text:
                    self._api.messages.send(
                        peer_id=event.object.peer_id,
                        random_id=get_random_id(),
                        message=get_schedule(type="exams")
                    )
                else:
                    self._api.messages.send(
                        peer_id=event.object.peer_id,
                        random_id=get_random_id(),
                        message=choice(REPLIES_TO_UNKNOWN_MESSAGE)
                    )
