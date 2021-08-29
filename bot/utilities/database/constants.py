from peewee import PostgresqlDatabase

from bot.utilities.constants import KEYS


DATABASE: PostgresqlDatabase = PostgresqlDatabase(database=KEYS.POSTGRESQL_DATABASE_NAME)
