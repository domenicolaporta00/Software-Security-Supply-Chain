from repositories.base_repository import BaseRepository
from repositories.query_builder import QueryBuilder

class CompanyRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.table = "Azienda"
    
    def get_all_companies(self):
        query = """
        SELECT Id_azienda, Tipo, Indirizzo, Nome FROM Azienda WHERE Tipo != "Certificatore"
        """
        companies = self.fetch_all(query)
        result = []
        
        for company in companies:
            co2_consumed = self._get_co2_consumed(company[0]) or 0
            co2_compensated = self._get_co2_compensated(company[0]) or 0
            result.append((company, co2_consumed, co2_compensated))
            
        return result
    
    def get_companies_ordered_by_co2_balance(self):
        companies = self.get_all_companies()
        return sorted(companies, key=lambda x: (x[2] or 0) - (x[1] or 0), reverse=True)
    
    def get_companies_by_type(self, company_type):
        query = """
        SELECT Id_azienda, Tipo, Indirizzo, Nome FROM Azienda WHERE Tipo != "Certificatore"
        AND Tipo = ?
        """
        companies = self.fetch_all(query, (company_type,))
        result = []
        
        for company in companies:
            co2_consumed = self._get_co2_consumed(company[0]) or 0
            co2_compensated = self._get_co2_compensated(company[0]) or 0
            result.append((company, co2_consumed, co2_compensated))
            
        return result
    
    def get_company_by_name(self, name):
        query = """
        SELECT Id_azienda, Tipo, Indirizzo, Nome FROM Azienda WHERE Tipo != "Certificatore"
        AND Nome = ?
        """
        companies = self.fetch_all(query, (name,))
        result = []
        
        for company in companies:
            co2_consumed = self._get_co2_consumed(company[0]) or 0
            co2_compensated = self._get_co2_compensated(company[0]) or 0
            result.append((company, co2_consumed, co2_compensated))
            
        return result
    
    def get_company_by_id(self, company_id):
        query = """
        SELECT Id_azienda, Tipo, Indirizzo, Nome, Email FROM Azienda WHERE Id_azienda = ?;
        """
        companies = self.fetch_all(query, (company_id,))
        result = []
        
        for company in companies:
            co2_consumed = self._get_co2_consumed(company[0]) or 0
            co2_compensated = self._get_co2_compensated(company[0]) or 0
            result.append((company, co2_consumed, co2_compensated))
            
        return result
    
    def get_retailers(self):
        query = """
        SELECT Id_azienda, Tipo, Indirizzo, Nome FROM Azienda WHERE Tipo = "Rivenditore"
        """
        return self.fetch_all(query)
    
    def update_company(self, company_id, email=None, address=None):
        qb = QueryBuilder().table(self.table).update()
        
        if email:
            qb.update(Email=email)
        if address:
            qb.update(Indirizzo=address)
            
        query, values = qb.where("Id_azienda", "=", company_id).get_query()
        self.execute_query(query, values)
    
    def get_company_profile(self, company_id):
        query, values = QueryBuilder().table(self.table).select("*").where("Id_azienda", "=", company_id).get_query()
        return self.fetch_one(query, values)
    
    def get_certification_count(self, company_id):
        query = """
        SELECT COUNT(*) FROM Certificato WHERE Id_azienda_certificatore = ?;
        """
        return self.fetch_one(query, (company_id,))[0]
    
    def _get_co2_consumed(self, company_id):
        query = """
        SELECT SUM(Consumo_CO2) FROM Operazione WHERE Id_azienda = ?;
        """
        result = self.fetch_one(query, (company_id,))
        return result[0] if result and result[0] else 0
    
    def _get_co2_compensated(self, company_id):
        query = """
        SELECT SUM(Co2_compensata) FROM Azioni_compensative WHERE Id_azienda = ?;
        """
        result = self.fetch_one(query, (company_id,))
        return result[0] if result and result[0] else 0