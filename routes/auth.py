from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from config import DB_CONFIG

auth = Blueprint("auth", __name__)

# Create a database connection
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

@auth.route("/signup", methods=["POST"])
def signup():
    data = request.json
    name= data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "Name, Email and password are required!"}), 400

    hashed_password = generate_password_hash(password)

    db = get_db_connection()
    cursor = db.cursor()

    try:
        # Check if email already exists
        cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({"error": "Email already registered!"}), 409

        # Insert new user
        cursor.execute("INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)", (name, email, hashed_password))
        db.commit()
        return jsonify({"message": "User registered successfully!"})
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
        cursor.execute("SELECT name, password_hash FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user[1], password):
            return jsonify({"message": f"Welcome to FitNexus {user[0]}! Login Successful!"})
        else:
            return jsonify({"error": "Invalid Credentials!"}), 401
    except mysql.connector.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()
