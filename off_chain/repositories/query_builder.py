class QueryBuilder:
     def __init__(self):
         self.query_table = None
         self.query_type = None
         self.query_select = []
         self.query_where = []
         self.query_values = []
         self.query_insert = {}
         self.query_update = {}
 
     def table(self, table_name):
         self.query_table = table_name
         return self
 
     def select(self, *fields):
         self.query_type = 'select'
         if fields:
             self.query_select = list(fields)
         return self
 
     def where(self, field, operator, value):
         self.query_where.append((field, operator, value))
         self.query_values.append(value)
         return self
 
     def insert(self, **kwargs):
         self.query_type = 'insert'
         self.query_insert = kwargs
         return self
 
     def update(self, **kwargs):
         if self.query_type != 'update':
             self.query_type = 'update'
             self.query_update = {}
         
         self.query_update.update(kwargs)
         return self
 
     def delete(self):
         self.query_type = 'delete'
         return self
 
     def get_query(self):
         if self.query_type == 'select':
             return self._build_select_query()
         elif self.query_type == 'insert':
             return self._build_insert_query()
         elif self.query_type == 'update':
             return self._build_update_query()
         elif self.query_type == 'delete':
             return self._build_delete_query()
         else:
             raise ValueError("Query type not specified")
 
     def _build_select_query(self):
         fields = ", ".join(self.query_select) if self.query_select else "*"
         query = f"SELECT {fields} FROM {self.query_table}"
         
         if self.query_where:
             where_clauses = [f"{field} {operator} ?" for field, operator, _ in self.query_where]
             query += " WHERE " + " AND ".join(where_clauses)
         
         return query, self.query_values
 
     def _build_insert_query(self):
         fields = ", ".join(self.query_insert.keys())
         placeholders = ", ".join(["?" for _ in self.query_insert])
         values = list(self.query_insert.values())
         
         query = f"INSERT INTO {self.query_table} ({fields}) VALUES ({placeholders})"
         
         return query, values
 
     def _build_update_query(self):
         set_clauses = [f"{field} = ?" for field in self.query_update.keys()]
         values = list(self.query_update.values())
         
         query = f"UPDATE {self.query_table} SET {', '.join(set_clauses)}"
         
         if self.query_where:
             where_clauses = [f"{field} {operator} ?" for field, operator, _ in self.query_where]
             query += " WHERE " + " AND ".join(where_clauses)
             values.extend(self.query_values)
         
         return query, values
 
     def _build_delete_query(self):
         query = f"DELETE FROM {self.query_table}"
         
         if self.query_where:
             where_clauses = [f"{field} {operator} ?" for field, operator, _ in self.query_where]
             query += " WHERE " + " AND ".join(where_clauses)
         
         return query, self.query_values