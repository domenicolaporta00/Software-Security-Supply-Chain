import psycopg2
from config.settings import Settings

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._connect()
        return cls._instance

    def _connect(self):
        self.connection = psycopg2.connect(
            dbname=Settings.DB_NAME,
            user=Settings.DB_USER,
            password=Settings.DB_PASSWORD,
            host=Settings.DB_HOST,
            port=Settings.DB_PORT
        )

    def get_connection(self):
        return self.connection

    def close_connection(self):
        if self.connection:
            self.connection.close()
            self._instance = None
