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

    def execute_query(self, query, params=()):
        """Esegue query di modifica (INSERT, UPDATE, DELETE)."""
        try:
            self.cur.execute(query, params)
            self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            raise RuntimeError(f"Errore database: {e}")

    def fetch_query(self, query, params=()):
        """Esegue una SELECT e restituisce i risultati."""
        try:
            self.cur.execute(query, params)
            return self.cur.fetchall()
        except psycopg2.Error as e:
            raise RuntimeError(f"Errore database: {e}")
        
    def close_connection(self):
        if self.connection:
            self.connection.close()
            self._instance = None
