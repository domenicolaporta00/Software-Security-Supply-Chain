from model.credential_model import CredentialModel
from repositories.auth_repository import AuthRepository
from repositories.company_repository import CompanyRepository
from config.database import Database
import bcrypt

class AuthService:
    def __init__(self):
        self.db = Database()
        self.auth_rep = AuthRepository()
        self.company_rep = CompanyRepository()

    def register(username, password, tipo, indirizzo, secret_key):

        CredentialModel.validete_password(password)

        hashed_password = CredentialModel.hash_password(password)

        #TODO
        #transaction inserimento nuove credenziali ed azienda


    def login(self,username, password):
        
        credentials = self.auth_rep.get_credential_by_username(username)

        if not credentials:
            raise ValueError("Credenziali errate!")

        hashed_password = credentials["password"].encode('utf-8')
        if not bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            raise ValueError("Credenziali errate!")

        return {"success": f"Login effettuato con successo per {username}"}


    