from flask import Flask, render_template, session, redirect, url_for
import mysql.connector
from config import DB_CONFIG
from routes.auth import auth
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

# REGISTERING AUTH BLUEPRINT
app.register_blueprint(auth, url_prefix="/auth")

# ROUTE FOR LANDING PAGE (AFTER LOGIN)
@app.route('/')
def index():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("index.html", user=session["user"])

# ROUTE FOR LOGIN PAGE
@app.route('/login')
def login():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
