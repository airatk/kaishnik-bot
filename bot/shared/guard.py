from aiogram.types import Message


class Guard:
    def __init__(self):
        self._text: str = None
        self._message: Message = None


    @property
    def text(self) -> str:
        return self._text

    @property
    def message(self) -> Message:
        return self._message


    @text.setter
    def text(self, text: str):
        self._text = text

    @message.setter
    def message(self, message: Message):
        self._message = message


    def drop(self):
        self.__init__()
