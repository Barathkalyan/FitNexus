from flask import Flask, render_template, session, redirect, url_for
import mysql.connector
from config import DB_CONFIG
from flask_cors import CORS
from flask_login import LoginManager
from models.user import User

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
    
    # ✅ Fixed: Changed 'username' to 'name'
    cursor.execute("SELECT id, name, email, profile_completed FROM users WHERE id = %s", (user_id,))
    user_data = cursor.fetchone()
    
    cursor.close()
    db.close()

    return User(user_data["id"], user_data["name"], user_data["email"], user_data["profile_completed"]) if user_data else None

# Import blueprints
from routes.auth import auth
app.register_blueprint(auth, url_prefix="/auth")

@app.route('/')
def index():
    if "id" not in session:
        return redirect(url_for("auth.login_page"))
    return render_template("index.html", user=session["name"]) 
def login():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
