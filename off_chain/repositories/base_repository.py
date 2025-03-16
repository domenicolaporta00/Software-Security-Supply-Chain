from config.database import Database

class BaseRepository:
    def __init__(self):
        self.db = Database().get_connection()
        self.cursor = None
    
    def execute_query(self, query, values=()):
        """Execute a query and commit changes"""
        self.cursor = self.db.cursor()
        self.cursor.execute(query, values)
        self.db.commit()
        self.cursor.close()
    
    def fetch_all(self, query, values=()):
        """Execute a query and fetch all results"""
        self.cursor = self.db.cursor()
        self.cursor.execute(query, values)
        results = self.cursor.fetchall()
        self.cursor.close()
        return results
    
    def fetch_one(self, query, values=()):
        """Execute a query and fetch one result"""
        self.cursor = self.db.cursor()
        self.cursor.execute(query, values)
        result = self.cursor.fetchone()
        self.cursor.close()
        return result
    
    def close(self):
        """Close the database connection"""
        if self.db:
            self.db.close()