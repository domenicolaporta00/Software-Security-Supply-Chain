from sqlite3 import IntegrityError

import pyotp

from database_domenico.db_login import DatabaseLogin, UniqueConstraintError, DatabaseError, \
    PasswordTooShortError, PasswordWeakError

from services.auth_service import AuthService


class ControllerAutenticazione:
    def __init__(self):
        self.database = DatabaseLogin()
        self.auth_service = AuthService()


    # Effettua la registrazione
    def registrazione(self, username, password, tipo, indirizzo):
        """Tenta di aggiungere un utente, gestendo eventuali errori."""
        try:
            # Genera una chiave segreta per l'autenticazione a due fattori
            secret_key = pyotp.random_base32()

            self.auth_service

            # Inserisce le credenziali e la chiave segreta nel database
            self.database.inserisci_credenziali_e_azienda(username, password, tipo, indirizzo, secret_key)

            # Restituisce il successo insieme alla chiave segreta
            return True, "Utente registrato con successo!", secret_key
        
        except PasswordTooShortError as e:
            return False, str(e), None
        except PasswordWeakError as e:
            return False, str(e), None
        except UniqueConstraintError:
            return False, "Errore: Username già esistente.", None
        except DatabaseError:
            return False, "Errore nel database.", None

    def login(self, username, password, otp_code):
        try:
            result = self.auth_service.login(username, password)
            return result  # Può essere mostrato in una GUI o come risposta JSON
        except ValueError as e:
            return {"error": str(e)}