import sqlite3
from config.settings import DATABASE_CONFIG

class Database:
    _instance = None  # Singleton per la connessione al database

    def __new__(cls):
        """Implementa il pattern Singleton per mantenere una singola connessione al database."""
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            try:
                cls._instance.conn = sqlite3.connect(
                    DATABASE_CONFIG["dbname"], check_same_thread=False
                )
                cls._instance.cur = cls._instance.conn.cursor()
                print("Connessione al database SQLite riuscita.")
            except sqlite3.Error as e:
                print(f"Errore durante la connessione al database: {e}")
                cls._instance = None
        return cls._instance

    def execute_query(self, query, params=()):
        """Esegue una query di modifica (INSERT, UPDATE, DELETE) con gestione errori."""
        if not hasattr(self, "conn") or self.conn is None:
            raise ConnectionError("La connessione al database non è attiva.")
        
        try:
            self.cur.execute(query, params)
            self.conn.commit()
        except sqlite3.IntegrityError:
            print("Errore: Violazione di vincolo di unicità.")
        except sqlite3.OperationalError as e:
            print(f"Errore SQL: {e}")
        except sqlite3.Error as e:
            print(f"Errore generico nel database: {e}")

    def fetch_results(self, query, params=()):
        """Esegue una query di selezione e restituisce i risultati."""
        if not hasattr(self, "conn") or self.conn is None:
            raise ConnectionError("La connessione al database non è attiva.")
        
        try:
            self.cur.execute(query, params)
            return self.cur.fetchall()
        except sqlite3.Error as e:
            print(f"Errore nella query: {e}")
            return None

    def close_connection(self):
        """Chiude la connessione al database in modo sicuro."""
        if hasattr(self, "conn") and self.conn:
            self.conn.close()
            Database._instance = None  # Resetta il Singleton
            print("Connessione SQLite chiusa.")

    def __del__(self):
        """Chiusura sicura della connessione quando l'istanza viene distrutta."""
        self.close_connection()
