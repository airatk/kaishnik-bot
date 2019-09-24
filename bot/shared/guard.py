class Guard:
    def __init__(self):
        self._text = None
        self._message = None


    @property
    def text(self):
        return self._text

    @property
    def message(self):
        return self._message


    @text.setter
    def text(self, text):
        self._text = text

    @message.setter
    def message(self, message):
        self._message = message


    def drop(self):
        self.__init__()
