from bot.shared.commands import Commands

from datetime import datetime


class Metrics:
    def __init__(self):
        self.day: int = datetime.today().isoweekday()
        
        self.no_permissions: int = 0
        self.cancel: int = 0
        self.start: int = 0
        self.login: int = 0
        self.unlogin: int = 0
        self.classes: int = 0
        self.exams: int = 0
        self.lecturers: int = 0
        self.score: int = 0
        self.notes: int = 0
        self.edit: int = 0
        self.locations: int = 0
        self.week: int = 0
        self.brs: int = 0
        self.help: int = 0
        self.donate: int = 0
        self.dice: int = 0
        self.settings: int = 0
        self.unknown_nontext_message: int = 0
        self.unknown_text_message: int = 0
        self.unknown_callback: int = 0
    
    
    @property
    def sum(self) -> int:
        return (
            self.no_permissions +
            self.cancel +
            self.start +
            self.login +
            self.unlogin +
            self.classes +
            self.exams +
            self.lecturers +
            self.score +
            self.notes +
            self.edit +
            self.locations +
            self.week +
            self.brs +
            self.help +
            self.donate +
            self.dice +
            self.settings +
            self.unknown_nontext_message +
            self.unknown_text_message +
            self.unknown_callback
        )
    
    
    def drop(self):
        self.__init__()
    
    def increment(self, command: Commands):
        def outter(func):
            async def inner(arg):
                if self.day != datetime.today().isoweekday(): self.drop()
                
                if command is Commands.NO_PERMISSIONS: self.no_permissions += 1
                elif command is Commands.CANCEL: self.cancel += 1
                elif command is Commands.START: self.start += 1
                elif command is Commands.LOGIN: self.login += 1
                elif command is Commands.UNLOGIN: self.unlogin += 1
                elif command is Commands.CLASSES: self.classes += 1
                elif command is Commands.EXAMS: self.exams += 1
                elif command is Commands.LECTURERS: self.lecturers += 1
                elif command is Commands.SCORE: self.score += 1
                elif command is Commands.NOTES: self.notes += 1
                elif command is Commands.EDIT: self.edit += 1
                elif command is Commands.LOCATIONS: self.locations += 1
                elif command is Commands.WEEK: self.week += 1
                elif command is Commands.BRS: self.brs += 1
                elif command is Commands.HELP: self.help += 1
                elif command is Commands.DONATE: self.donate += 1
                elif command is Commands.DICE: self.dice += 1
                elif command is Commands.SETTINGS: self.settings += 1
                elif command is Commands.UNKNOWN_NONTEXT_MESSAGE: self.unknown_nontext_message += 1
                elif command is Commands.UNKNOWN_TEXT_MESSAGE: self.unknown_text_message += 1
                elif command is Commands.UNKNOWN_CALLBACK: self.unknown_callback += 1
                
                await func(arg)
            return inner
        return outter
