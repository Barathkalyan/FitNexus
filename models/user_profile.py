import mysql.connector
from flask import session
from config import DB_CONFIG

class Profile:
    @staticmethod
    def get_db_connection():
        return mysql.connector.connect(**DB_CONFIG)

    @staticmethod
    def is_profile_complete(email):
        db = Profile.get_db_connection()
        cursor = db.cursor()
        try:
            cursor.execute("SELECT * FROM profile WHERE email = %s", (email,))
            return bool(cursor.fetchone())
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def get_profile(email):
        db = Profile.get_db_connection()
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM profile WHERE email = %s", (email,))
            return cursor.fetchone()
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def update_profile(email, data):
        db = Profile.get_db_connection()
        cursor = db.cursor()
        try:
            cursor.execute("""
                UPDATE profile 
                SET age = %s, height = %s, weight = %s, fitness_goal = %s 
                WHERE email = %s
            """, (
                data["age"], data["height"], data["weight"], data["fitness_goal"], email
            ))
            db.commit()
            return True
        except mysql.connector.Error as e:
            print(f"Error updating profile: {e}")
            return False
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def save_full_profile(data):
        db = Profile.get_db_connection()
        cursor = db.cursor()
        try:
            email = session.get("email")
            if not email:
                raise Exception("Email not found in session.")

            cursor.execute("""
                INSERT INTO profile 
                (email, age, gender, height, weight, fitness_goal, target_weight, diet_preference, workout_time, workout_days)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    age=%s, gender=%s, height=%s, weight=%s,
                    fitness_goal=%s, target_weight=%s,
                    diet_preference=%s, workout_time=%s, workout_days=%s
            """, (
                email, data["age"], data["gender"], data["height"], data["weight"],
                data["fitness_goal"], data["target_weight"], data["diet_preference"],
                data["workout_time"], data["workout_days"],
                data["age"], data["gender"], data["height"], data["weight"],
                data["fitness_goal"], data["target_weight"],
                data["diet_preference"], data["workout_time"], data["workout_days"]
            ))
            db.commit()
            return True
        except mysql.connector.Error as e:
            print("Error saving full profile:", e)
            return False
        finally:
            cursor.close()
            db.close()
