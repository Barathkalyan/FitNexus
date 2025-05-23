from flask import Flask, render_template, session, redirect, url_for, request, jsonify
import mysql.connector
from config import DB_CONFIG
from flask_cors import CORS
from flask_login import LoginManager, login_required, current_user
from models.user import User
from models.user_profile import Profile

# Initialize Flask app
app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "b94f8e17d2a645f3a3c91e4825a1d6b7"
CORS(app, supports_credentials=True)

# Set up Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login_page"

# Load user from session
@login_manager.user_loader
def load_user(user_id):
    db = mysql.connector.connect(**DB_CONFIG)
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, name, email, profile_completed FROM users WHERE id = %s", (user_id,))
    user_data = cursor.fetchone()
    cursor.close()
    db.close()

    if user_data:
        session["email"] = user_data["email"]
        return User(
            user_data["id"],
            user_data["name"],
            user_data["email"],
            user_data["profile_completed"]
        )
    return None

# Register authentication routes
from routes.auth import auth
app.register_blueprint(auth, url_prefix="/auth")

# Home route - redirect based on login and profile status
@app.route("/")
def home():
    if "id" not in session:
        return redirect(url_for("auth.login_page"))
    if session.get("profile_completed"):
        return redirect(url_for("dashboard"))
    return redirect(url_for("profile_complete"))

# Smart redirect based on profile completion
@app.route("/get-started")
def get_started():
    if "id" not in session:
        return redirect(url_for("auth.login_page"))
    if session.get("profile_completed"):
        return redirect(url_for("dashboard"))
    return redirect(url_for("profile_complete"))

# Dashboard - only accessible when profile is completed
@app.route("/dashboard")
@login_required
def dashboard():
    if not session.get("profile_completed"):
        return redirect(url_for("profile_complete"))
    
    db = mysql.connector.connect(**DB_CONFIG)
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("SELECT weight,target_weight,fitness_goal,diet_preference from profile where user_id=%s", (session["user_id"],))
    profile=cursor.fetchone()
    
    cursor.close()
    db.close()
    
    if profile:
        return render_template("dashboard.html",
                               name=session["name"],
                               user_id=session["user_id"],
                               weight=profile["weight"],
                               target_weight=profile["target_weight"],
                               goal=profile["fitness_goal"],
                               diet=profile["diet_preference"] 
                               )
    else:

        return render_template("dashboard.html",
                               name=session["name"],
                               user_id=session["user_id"],
                               weight=0,target_weight=0,goal="Not set",diet="Not set"
                               )


# Profile completion form (GET = form, POST = mark completed)
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

# API to save profile data from frontend form
@app.route("/api/complete-profile", methods=["POST"])
@login_required
def complete_profile_api():
    data = request.json
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Session expired. Please log in again."}), 401

    data["user_id"] = user_id  # Attach user ID to the incoming profile data

    if Profile.save_full_profile(data):
        # ✅ Update profile_completed in DB
        db = mysql.connector.connect(**DB_CONFIG)
        cursor = db.cursor()
        cursor.execute("UPDATE users SET profile_completed = 1 WHERE user_id = %s", (user_id,))
        db.commit()
        cursor.close()
        db.close()

        session["profile_completed"] = True
        return jsonify({"message": "Profile saved successfully", "redirect": "/dashboard"}), 200
    else:
        return jsonify({"error": "Failed to save profile"}), 500
    
@app.route('/workout_log')
def workout_log():
    return render_template('workout_log.html')

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
