from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
import mysql.connector
from config import DB_CONFIG
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


auth = Blueprint("auth", __name__)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.login_view = "auth.login_page"

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# User Model
class User(UserMixin):
    def __init__(self, id, name, email,profile_completed=False):
        self.id = id
        self.name = name
        self.email = email
        self.profile_completed= profile_completed

@login_manager.user_loader
def load_user(user_id):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT id, name, email, profile_completed FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    db.close()
    
    if user:
        return User(id=user[0], name=user[1], email=user[2], profile_completed=bool(user[3])) 
    return None


@auth.route("/signup")
def signup_page():
    return render_template("signup.html")

@auth.route("/login")
def login_page():
    return render_template("login.html")

@auth.route("/signup", methods=["POST"])
def signup():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "All fields are required!"}), 400

    hashed_password = generate_password_hash(password)

    db = get_db_connection()
    cursor = db.cursor()

    try:
        cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({"error": "Email already registered!"}), 409

        cursor.execute("INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)", (name, email, hashed_password))
        db.commit()
        return jsonify({"message": "User registered successfully!", "redirect": "/auth/login"}), 200

    except mysql.connector.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()

@auth.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required!"}), 400

    db = get_db_connection()
    cursor = db.cursor()

    try:
        cursor.execute("SELECT id, name, email, password_hash, profile_completed FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user[3], password):
            user_obj = User(id=user[0], name=user[1], email=user[2], profile_completed=bool(user[4]))  # Include profile_completed
            login_user(user_obj)
            session["id"] = user[0]
            session["name"] = user[1]
            return jsonify({"message": "Login successful!", "redirect": url_for("landing_page")}), 200

        else:
            return jsonify({"error": "Invalid Credentials!"}), 401
    except mysql.connector.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("auth.login_page"))



@auth.route("/check_profile")
@login_required
def check_profile():
    return jsonify({"complete": bool(current_user.profile_completed)})

@auth.route("/complete_profile", methods=["POST"])
@login_required
def complete_profile():
    data = request.json
    email = current_user.email  

    db = get_db_connection()
    cursor = db.cursor()

    try:
        # Insert profile data
        cursor.execute("""
            INSERT INTO profile (email, age, gender, height, weight, fitness_goal, 
                                 target_weight, diet_preference, workout_time, workout_days)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
                age=VALUES(age), gender=VALUES(gender), height=VALUES(height),
                weight=VALUES(weight), fitness_goal=VALUES(fitness_goal),
                target_weight=VALUES(target_weight), diet_preference=VALUES(diet_preference),
                workout_time=VALUES(workout_time), workout_days=VALUES(workout_days)
        """, (email, data["age"], data["gender"], data["height"], data["weight"], 
              data["fitness_goal"], data["target_weight"], data["diet_preference"], 
              data["workout_time"], data["workout_days"]))

        # Mark profile as completed
        cursor.execute("UPDATE users SET profile_completed = TRUE WHERE email = %s", (email,))
        db.commit()

        return jsonify({"message": "Profile completed successfully!", "redirect": "/dashboard"}), 200

    except mysql.connector.Error as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()

@auth.route('/complete_profile',methods=["POST"])
@login.required
def complete_profile():
    data=request.get_json()
    
    try:
        current_user.age=data["age"]
        current_user.gender = data['gender']
        current_user.height = data['height']
        current_user.weight = data['weight']
        current_user.fitness_goal = data['fitness_goal']
        current_user.target_weight = data['target_weight']
        current_user.diet_preference = data['diet_preference']
        current_user.workout_time = data['workout_time']
        current_user.workout_days = data['workout_days']
        return jsonify({"redirect": "/dashboard"})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        



