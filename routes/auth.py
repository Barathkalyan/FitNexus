from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
import mysql.connector
from config import DB_CONFIG
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user, UserMixin
import random

auth = Blueprint("auth", __name__)

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# Generate unique user ID like FN123
def generate_user_id():
    return f"FN{random.randint(100, 999)}"

def is_user_id_unique(user_id):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id,))
    exists = cursor.fetchone()
    cursor.close()
    db.close()
    return exists is None

# User model
class User(UserMixin):
    def __init__(self, id, user_id, name, email, profile_completed=False):
        self.id = id
        self.user_id = user_id
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

        # Generate unique user_id
        user_id = generate_user_id()
        while not is_user_id_unique(user_id):
            user_id = generate_user_id()

        cursor.execute("""
            INSERT INTO users (name, email, password_hash, user_id)
            VALUES (%s, %s, %s, %s)
        """, (name, email, hashed_password, user_id))
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
        cursor.execute("""
            SELECT id, name, email, password_hash, profile_completed, user_id 
            FROM users WHERE email = %s
        """, (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user[3], password):
            user_obj = User(id=user[0], user_id=user[5], name=user[1], email=user[2], profile_completed=bool(user[4]))
            login_user(user_obj)
            session["id"] = user[0]
            session["name"] = user[1]
            session["email"] = user[2]
            session["user_id"] = user[5]
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
        "user_id": current_user.user_id,
        "name": current_user.name,
        "email": current_user.email
    })
