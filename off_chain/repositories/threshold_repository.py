from repositories.base_repository import BaseRepository
from repositories.query_builder import QueryBuilder

class ThresholdRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.table = "Soglie"
    
    def get_all_thresholds(self):
        query, values = QueryBuilder().table(self.table).select("*").get_query()
        return self.fetch_all(query, values)
    
    def get_threshold_by_operation_and_product(self, operation, product):
        query = """
        SELECT Soglia_Massima FROM Soglie WHERE Operazione = ? AND Prodotto = ?;
        """
        result = self.fetch_one(query, (operation, product))
        return result[0] if result else 999  # Default high value if not found
    
    def get_products_by_type(self, product_type):
        query = """
        SELECT DISTINCT Prodotto FROM Soglie WHERE Tipo = ?;
        """
        results = self.fetch_all(query, (product_type,))
        return [result[0] for result in results]
    
    def insert_threshold(self, operation, product, max_threshold, product_type):
        query, values = QueryBuilder().table(self.table).insert(
            Operazione=operation,
            Prodotto=product,
            Soglia_Massima=max_threshold,
            Tipo=product_type
        ).get_query()
        self.execute_query(query, values)
    
    def update_threshold(self, operation, product, max_threshold=None, product_type=None):
        qb = QueryBuilder().table(self.table).update()
        
        if max_threshold is not None:
            qb.update(Soglia_Massima=max_threshold)
        if product_type is not None:
            qb.update(Tipo=product_type)
            
        query, values = qb.where("Operazione", "=", operation).where("Prodotto", "=", product).get_query()
        self.execute_query(query, values)
    
    def delete_threshold(self, operation, product):
        query, values = QueryBuilder().table(self.table).delete().where("Operazione", "=", operation).where("Prodotto", "=", product).get_query()
        self.execute_query(query, values)