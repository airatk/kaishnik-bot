from peewee import AutoField
from peewee import BigIntegerField
from peewee import BooleanField

from bot.models.base.base import Base


class Users(Base):
    user_id: AutoField = AutoField()
    
    telegram_id: BigIntegerField = BigIntegerField(unique=True, null=True, index=True)
    vk_id: BigIntegerField = BigIntegerField(unique=True, null=True, index=True)
    
    is_setup: BooleanField = BooleanField(default=False)
