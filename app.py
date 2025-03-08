from flask import Flask
import mysql.connector
from config import DB_CONFIG


app= Flask(__name__)

#DB CONNECTION
db=mysql.connector.connect(**DB_CONFIG)
cursor=db.cursor()

#IMPORTING AUTH
from routes.auth import auth
app.register_blueprint(auth,url_prefix="/auth")

if __name__== "__main__":
    app.run(debug=True)

