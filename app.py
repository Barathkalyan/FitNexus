from flask import Flask, render_template, session, redirect, url_for
import mysql.connector
from config import DB_CONFIG
from flask_cors import CORS
app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "your_secret_key"
CORS(app)

# DATABASE CONNECTION
try:
    db = mysql.connector.connect(**DB_CONFIG)
    cursor = db.cursor()
    print("Database connection successful!")
except mysql.connector.Error as err:
    print(f"Database connection failed: {err}")
    db = None

# Import blueprints after app is initialized to avoid circular imports
from routes.auth import auth

app.register_blueprint(auth, url_prefix="/auth")

@app.route('/')
def index():
    if "id" not in session:
        return redirect(url_for("auth.login_page"))
    return render_template("index.html", user=session["name"])

@app.route('/login')
def login():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
