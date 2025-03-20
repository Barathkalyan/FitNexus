from app import db, cursor

class User:
    @staticmethod
    def create_user(username, email, password_hash):
        query = "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)"
        values = (username, email, password_hash)
        cursor.execute(query, values)
        db.commit()

    @staticmethod
    def get_user_by_email(email):
        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        return cursor.fetchone()
