from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
import mysql.connector
from config import DB_CONFIG
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user, UserMixin

auth = Blueprint("auth", __name__)

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# User model
class User(UserMixin):
    def __init__(self, id, name, email, profile_completed=False):
        self.id = id
        self.name = name
        self.email = email
        self.profile_completed = profile_completed

    def get_id(self):
        return str(self.id)

# Routes
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

        cursor.execute("INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)",
                       (name, email, hashed_password))
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
            user_obj = User(id=user[0], name=user[1], email=user[2], profile_completed=bool(user[4]))
            login_user(user_obj)
            session["id"] = user[0]
            session["name"] = user[1]
            session["email"] = user[2]  # ✅ REQUIRED for profile save
            session["profile_completed"] = bool(user[4])
            return jsonify({"message": "Login successful!", "redirect": "/"}), 200
        else:
            return jsonify({"error": "Invalid credentials!"}), 401
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
    return jsonify({
        "complete": current_user.profile_completed,
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email
    })
