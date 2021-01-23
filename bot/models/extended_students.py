from peewee import TextField

from bot.models.base.students import Students


class ExtendedStudents(Students):
    institute: TextField = TextField(null=True)
    institute_id: TextField = TextField(null=True)
    year: TextField = TextField(null=True)
    group: TextField = TextField(null=True)
    group_schedule_id: TextField = TextField(null=True)
    group_score_id: TextField = TextField(null=True)
    name: TextField = TextField(null=True)
    name_id: TextField = TextField(null=True)
    card: TextField = TextField(null=True)
