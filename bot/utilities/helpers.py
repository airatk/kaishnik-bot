from datetime import date

from bot.models.metrics import Metrics

from bot.utilities.types import Commands


def increment_command_metrics(command: Commands):
    def outter(func):
        async def inner(arg):
            (metrics, _) = Metrics.get_or_create(date=date.today().strftime("%Y-%m-%d"))
            
            if command is Commands.NO_PERMISSIONS: metrics.no_permissions += 1
            elif command is Commands.CANCEL: metrics.cancel += 1
            elif command is Commands.START: metrics.start += 1
            elif command is Commands.LOGIN: metrics.login += 1
            elif command is Commands.UNLOGIN: metrics.unlogin += 1
            elif command is Commands.CLASSES: metrics.classes += 1
            elif command is Commands.EXAMS: metrics.exams += 1
            elif command is Commands.LECTURERS: metrics.lecturers += 1
            elif command is Commands.SCORE: metrics.score += 1
            elif command is Commands.NOTES: metrics.notes += 1
            elif command is Commands.EDIT: metrics.edit += 1
            elif command is Commands.LOCATIONS: metrics.locations += 1
            elif command is Commands.WEEK: metrics.week += 1
            elif command is Commands.BRS: metrics.brs += 1
            elif command is Commands.HELP: metrics.help += 1
            elif command is Commands.DONATE: metrics.donate += 1
            elif command is Commands.DICE: metrics.dice += 1
            elif command is Commands.SETTINGS: metrics.settings += 1
            elif command is Commands.UNKNOWN_NONTEXT_MESSAGE: metrics.unknown_nontext_message += 1
            elif command is Commands.UNKNOWN_TEXT_MESSAGE: metrics.unknown_text_message += 1
            elif command is Commands.UNKNOWN_CALLBACK: metrics.unknown_callback += 1
            
            metrics.save()
            
            await func(arg)
        return inner
    return outter
