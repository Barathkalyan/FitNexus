from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY  # Add these to config.py
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user, UserMixin
import random

auth = Blueprint("auth", __name__)

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Generate unique user ID like FN123::
def generate_user_id():
    return f"FN{random.randint(100, 999)}"

def is_user_id_unique(user_id):
    response = supabase.table('users').select('user_id').eq('user_id', user_id).execute()
    return len(response.data) == 0

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

    try:
        # Check if email already exists
        response = supabase.table('users').select('email').eq('email', email).execute()
        if response.data:
            return jsonify({"error": "Email already registered!"}), 409

        # Generate unique user_id
        user_id = generate_user_id()
        while not is_user_id_unique(user_id):
            user_id = generate_user_id()

        # Insert new user
        response = supabase.table('users').insert({
            "name": name,
            "email": email,
            "password_hash": hashed_password,
            "user_id": user_id,
            "profile_completed": False
        }).execute()

        if response.error:
            return jsonify({"error": str(response.error)}), 500

        return jsonify({"message": "User registered successfully!", "redirect": "/auth/login"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required!"}), 400

    try:
        # Fetch user from Supabase
        response = supabase.table('users').select('id, name, email, password_hash, profile_completed, user_id').eq('email', email).execute()
        if not response.data or len(response.data) == 0:
            return jsonify({"error": "Invalid credentials!"}), 401

        user_data = response.data[0]
        if check_password_hash(user_data['password_hash'], password):
            user_obj = User(id=user_data['id'], user_id=user_data['user_id'], name=user_data['name'], email=user_data['email'], profile_completed=bool(user_data['profile_completed']))
            login_user(user_obj)
            session["id"] = user_data['id']
            session["name"] = user_data['name']
            session["email"] = user_data['email']
            session["user_id"] = user_data['user_id']
            session["profile_completed"] = bool(user_data['profile_completed'])
            return jsonify({"message": "Login successful!", "redirect": "/"}), 200
        else:
            return jsonify({"error": "Invalid credentials!"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
