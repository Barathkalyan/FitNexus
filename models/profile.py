from app import db, cursor

class Profile:
    @staticmethod
    def create_profile(user_id, dob, gender, height, weight, goal, workout_preference):
        query = """INSERT INTO profile (user_id, dob, gender, height, weight, goal, workout_preference) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        values = (user_id, dob, gender, height, weight, goal, workout_preference)
        cursor.execute(query, values)
        db.commit()

    @staticmethod
    def get_profile(user_id):
        query = "SELECT * FROM profile WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        return cursor.fetchone()

    @staticmethod
    def is_profile_complete(user_id):
        query = "SELECT COUNT(*) FROM profile WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        return cursor.fetchone()[0] > 0
