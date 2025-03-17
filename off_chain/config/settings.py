import os
from dotenv import load_dotenv

#TODO aggiustare path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE_CONFIG = {
    "dbname": os.path.join(BASE_DIR, "database.db")
}

