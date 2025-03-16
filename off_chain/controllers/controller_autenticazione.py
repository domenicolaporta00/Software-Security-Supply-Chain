from sqlite3 import IntegrityError

import bcrypt

from database_domenico.db_login import DatabaseLogin, UniqueConstraintError, DatabaseError, \
    PasswordTooShortError, PasswordWeakError


class ControllerAutenticazione:
    def __init__(self):
        self.database = DatabaseLogin()

    # Effettua la registrazione
    def registrazione(self, username, password, tipo, indirizzo):
        """Tenta di aggiungere un utente, gestendo eventuali errori."""
        try:
            # Inserisce le credenziali nel database (senza chiave segreta OTP)
            self.database.inserisci_credenziali_e_azienda(username, password, tipo, indirizzo, secret_key=None)

            # Restituisce il successo
            return True, "Utente registrato con successo!", None
        except PasswordTooShortError as e:
            return False, str(e), None
        except PasswordWeakError as e:
            return False, str(e), None
        except UniqueConstraintError:
            return False, "Errore: Username già esistente.", None
        except DatabaseError:
            return False, "Errore nel database.", None

    def login(self, username, password, otp_code=None):
        # Recupera le credenziali dell'utente specifico
        credenziale = self.database.get_credenziale_by_username(username)

        if not credenziale:
            return None, "Username non trovato!"  # Username non trovato

        id_ = credenziale[0]
        password_hash = credenziale[2]  # La password hashata salvata nel database

        if password != password_hash:
            return None, "Password errata!"

        # Recupera l'azienda associata
        azienda = self.database.get_azienda_by_id(id_)
        return (azienda[0], "Accesso effettuato correttamente!") if azienda \
            else (None, "Errore!")