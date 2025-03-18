from flask import Flask, render_template
import mysql.connector
from config import DB_CONFIG
from routes.auth import auth
from flask_cors import CORS

app = Flask(__name__, template_folder="templates", static_folder="static")
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
def register_blueprints():
    from routes.auth import auth
    app.register_blueprint(auth, url_prefix="/auth")

register_blueprints()

# ROUTE FOR LANDING PAGE
@app.route('/')
def index():
    return render_template('index.html', user="bk")  # Change "YourName" as needed

if __name__ == "__main__":
    app.run(debug=True)
