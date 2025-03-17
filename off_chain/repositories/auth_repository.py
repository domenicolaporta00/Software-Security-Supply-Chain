import hashlib
import re
from repositories.query_builder import QueryBuilder
from model.credential_model import CredentialModel
from config.database import Database
 
class AuthRepository():
     def __init__(self):
         super().__init__()
         self.table = "Credenziali"
         self.db = Database()
     
     def get_all_credentials(self):
         query, values = QueryBuilder().table(self.table).select("*").get_query()
         return self.fetch_all(query, values)
     
     def get_credential_by_username(self, username):
         
         
         #TODO query builder
         query = QueryBuilder().table(self.table).select("*").where("Username", "=", username).get_query()
         query = """
         SELECT * FROM Credenziali WHERE Username = ?
         """
         return self.db.fetch_query(query,(username,), fetchone = True)
     
     @staticmethod
     def hash_password(password):
         """Esegue l'hashing della password usando SHA-256"""
         return hashlib.sha256(password.encode()).hexdigest()
     
     def update_password(self, credential_id, new_password):
         
         CredentialModel.validete_password(new_password)       
         
 
         # Hash della nuova password
         hashed_new_password = CredentialModel.hash_password(new_password)
 
         # Aggiorna la password nel database
         query, values = QueryBuilder().table(self.table).update(Password=hashed_new_password).where("Id_credenziali", "=", credential_id).get_query()

         self.execute_query(query, values)
         
         return True
     
     def verify_password(self, credential_id, password):
         
         #usare query builder
         query = """
         SELECT Password FROM Credenziali WHERE Id_credenziali = ?
         """
         result = self.fetch_one(query, (credential_id,))
         if not result:
             return False
         
         hashed_password = self.hash_password(password)
         return result[0] == hashed_password