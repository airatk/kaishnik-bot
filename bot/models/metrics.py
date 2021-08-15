from peewee import TextField
from peewee import IntegerField
from peewee import Check

from bot.models.base.base import Base


class Metrics(Base):
    date: TextField = TextField(primary_key=True, index=True, constraints=[ Check("date LIKE '____-__-__'") ])
    
    classes: IntegerField = IntegerField(default=0)
    score: IntegerField = IntegerField(default=0)
    lecturers: IntegerField = IntegerField(default=0)
    notes: IntegerField = IntegerField(default=0)
    week: IntegerField = IntegerField(default=0)
    exams: IntegerField = IntegerField(default=0)
    dice: IntegerField = IntegerField(default=0)
    locations: IntegerField = IntegerField(default=0)
    brs: IntegerField = IntegerField(default=0)
    settings: IntegerField = IntegerField(default=0)
    edit: IntegerField = IntegerField(default=0)
    help: IntegerField = IntegerField(default=0)
    donate: IntegerField = IntegerField(default=0)
    
    menu: IntegerField = IntegerField(default=0)
    more: IntegerField = IntegerField(default=0)

    cancel: IntegerField = IntegerField(default=0)
    
    start: IntegerField = IntegerField(default=0)
    login: IntegerField = IntegerField(default=0)
    
    unknown_nontext_message: IntegerField = IntegerField(default=0)
    unknown_text_message: IntegerField = IntegerField(default=0)
    unknown_callback: IntegerField = IntegerField(default=0)
    
    no_permissions: IntegerField = IntegerField(default=0)
    unlogin: IntegerField = IntegerField(default=0)
    restart: IntegerField = IntegerField(default=0)
