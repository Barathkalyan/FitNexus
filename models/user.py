import mysql.connector
from config import DB_CONFIG

class User:
    def __init__(self, id, user_id, name, email, profile_completed=False):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.email = email
        self.profile_completed = profile_completed

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    @staticmethod
    def get_user_by_email(email):
        db = mysql.connector.connect(**DB_CONFIG)
        cursor = db.cursor()
        try:
            query = "SELECT id, user_id, name, email, profile_completed FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            row = cursor.fetchone()
            if row:
                return User(row[0], row[1], row[2], row[3], row[4])
            return None
        finally:
            cursor.close()
            db.close()
