from datetime import date

from bot.models.metrics import Metrics

from bot.utilities.types import Commands


def increment_command_metrics(command: Commands):
    def outter(func):
        async def inner(arg):
            (last_metrics, _) = Metrics.get_or_create(date=date.today().strftime("%Y-%m-%d"))
            
            if command is Commands.NO_PERMISSIONS: last_metrics.no_permissions += 1
            elif command is Commands.CANCEL: last_metrics.cancel += 1
            elif command is Commands.START: last_metrics.start += 1
            elif command is Commands.LOGIN: last_metrics.login += 1
            elif command is Commands.UNLOGIN: last_metrics.unlogin += 1
            elif command is Commands.CLASSES: last_metrics.classes += 1
            elif command is Commands.EXAMS: last_metrics.exams += 1
            elif command is Commands.LECTURERS: last_metrics.lecturers += 1
            elif command is Commands.SCORE: last_metrics.score += 1
            elif command is Commands.NOTES: last_metrics.notes += 1
            elif command is Commands.EDIT: last_metrics.edit += 1
            elif command is Commands.LOCATIONS: last_metrics.locations += 1
            elif command is Commands.WEEK: last_metrics.week += 1
            elif command is Commands.BRS: last_metrics.brs += 1
            elif command is Commands.HELP: last_metrics.help += 1
            elif command is Commands.DONATE: last_metrics.donate += 1
            elif command is Commands.DICE: last_metrics.dice += 1
            elif command is Commands.SETTINGS: last_metrics.settings += 1
            elif command is Commands.UNKNOWN_NONTEXT_MESSAGE: last_metrics.unknown_nontext_message += 1
            elif command is Commands.UNKNOWN_TEXT_MESSAGE: last_metrics.unknown_text_message += 1
            elif command is Commands.UNKNOWN_CALLBACK: last_metrics.unknown_callback += 1
            
            last_metrics.save()
            
            await func(arg)
        return inner
    return outter
