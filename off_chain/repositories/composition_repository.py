from repositories.base_repository import BaseRepository
from repositories.query_builder import QueryBuilder

class CompositionRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.table = "Composizione"
    
    def get_composition_by_product(self, product_id):
        query = """
        SELECT Materia_prima FROM Composizione WHERE Prodotto = ?;
        """
        results = self.fetch_all(query, (product_id,))
        return [result[0] for result in results] if results else []
    
    def add_raw_material_to_product(self, product_id, raw_material_id):
        query, values = QueryBuilder().table(self.table).insert(
            Prodotto=product_id,
            Materia_prima=raw_material_id
        ).get_query()
        self.execute_query(query, values)
    
    def remove_raw_material_from_product(self, product_id, raw_material_id):
        query, values = QueryBuilder().table(self.table).delete()\
            .where("Prodotto", "=", product_id)\
            .where("Materia_prima", "=", raw_material_id).get_query()
        self.execute_query(query, values)
    
    def get_raw_materials_for_transformation(self, company_id):
        query = """
        SELECT Prodotto.Id_prodotto, Prodotto.Nome, Prodotto.Quantita
        FROM Prodotto
        JOIN Operazione
        ON Prodotto.Id_prodotto = Operazione.Id_prodotto
        WHERE Operazione.Operazione = "Trasformazione"
        AND Operazione.Id_azienda = ?
        ORDER BY Operazione.Data_operazione DESC;
        """
        return self.fetch_all(query, (company_id,))