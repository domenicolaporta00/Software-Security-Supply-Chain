from repositories.base_repository import BaseRepository
from repositories.query_builder import QueryBuilder

class OperationRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.table = "Operazione"
    
    def get_operations_by_company(self, company_id):
        query = """
        SELECT Operazione.Id_operazione, Prodotto.Id_prodotto, Prodotto.Nome, Prodotto.Quantita, 
        Operazione.Data_operazione, Operazione.Consumo_CO2, Operazione.Operazione
        FROM Operazione JOIN Prodotto
        ON Operazione.Id_prodotto = Prodotto.Id_prodotto
        WHERE Operazione.Id_azienda = ?;
        """
        return self.fetch_all(query, (company_id,))
    
    def get_operations_by_date_range(self, company_id, start_date, end_date):
        query = """
        SELECT Operazione.Id_operazione, Prodotto.Id_prodotto, Prodotto.Nome, Prodotto.Quantita, 
        Operazione.Data_operazione, Operazione.Consumo_CO2, Operazione.Operazione
        FROM Operazione JOIN Prodotto
        ON Operazione.Id_prodotto = Prodotto.Id_prodotto
        WHERE Operazione.Id_azienda = ?
        AND Operazione.Data_operazione BETWEEN ? AND ?;
        """
        return self.fetch_all(query, (company_id, start_date, end_date))
    
    def get_operations_ordered_by_co2(self, company_id):
        query = """
        SELECT Operazione.Id_operazione, Prodotto.Id_prodotto, Prodotto.Nome, Prodotto.Quantita, 
        Operazione.Data_operazione, Operazione.Consumo_CO2, Operazione.Operazione
        FROM Operazione JOIN Prodotto
        ON Operazione.Id_prodotto = Prodotto.Id_prodotto
        WHERE Operazione.Id_azienda = ?
        ORDER BY Operazione.Consumo_CO2 ASC;
        """
        return self.fetch_all(query, (company_id,))
    
    def insert_operation(self, company_id, product_id, date, co2_consumption, operation_type, recipient=None):
        qb = QueryBuilder().table(self.table).insert(
            Id_azienda=company_id,
            Id_prodotto=product_id,
            Data_operazione=date,
            Consumo_CO2=co2_consumption,
            Operazione=operation_type
        )
        
        if recipient:
            qb.insert(Destinatario=recipient)
            
        query, values = qb.get_query()
        self.execute_query(query, values)
        
    def get_operation_by_id(self, operation_id):
        query, values = QueryBuilder().table(self.table).select("*").where("Id_operazione", "=", operation_id).get_query()
        return self.fetch_one(query, values)
    
    def update_operation(self, operation_id, **kwargs):
        qb = QueryBuilder().table(self.table).update()
        
        for key, value in kwargs.items():
            if value is not None:
                qb.update(**{key: value})
                
        query, values = qb.where("Id_operazione", "=", operation_id).get_query()
        self.execute_query(query, values)
        
    def delete_operation(self, operation_id):
        query, values = QueryBuilder().table(self.table).delete().where("Id_operazione", "=", operation_id).get_query()
        self.execute_query(query, values)