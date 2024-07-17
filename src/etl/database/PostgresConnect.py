import psycopg2
from config import settings
from psycopg2 import sql


class PostgresConnect:
    def __init__(self, db):
        self.db = db if db is not None else settings.postgres_db
        self.user = settings.postgres_user
        self.password = settings.postgres_password.get_secret_value()
        self.host = settings.postgres_host
        self.port = settings.postgres_port

    def connect(self):
        self.conn = psycopg2.connect(
            dbname=self.db,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
        )
        return self.conn

    def close(self):
        self.conn.close()

    def execute(self, sql: sql.SQL):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        self.conn.commit()
        cursor.close()
