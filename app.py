from flask import Flask
import mysql.connector
from config import DB_CONFIG
from routes.auth import auth

app= Flask(__name__)
app.register_blueprint(auth,url_prefix="/auth")

if __name__== "__main__":
    app.run(debug=True)

db=mysql.connector.connect(**DB_CONFIG)
cursor=db.cursor()
