from flask import Flask, render_template, session, redirect, url_for, request, jsonify
from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY, SECRET_KEY
from flask_cors import CORS
from flask_login import LoginManager, login_required, current_user
from auth import User  # Import User class from auth.py
from models.user_profile import Profile

# Initialize Flask app
app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = SECRET_KEY
CORS(app, supports_credentials=True)

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Set up Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login_page"

# Load user from session
@login_manager.user_loader
def load_user(user_id):
    response = supabase.table('users').select('id, user_id, name, email, profile_completed').eq('id', user_id).execute()
    if response.data and len(response.data) > 0:
        user_data = response.data[0]
        session["email"] = user_data['email']
        return User(
            id=user_data['id'],
            user_id=user_data['user_id'],
            name=user_data['name'],
            email=user_data['email'],
            profile_completed=bool(user_data['profile_completed'])
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
    
    response = supabase.table('profile').select('weight, target_weight, fitness_goal, diet_preference').eq('user_id', session["user_id"]).execute()
    
    if response.data and len(response.data) > 0:
        profile = response.data[0]
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
                               weight=0, target_weight=0, goal="Not set", diet="Not set"
                               )

# Profile completion form (GET = form, POST = mark completed)
@app.route("/profile-complete", methods=["GET", "POST"])
@login_required
def profile_complete():
    if request.method == "POST":
        response = supabase.table('users').update({'profile_completed': True}).eq('id', session["id"]).execute()
        if response.error:
            return jsonify({"error": str(response.error)}), 500
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
        # Update profile_completed in Supabase
        response = supabase.table('users').update({'profile_completed': True}).eq('user_id', user_id).execute()
        if response.error:
            return jsonify({"error": str(response.error)}), 500

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