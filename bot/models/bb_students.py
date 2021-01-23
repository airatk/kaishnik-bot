from peewee import TextField

from bot.models.base.students import Students


class BBStudents(Students):
    login: TextField = TextField(null=True)
    password: TextField = TextField(null=True)
