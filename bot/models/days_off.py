from peewee import TextField
from peewee import Check

from bot.models.base.base import Base


class DaysOff(Base):
    date: TextField = TextField(primary_key=True, index=True, constraints=[ Check("date LIKE '__-__'") ])
    
    message: TextField = TextField(default="Выходной")
