from flask import Flask
import mysql.connector
from config import DB_CONFIG
from routes.auth import auth
from flask_cors import CORS

app= Flask(__name__)
CORS(app)

#DATABASE CONNECTION
try:
    db=mysql.connector.connect(**DB_CONFIG)
    cursor=db.cursor()
    print("Database connection succesful!")
except mysql.connector.Error as err:
    print(f"Database connection failed: {err}")
    db= None
    
#IMPORTING AUTH
def register_blueprints():
    from routes.auth import auth
    app.register_blueprint(auth,url_prefix="/auth")
    
register_blueprints()


if __name__== "__main__":
    app.run(debug=True)

