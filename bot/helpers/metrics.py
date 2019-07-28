from datetime import datetime


class Metrics:
    def __init__(self):
        self._day = datetime.today().isoweekday()
        self._classes = 0
        self._score = 0
        self._lecturers = 0
        self._week = 0
        self._notes = 0
        self._exams = 0
        self._locations = 0
        self._card = 0
        self._brs = 0
        self._me = 0
        self._cancel = 0
        self._start = 0
        self._settings = 0
        self._unsetup = 0
        self._edit = 0
        self._help = 0
        self._donate = 0
        self._unknown = 0
    
    @property
    def day(self):
        return self._day
    
    @property
    def classes(self):
        return self._classes
    
    @property
    def score(self):
        return self._score
    
    @property
    def lecturers(self):
        return self._lecturers
    
    @property
    def week(self):
        return self._week
    
    @property
    def notes(self):
        return self._notes
    
    @property
    def exams(self):
        return self._exams
    
    @property
    def locations(self):
        return self._locations
    
    @property
    def card(self):
        return self._card
    
    @property
    def brs(self):
        return self._brs
    
    @property
    def me(self):
        return self._me
    
    @property
    def cancel(self):
        return self._cancel
    
    @property
    def start(self):
        return self._start
    
    @property
    def settings(self):
        return self._settings
    
    @property
    def unsetup(self):
        return self._unsetup
    
    @property
    def edit(self):
        return self._edit
    
    @property
    def help(self):
        return self._help
    
    @property
    def donate(self):
        return self._donate
    
    @property
    def unknown(self):
        return self._unknown
    
    @property
    def sum(self):
        return (
            self._classes +
            self._score +
            self._lecturers +
            self._week +
            self._notes +
            self._exams +
            self._locations +
            self._card +
            self._brs +
            self._me +
            self._cancel +
            self._start +
            self._settings +
            self._unsetup +
            self._edit +
            self._help +
            self._donate +
            self._unknown
        )
    
    def zerofy(self):
        self._day = datetime.today().isoweekday()
        self._classes = 0
        self._score = 0
        self._lecturers = 0
        self._week = 0
        self._notes = 0
        self._exams = 0
        self._locations = 0
        self._card = 0
        self._brs = 0
        self._me = 0
        self._cancel = 0
        self._start = 0
        self._settings = 0
        self._unsetup = 0
        self._edit = 0
        self._help = 0
        self._donate = 0
        self._unknown = 0
    
    def increment(self, command):
        def decorator(func):
            def wrapper(arg):
                if self._day != datetime.today().isoweekday(): self.zerofy()
                
                if command == "classes": self._classes += 1
                elif command == "score": self._score += 1
                elif command == "lecturers": self._lecturers += 1
                elif command == "week": self._week += 1
                elif command == "notes": self._notes += 1
                elif command == "exams": self._exams += 1
                elif command == "locations": self._locations += 1
                elif command == "card": self._card += 1
                elif command == "brs": self._brs += 1
                elif command == "me": self._me += 1
                elif command == "cancel": self._cancel += 1
                elif command == "start": self._start += 1
                elif command == "settings": self._settings += 1
                elif command == "unsetup": self._unsetup += 1
                elif command == "edit": self._edit += 1
                elif command == "help": self._help += 1
                elif command == "donate": self._donate += 1
                elif command == "unknown": self._unknown += 1
                
                func(arg)
            return wrapper
        return decorator
