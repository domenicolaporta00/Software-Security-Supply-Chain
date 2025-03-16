from config.database import Database
from repositories.query_builder import QueryBuilder

class UserService:
    def __init__(self):
        self.db = Database().get_connection()

    def get_all_users(self):
        query, values = QueryBuilder().table("users").select("id", "name", "email").get_query()
        cursor = self.db.cursor()
        cursor.execute(query, values)
        users = cursor.fetchall()
        cursor.close()
        return [{"id": u[0], "name": u[1], "email": u[2]} for u in users]

    def get_user_by_id(self, user_id):
        query, values = QueryBuilder().table("users").select("id", "name", "email").where("id", "=", user_id).get_query()
        cursor = self.db.cursor()
        cursor.execute(query, values)
        user = cursor.fetchone()
        cursor.close()
        return {"id": user[0], "name": user[1], "email": user[2]} if user else None

    def create_user(self, name, email):
        query, values = QueryBuilder().table("users").insert(name=name, email=email).get_query()
        cursor = self.db.cursor()
        cursor.execute(query, values)
        self.db.commit()
        cursor.close()

    def update_user(self, user_id, name=None, email=None):
        qb = QueryBuilder().table("users").update()
        if name:
            qb.update(name=name)
        if email:
            qb.update(email=email)
        query, values = qb.where("id", "=", user_id).get_query()

        cursor = self.db.cursor()
        cursor.execute(query, values)
        self.db.commit()
        cursor.close()

    def delete_user(self, user_id):
        query, values = QueryBuilder().table("users").delete().where("id", "=", user_id).get_query()
        cursor = self.db.cursor()
        cursor.execute(query, values)
        self.db.commit()
        cursor.close()