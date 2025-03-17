from repositories.query_builder import QueryBuilder
 
class CompensatoryActionRepository():
     def __init__(self):
         super().__init__()
         self.table = "Azioni_compensative"
     
     def get_actions_by_company(self, company_id):
         query = """
         SELECT * FROM Azioni_compensative WHERE Id_azienda = ?;
         """
         return self.fetch_all(query, (company_id,))
     
     def get_actions_by_date_range(self, company_id, start_date, end_date):
         query = """
         SELECT * FROM Azioni_compensative
         WHERE Id_azienda = ? AND Data BETWEEN ? AND ?;
         """
         return self.fetch_all(query, (company_id, start_date, end_date))
     
     def get_actions_ordered_by_co2(self, company_id):
         query = """
         SELECT * FROM Azioni_compensative
         WHERE Id_azienda = ?
         ORDER BY Co2_compensata DESC;
         """
         return self.fetch_all(query, (company_id,))
     
     def get_total_co2_compensated(self, company_id):
         query = """
         SELECT SUM(Co2_compensata) FROM Azioni_compensative WHERE Id_azienda = ?;
         """
         result = self.fetch_one(query, (company_id,))
         return result[0] if result and result[0] else 0
     
     def insert_action(self, date, company_id, co2_compensated, action_name):
         query, values = QueryBuilder().table(self.table).insert(
             Data=date,
             Id_azienda=company_id,
             Co2_compensata=co2_compensated,
             Nome_azione=action_name
         ).get_query()
         self.execute_query(query, values)
     
     def get_action_by_id(self, action_id):
         query, values = QueryBuilder().table(self.table).select("*").where("Id_azione", "=", action_id).get_query()
         return self.fetch_one(query, values)
     
     def update_action(self, action_id, **kwargs):
         qb = QueryBuilder().table(self.table).update()
         
         for key, value in kwargs.items():
             if value is not None:
                 qb.update(**{key: value})
                 
         query, values = qb.where("Id_azione", "=", action_id).get_query()
         self.execute_query(query, values)
     
     def delete_action(self, action_id):
         query, values = QueryBuilder().table(self.table).delete().where("Id_azione", "=", action_id).get_query()
         self.execute_query(query, values)