from peewee import PostgresqlDatabase


POSTGRESQL_DATABASE_NAME: str = "kaist_db"
DATABASE: PostgresqlDatabase = PostgresqlDatabase(POSTGRESQL_DATABASE_NAME)
