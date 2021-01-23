from peewee import TextField

from bot.models.base.students import Students


class CompactStudents(Students):
    group: TextField = TextField(null=True)
    group_schedule_id: TextField = TextField(null=True)
