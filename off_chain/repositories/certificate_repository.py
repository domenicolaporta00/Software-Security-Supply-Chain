from repositories.base_repository import BaseRepository
from repositories.query_builder import QueryBuilder

class CertificateRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.table = "Certificato"
    
    def get_all_certificates(self):
        query, values = QueryBuilder().table(self.table).select("*").get_query()
        return self.fetch_all(query, values)
    
    def get_certificate_by_id(self, certificate_id):
        query, values = QueryBuilder().table(self.table).select("*").where("Id_certificato", "=", certificate_id).get_query()
        return self.fetch_one(query, values)
    
    def get_certificate_by_product(self, product_id):
        query = """
        SELECT 
            Certificato.Id_certificato,
            Prodotto.Nome,
            Certificato.Descrizione,
            Azienda.Nome,
            Certificato.Data
        FROM Certificato
        JOIN Azienda ON Certificato.Id_azienda_certificatore = Azienda.Id_azienda
        JOIN Prodotto ON Certificato.Id_prodotto = Prodotto.Id_prodotto
        WHERE Certificato.Id_prodotto = ?;
        """
        return self.fetch_all(query, (product_id,))
    
    def is_product_certified(self, product_id):
        query = "SELECT * FROM Certificato WHERE Id_prodotto = ?;"
        result = self.fetch_all(query, (product_id,))
        return len(result) > 0
    
    def insert_certificate(self, product_id, description, certifier_company_id, date=None):
        qb = QueryBuilder().table(self.table).insert(
            Id_prodotto=product_id,
            Descrizione=description,
            Id_azienda_certificatore=certifier_company_id
        )
        
        if date:
            qb.insert(Data=date)
            
        query, values = qb.get_query()
        self.execute_query(query, values)
    
    def update_certificate(self, certificate_id, **kwargs):
        qb = QueryBuilder().table(self.table).update()
        
        for key, value in kwargs.items():
            if value is not None:
                qb.update(**{key: value})
                
        query, values = qb.where("Id_certificato", "=", certificate_id).get_query()
        self.execute_query(query, values)
    
    def delete_certificate(self, certificate_id):
        query, values = QueryBuilder().table(self.table).delete().where("Id_certificato", "=", certificate_id).get_query()
        self.execute_query(query, values)