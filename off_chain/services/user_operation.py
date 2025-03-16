from config.database import Database
from repositories.query_builder import QueryBuilder

class UserService:
    def __init__(self):
        self.db = Database()

    