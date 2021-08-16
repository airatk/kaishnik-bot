from peewee import AutoField
from peewee import FloatField
from peewee import DateField
from peewee import TextField

from bot.models.base.base import Base


class Donations(Base):
    donation_id: AutoField = AutoField()

    amount: FloatField = FloatField()
    date: DateField = DateField()
    name: TextField = TextField()
