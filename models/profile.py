import mysql.connector
from config import DB_CONFIG

class Profile:
    @staticmethod
    def get_db_connection():
        return mysql.connector.connect(**DB_CONFIG)

    @staticmethod
    def is_profile_complete(user_id):
        db = Profile.get_db_connection()
        cursor = db.cursor()

        try:
            cursor.execute("SELECT * FROM profiles WHERE user_id = %s", (user_id,))
            profile = cursor.fetchone()
            return bool(profile)
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def get_profile(user_id):
        db = Profile.get_db_connection()
        cursor = db.cursor(dictionary=True)

        try:
            cursor.execute("SELECT * FROM profiles WHERE user_id = %s", (user_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def update_profile(user_id, data):
        db = Profile.get_db_connection()
        cursor = db.cursor()

        try:
            cursor.execute("""
                UPDATE profiles 
                SET age = %s, height = %s, weight = %s, goal = %s 
                WHERE user_id = %s
            """, (data["age"], data["height"], data["weight"], data["goal"], user_id))
            
            db.commit()
            return True
        except mysql.connector.Error as e:
            print(f"Error updating profile: {e}")
            return False
        finally:
            cursor.close()
            db.close()
