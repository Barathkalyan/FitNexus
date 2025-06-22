from flask import Flask, render_template, session, redirect, url_for, request, jsonify
from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY, SECRET_KEY
from flask_cors import CORS
from flask_login import LoginManager, login_required, current_user
from routes.auth import User

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
        session["user_id"] = user_data['user_id']
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

    # Verify user_id exists in users table
    user_check = supabase.table('users').select('user_id').eq('user_id', user_id).execute()
    if not user_check.data:
        return jsonify({"error": "Invalid user ID."}), 400

    # Prepare profile data, casting strings to integers where needed
    profile_data = {
        "user_id": user_id,
        "age": int(data["age"]) if data["age"] else None,
        "gender": data["gender"],
        "height": int(data["height"]) if data["height"] else None,
        "weight": int(data["weight"]) if data["weight"] else None,
        "fitness_goal": data["fitness_goal"],
        "target_weight": int(data["target_weight"]) if data["target_weight"] else None,
        "diet_preference": data["diet_preference"],
        "workout_time": int(data["workout_time"]) if data["workout_time"] else None,
        "workout_days": int(data["workout_days"]) if data["workout_days"] else None
    }

    # Upsert profile data to handle duplicates
    response = supabase.table('profile').upsert(
        profile_data,
        options={"on_conflict": "user_id"}
    ).execute()

    if response.error:
        return jsonify({"error": str(response.error)}), 500

    # Update profile_completed in users table
    response = supabase.table('users').update({'profile_completed': True}).eq('user_id', user_id).execute()
    if response.error:
        return jsonify({"error": str(response.error)}), 500

    session["profile_completed"] = True
    return jsonify({"message": "Profile saved successfully", "redirect": "/dashboard"}), 200

# Profile page - display and edit user details
@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if not session.get("profile_completed"):
        return redirect(url_for("profile_complete"))

    # Fetch user data from users table
    user_response = supabase.table('users').select('id, user_id, name, email').eq('user_id', session["user_id"]).execute()
    if not user_response.data:
        return jsonify({"error": "User not found."}), 404
    user_data = user_response.data[0]

    # Fetch profile data from profile table
    profile_response = supabase.table('profile').select('*').eq('user_id', session["user_id"]).execute()
    profile_data = profile_response.data[0] if profile_response.data else {}

    if request.method == "POST":
        data = request.json
        user_id = session.get("user_id")

        # Validate user_id
        if not user_id:
            return jsonify({"error": "Session expired. Please log in again."}), 401

        # Update users table
        user_update = {
            "name": data["name"],
            "email": data["email"]
        }
        user_response = supabase.table('users').update(user_update).eq('user_id', user_id).execute()
        if user_response.error:
            return jsonify({"error": str(user_response.error)}), 500

        # Update profile table
        profile_update = {
            "user_id": user_id,
            "age": int(data["age"]) if data["age"] else None,
            "gender": data["gender"],
            "height": int(data["height"]) if data["height"] else None,
            "weight": int(data["weight"]) if data["weight"] else None,
            "fitness_goal": data["fitness_goal"],
            "target_weight": int(data["target_weight"]) if data["target_weight"] else None,
            "diet_preference": data["diet"],
            "workout_time": int(data["workout_time"]) if data["workout_time"] else None,
            "workout_days": int(data["workout_days"]) if data["workout_days"] else None
        }
        profile_response = supabase.table('profile').upsert(
            profile_update,
            options={"on_conflict": "user_id"}
        ).execute()
        if profile_response.error:
            return jsonify({"error": str(profile_response.error)}), 500

        # Update session data
        session["name"] = data["name"]
        session["email"] = data["email"]
        return jsonify({"message": "Profile updated successfully", "redirect": "/dashboard"}), 200

    return render_template("profile.html",
                           user=user_data,
                           profile=profile_data,
                           name=session["name"],
                           user_id=session["user_id"])

# Placeholder routes for sidebar navigation
@app.route("/workout_log")
@login_required
def workout_log():
    if not session.get("profile_completed"):
        return redirect(url_for("profile_complete"))
    return render_template("workout_log.html")  # Ensure this template exists

@app.route("/calorie_intake")
@login_required
def calorie_intake():
    if not session.get("profile_completed"):
        return redirect(url_for("profile_complete"))
    return render_template("calorie_intake.html")  # Ensure this template exists

@app.route("/goal_progress")
@login_required
def goal_progress():
    if not session.get("profile_completed"):
        return redirect(url_for("profile_complete"))
    return render_template("goal_progress.html")  # Ensure this template exists

# Run the app
if __name__ == "__main__":
    app.run(debug=True)