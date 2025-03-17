from dataclasses import dataclass
import re
import bcrypt


@dataclass
class CredentialModel:
    """
    Data Transfer Object (DTO) for user authentication.
    """
    Id_credential: int
    Username: str
    Password: str
    Topt_secret: str

    @staticmethod
    def validete_password(password):
        if len(password) < 8:
            raise ValueError("La password deve contenere almeno 8 caratteri!")
        if not re.search(r'[A-Z]', password):
            raise ValueError("La password deve contenere almeno una lettera maiuscola.")
        if not re.search(r'[a-z]', password):
            raise ValueError("La password deve contenere almeno una lettera minuscola.")
        if not re.search(r'[0-9]', password):
            raise ValueError("La password deve contenere almeno un numero.")
        if not re.search(r'\W', password):
            raise ValueError("La password deve contenere almeno un carattere speciale (!, @, #, etc.).")
        if "'" in password or " " in password:
            raise ValueError("La password non può contenere spazi o caratteri pericolosi.")
        
    @staticmethod
    def hash_password(password):
        salt = bcrypt.gensalt()  # Genera un salt casuale
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)  # Hash della password
        return hashed
