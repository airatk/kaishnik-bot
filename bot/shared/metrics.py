from bot.shared.commands import Commands

from datetime import datetime


class Metrics:
    def __init__(self):
        self._day = datetime.today().isoweekday()
        
        self._cancel = 0
        self._start = 0
        self._login = 0
        self._unlogin = 0
        self._classes = 0
        self._exams = 0
        self._lecturers = 0
        self._score = 0
        self._notes = 0
        self._edit = 0
        self._locations = 0
        self._week = 0
        self._card = 0
        self._brs = 0
        self._help = 0
        self._donate = 0
        self._me = 0
        self._unknown = 0
    
    
    @property
    def day(self):
        return self._day
    
    
    @property
    def cancel(self):
        return self._cancel
    
    @property
    def start(self):
        return self._start
    
    @property
    def login(self):
        return self._login
    
    @property
    def unlogin(self):
        return self._unlogin
    
    @property
    def classes(self):
        return self._classes
    
    @property
    def exams(self):
        return self._exams
    
    @property
    def lecturers(self):
        return self._lecturers
    
    @property
    def score(self):
        return self._score
    
    @property
    def notes(self):
        return self._notes
    
    @property
    def edit(self):
        return self._edit
    
    @property
    def locations(self):
        return self._locations
    
    @property
    def week(self):
        return self._week
    
    @property
    def card(self):
        return self._card
    
    @property
    def brs(self):
        return self._brs
    
    @property
    def help(self):
        return self._help
    
    @property
    def donate(self):
        return self._donate
    
    @property
    def me(self):
        return self._me
    
    @property
    def unknown(self):
        return self._unknown
    
    
    @property
    def sum(self):
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
    
    
    def increment(self, command):
        def outter(func):
            def inner(arg):
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
                
                func(arg)
            return inner
        return outter
