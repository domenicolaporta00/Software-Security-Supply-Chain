class QueryBuilder:
    def __init__(self):
        self._table = None
        self._columns = "*"
        self._where = []
        self._values = []
        self._set = []

    def table(self, table_name):
        self._table = table_name
        return self

    def select(self, *columns):
        self._columns = ", ".join(columns) if columns else "*"
        return self

    def where(self, column, operator, value):
        self._where.append(f"{column} {operator} %s")
        self._values.append(value)
        return self

    def insert(self, **values):
        columns = ", ".join(values.keys())
        placeholders = ", ".join(["%s"] * len(values))
        self._query = f"INSERT INTO {self._table} ({columns}) VALUES ({placeholders})"
        self._values = list(values.values())
        return self

    def update(self, **values):
        self._set = [f"{col} = %s" for col in values.keys()]
        self._values = list(values.values())
        return self

    def delete(self):
        self._query = f"DELETE FROM {self._table}"
        return self

    def get_query(self):
        if self._set:
            query = f"UPDATE {self._table} SET {', '.join(self._set)}"
        elif self._where:
            query = f"SELECT {self._columns} FROM {self._table} WHERE {' AND '.join(self._where)}"
        else:
            query = f"SELECT {self._columns} FROM {self._table}"
        return query, self._values
