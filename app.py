from flask import Flask, render_template, session, redirect, url_for, request
from flask import request, jsonify, session
import mysql.connector
from config import DB_CONFIG
from flask_cors import CORS
from flask_login import LoginManager, current_user
from models.user import User
from profile import Profile

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "b94f8e17d2a645f3a3c91e4825a1d6b7"
CORS(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login_page"

# User loader function
@login_manager.user_loader
def load_user(user_id):
    db = mysql.connector.connect(**DB_CONFIG)
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT id, name, email, profile_completed FROM users WHERE id = %s", (user_id,))
    user_data = cursor.fetchone()

    cursor.close()
    db.close()

    if user_data:
        user = User(user_data["id"], user_data["name"], user_data["email"], user_data["profile_completed"])
        session["profile_completed"] = bool(user_data["profile_completed"])  # Store as boolean
        return user
    return None

# Import blueprints
from routes.auth import auth
app.register_blueprint(auth, url_prefix="/auth")

@app.route('/')
def home():
    """Redirect to login if not logged in, otherwise go to landing or dashboard."""
    if "id" not in session:
        return redirect(url_for("auth.login_page"))  # Ensure login page appears first

    if session.get("profile_completed"):
        return redirect(url_for("dashboard"))  # Go to dashboard if profile is complete
    return redirect(url_for("profile_complete"))  # Else, go to profile completion

@app.route('/landing')
def landing_page():
    return render_template("index.html")  # Separate route for the landing page

@app.route('/get-started')
def get_started():
    if "id" not in session:
        return redirect(url_for("auth.login_page"))  # Redirect to login if not logged in

    if session.get("profile_completed"):
        return redirect(url_for("dashboard"))  # Redirect to dashboard if profile is complete
    return redirect(url_for("profile_complete"))  # Else, go to profile completion page

@app.route("/dashboard")
def dashboard():
    if "id" not in session:
        return redirect(url_for("auth.login_page"))
    
    if not session.get("profile_completed"):
        return redirect(url_for("profile_complete"))

    return render_template("dashboard.html")

@app.route("/profile-complete", methods=["GET", "POST"])
def profile_complete():
    if "id" not in session:
        return redirect(url_for("auth.login_page"))

    if request.method == "POST":
        # Update profile completion in DB
        db = mysql.connector.connect(**DB_CONFIG)
        cursor = db.cursor()
        cursor.execute("UPDATE users SET profile_completed = 1 WHERE id = %s", (session["id"],))
        db.commit()
        cursor.close()
        db.close()

        # Update session
        session["profile_completed"] = True
        return redirect(url_for("dashboard"))

    return render_template("profile_complete.html")

@app.route("/api/complete-profile", methods=["POST"])
def complete_profile():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    user_id= session["user_id"]
    data=request.get_json()
    
    success= Profile.save_full_profile(user_id,data)
    
    if success:
        return jsonify({"redirect": "/dashboard"})
    else:
        return jsonify({"error": "Failed to save Profile"}), 500

if __name__ == "__main__":
    app.run(debug=True)
