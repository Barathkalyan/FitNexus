import mysql.connector
from config import DB_CONFIG

db = mysql.connector.connect(**DB_CONFIG)
cursor = db.cursor()

class User:
    def __init__(self, id, name, email, profile_completed=False):
        self.id = id
        self.name = name
        self.email = email
        self.profile_completed = profile_completed  # ✅ Added this

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
        query = "SELECT id, name, email, profile_completed FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        row = cursor.fetchone()
        if row:
            return User(row[0], row[1], row[2], row[3])  # ✅ Included profile_completed
        return None
