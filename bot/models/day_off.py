from peewee import TextField
from peewee import Check

from bot.models.base import Base


class DayOff(Base):
    day: TextField = TextField(primary_key=True, index=True, constraints=[ Check("day LIKE '__-__'") ])
    
    message: TextField = TextField(default="Выходной")
