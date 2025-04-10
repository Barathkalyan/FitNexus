from flask import Flask, render_template, session, redirect, url_for, request, jsonify
import mysql.connector
from config import DB_CONFIG
from flask_cors import CORS
from flask_login import LoginManager, login_required, current_user
from models.user import User
from models.user_profile import Profile

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "b94f8e17d2a645f3a3c91e4825a1d6b7"
CORS(app, supports_credentials=True)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login_page"

@login_manager.user_loader
def load_user(user_id):
    db = mysql.connector.connect(**DB_CONFIG)
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, name, email, profile_completed FROM users WHERE id = %s", (user_id,))
    user_data = cursor.fetchone()
    cursor.close()
    db.close()

    if user_data:
        session["email"]= user_data["email"]
        return User(user_data["id"], user_data["name"], user_data["email"], user_data["profile_completed"])
    return None

from routes.auth import auth
app.register_blueprint(auth, url_prefix="/auth")

@app.route("/")
def home():
    if "id" not in session:
        return redirect(url_for("auth.login_page"))
    return redirect(url_for("landing_page") if session.get("profile_completed") else url_for("profile_complete"))

@app.route("/landing")
def landing_page():
    return render_template("index.html")

@app.route("/get-started")
def get_started():
    if "id" not in session:
        return redirect(url_for("auth.login_page"))
    return redirect(url_for("dashboard") if session.get("profile_completed") else url_for("profile_complete"))

@app.route("/dashboard")
@login_required
def dashboard():
    if not session.get("profile_completed"):
        return redirect(url_for("profile_complete"))
    return render_template("dashboard.html")

@app.route("/profile-complete", methods=["GET", "POST"])
@login_required
def profile_complete():
    if request.method == "POST":
        db = mysql.connector.connect(**DB_CONFIG)
        cursor = db.cursor()
        cursor.execute("UPDATE users SET profile_completed = 1 WHERE id = %s", (session["id"],))
        db.commit()
        cursor.close()
        db.close()
        session["profile_completed"] = True
        return redirect(url_for("dashboard"))
    return render_template("profile_complete.html")

@app.route("/api/complete-profile", methods=["POST"])
@login_required
def complete_profile_api():
    data = request.json
    user_id = session.get("id")
    if not user_id:
        return jsonify({"error": "Session expired. Please log in again."}), 401

    data["user_id"] = user_id  # Make sure the profile gets linked to the user

    if Profile.save_full_profile(data):
        session["profile_completed"] = True
        return jsonify({"message": "Profile saved successfully", "redirect": "/dashboard"}), 200
    else:
        return jsonify({"error": "Failed to save profile"}), 500

if __name__ == "__main__":
    app.run(debug=True)
