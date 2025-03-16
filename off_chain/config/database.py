import os
import sqlite3

class Database:
    def __init__(self, db_path='database.db'):
        # Percorso assoluto del database nella cartella del progetto
        if db_path == 'database.db':  # Se viene usato il percorso di default
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.db_path = os.path.join(BASE_DIR, db_path)
        else:
            self.db_path = db_path

        # Controlla che il database esista prima di connettersi
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Database non trovato: {self.db_path}")

    def get_connection(self):
        # Connessione al database esistente
        conn = sqlite3.connect(self.db_path)
        return conn