from bot.shared.commands import Commands

from datetime import datetime


class Metrics:
    def __init__(self):
        self._day: int = datetime.today().isoweekday()
        
        self._cancel: int = 0
        self._start: int = 0
        self._login: int = 0
        self._unlogin: int = 0
        self._classes: int = 0
        self._exams: int = 0
        self._lecturers: int = 0
        self._score: int = 0
        self._notes: int = 0
        self._edit: int = 0
        self._locations: int = 0
        self._week: int = 0
        self._card: int = 0
        self._brs: int = 0
        self._help: int = 0
        self._donate: int = 0
        self._me: int = 0
        self._unknown: int = 0
    
    
    @property
    def day(self) -> int:
        return self._day
    
    
    @property
    def cancel(self) -> int:
        return self._cancel
    
    @property
    def start(self) -> int:
        return self._start
    
    @property
    def login(self) -> int:
        return self._login
    
    @property
    def unlogin(self) -> int:
        return self._unlogin
    
    @property
    def classes(self) -> int:
        return self._classes
    
    @property
    def exams(self) -> int:
        return self._exams
    
    @property
    def lecturers(self) -> int:
        return self._lecturers
    
    @property
    def score(self) -> int:
        return self._score
    
    @property
    def notes(self) -> int:
        return self._notes
    
    @property
    def edit(self) -> int:
        return self._edit
    
    @property
    def locations(self) -> int:
        return self._locations
    
    @property
    def week(self) -> int:
        return self._week
    
    @property
    def card(self) -> int:
        return self._card
    
    @property
    def brs(self) -> int:
        return self._brs
    
    @property
    def help(self) -> int:
        return self._help
    
    @property
    def donate(self) -> int:
        return self._donate
    
    @property
    def me(self) -> int:
        return self._me
    
    @property
    def unknown(self) -> int:
        return self._unknown
    
    
    @property
    def sum(self) -> int:
        return (
            self._cancel +
            self._start +
            self._login +
            self._unlogin +
            self._classes +
            self._exams +
            self._lecturers +
            self._score +
            self._notes +
            self._edit +
            self._locations +
            self._week +
            self._card +
            self._brs +
            self._help +
            self._donate +
            self._me +
            self._unknown
        )
    
    
    def drop(self):
        self.__init__()
    
    
    def increment(self, command: Commands):
        def outter(func):
            async def inner(arg):
                if self._day != datetime.today().isoweekday(): self.drop()
                
                if command is Commands.CANCEL: self._cancel += 1
                elif command is Commands.START: self._start += 1
                elif command is Commands.LOGIN: self._login += 1
                elif command is Commands.UNLOGIN: self._unlogin += 1
                elif command is Commands.CLASSES: self._classes += 1
                elif command is Commands.EXAMS: self._exams += 1
                elif command is Commands.LECTURERS: self._lecturers += 1
                elif command is Commands.SCORE: self._score += 1
                elif command is Commands.NOTES: self._notes += 1
                elif command is Commands.EDIT: self._edit += 1
                elif command is Commands.LOCATIONS: self._locations += 1
                elif command is Commands.WEEK: self._week += 1
                elif command is Commands.CARD: self._card += 1
                elif command is Commands.BRS: self._brs += 1
                elif command is Commands.HELP: self._help += 1
                elif command is Commands.DONATE: self._donate += 1
                elif command is Commands.ME: self._me += 1
                elif command is Commands.UNKNOWN: self._unknown += 1
                
                await func(arg)
            return inner
        return outter
