from repositories.base_repository import BaseRepository
from repositories.query_builder import QueryBuilder

class ProductRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.table = "Prodotto"
    
    def get_all_products(self):
        query, values = QueryBuilder().table(self.table).select("*").get_query()
        return self.fetch_all(query, values)
    
    def get_product_by_id(self, product_id):
        query, values = QueryBuilder().table(self.table).select("*").where("Id_prodotto", "=", product_id).get_query()
        return self.fetch_one(query, values)
    
    def get_products_by_name(self, name):
        query, values = QueryBuilder().table(self.table).select("*").where("Nome", "=", name).get_query()
        return self.fetch_all(query, values)
    
    def get_products_on_shelves(self):
        query = """
        SELECT
            Prodotto.Id_prodotto,
            Prodotto.Nome,
            Prodotto.Quantita,
            Prodotto.Stato,
            Azienda.Nome
        FROM Operazione
        JOIN Azienda ON Operazione.Id_azienda = Azienda.Id_azienda
        JOIN Prodotto ON Operazione.Id_prodotto = Prodotto.Id_prodotto
        WHERE Operazione.Operazione = "Messo sugli scaffali";
        """
        return self.fetch_all(query)
    
    def get_products_on_shelves_by_name(self, name):
        query = """
        SELECT
            Prodotto.Id_prodotto,
            Prodotto.Nome,
            Prodotto.Quantita,
            Prodotto.Stato,
            Azienda.Nome
        FROM Operazione
        JOIN Azienda ON Operazione.Id_azienda = Azienda.Id_azienda
        JOIN Prodotto ON Operazione.Id_prodotto = Prodotto.Id_prodotto
        WHERE Operazione.Operazione = "Messo sugli scaffali"
        AND Prodotto.Nome = ?;
        """
        return self.fetch_all(query, (name,))
    
    def get_products_on_shelves_by_retailer(self, retailer_id):
        query = """
        SELECT
            Prodotto.Id_prodotto,
            Prodotto.Nome,
            Prodotto.Quantita,
            Prodotto.Stato,
            Azienda.Nome
        FROM Operazione
        JOIN Azienda ON Operazione.Id_azienda = Azienda.Id_azienda
        JOIN Prodotto ON Operazione.Id_prodotto = Prodotto.Id_prodotto
        WHERE Operazione.Operazione = "Messo sugli scaffali"
        AND Operazione.Id_azienda = ?;
        """
        return self.fetch_all(query, (retailer_id,))
    
    def get_certified_products(self):
        query = """
        SELECT
            Prodotto.Id_prodotto,
            Prodotto.Nome,
            Prodotto.Quantita,
            Prodotto.Stato,
            Azienda.Nome
        FROM Operazione
        JOIN Azienda ON Operazione.Id_azienda = Azienda.Id_azienda
        JOIN Prodotto ON Operazione.Id_prodotto = Prodotto.Id_prodotto
        WHERE Operazione.Operazione = "Messo sugli scaffali"
        AND Operazione.Id_prodotto IN (
            SELECT Id_prodotto FROM Certificato
        );
        """
        return self.fetch_all(query)
    
    def get_product_history(self, product_id):
        query = """
        SELECT
            Operazione.Id_operazione,
            Azienda.Nome,
            Prodotto.Nome,
            Operazione.Data_operazione,
            Operazione.Consumo_CO2,
            Operazione.Operazione
        FROM Operazione
        JOIN Azienda ON Operazione.Id_azienda = Azienda.Id_azienda
        JOIN Prodotto ON Operazione.Id_prodotto = Prodotto.Id_prodotto
        WHERE Operazione.Id_prodotto IN (
            SELECT Materia_prima
            FROM Composizione
            WHERE Prodotto = ?
        );
        """
        return self.fetch_all(query, (product_id,))
    
    def insert_product(self, name, quantity, state=0):
        query, values = QueryBuilder().table(self.table).insert(
            Nome=name,
            Quantita=quantity,
            Stato=state
        ).get_query()
        self.execute_query(query, values)
        # Get the last inserted ID
        return self.fetch_one("SELECT last_insert_rowid()")[0]
    
    def update_product(self, product_id, **kwargs):
        qb = QueryBuilder().table(self.table).update()
        
        for key, value in kwargs.items():
            if value is not None:
                qb.update(**{key: value})
                
        query, values = qb.where("Id_prodotto", "=", product_id).get_query()
        self.execute_query(query, values)
    
    def delete_product(self, product_id):
        query, values = QueryBuilder().table(self.table).delete().where("Id_prodotto", "=", product_id).get_query()
        self.execute_query(query, values)