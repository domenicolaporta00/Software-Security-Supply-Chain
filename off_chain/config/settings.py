import os
from dotenv import load_dotenv

load_dotenv()  # Carica le variabili d’ambiente dal file .env

class Settings:
    DB_HOST = os.getenv("DATABASE_HOST", "localhost")
    DB_PORT = os.getenv("DATABASE_PORT", "5432")
    DB_NAME = os.getenv("DATABASE_NAME", "my_database")
    DB_USER = os.getenv("DATABASE_USER", "my_user")
    DB_PASSWORD = os.getenv("DATABASE_PASSWORD", "my_password")
