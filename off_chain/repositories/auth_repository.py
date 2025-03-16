import hashlib
import re
from repositories.base_repository import BaseRepository
from repositories.query_builder import QueryBuilder

class AuthRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.table = "Credenziali"
    
    def get_all_credentials(self):
        query, values = QueryBuilder().table(self.table).select("*").get_query()
        return self.fetch_all(query, values)
    
    def get_credential_by_username(self, username):
        query = """
        SELECT * FROM Credenziali WHERE Username = ?
        """
        result = self.fetch_all(query, (username,))
        return result[0] if result else None
    
    @staticmethod
    def hash_password(password):
        """Esegue l'hashing della password usando SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def update_password(self, credential_id, new_password):
        # Controllo sulla nuova password
        if len(new_password) < 8:
            raise ValueError("La password deve contenere almeno 8 caratteri!")
        if not re.search(r'[A-Z]', new_password):
            raise ValueError("La password deve contenere almeno una lettera maiuscola.")
        if not re.search(r'[a-z]', new_password):
            raise ValueError("La password deve contenere almeno una lettera minuscola.")
        if not re.search(r'[0-9]', new_password):
            raise ValueError("La password deve contenere almeno un numero.")
        if not re.search(r'\W', new_password):
            raise ValueError("La password deve contenere almeno un carattere speciale (!, @, #, etc.).")
        if "'" in new_password or " " in new_password:
            raise ValueError("La password non può contenere spazi o caratteri pericolosi.")

        # Hash della nuova password
        hashed_new_password = self.hash_password(new_password)

        # Aggiorna la password nel database
        query, values = QueryBuilder().table(self.table).update(Password=hashed_new_password).where("Id_credenziali", "=", credential_id).get_query()
        self.execute_query(query, values)
        return True
    
    def verify_password(self, credential_id, password):
        query = """
        SELECT Password FROM Credenziali WHERE Id_credenziali = ?
        """
        result = self.fetch_one(query, (credential_id,))
        if not result:
            return False
        
        hashed_password = self.hash_password(password)
        return result[0] == hashed_password