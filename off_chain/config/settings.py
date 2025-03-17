import os

# Ottieni il percorso assoluto della cartella config
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Percorso del database all'interno della cartella config
DB_PATH = os.path.join(BASE_DIR, 'database.db')

# Configurazione database
DATABASE_CONFIG = {
    "ENGINE": "sqlite3",
    "NAME": DB_PATH,
}
