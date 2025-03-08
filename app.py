from flask import Flask
import mysql.connector
from config import DB_CONFIG

app= Flask(__name__)

db=mysql.connector.connect(**DB_CONFIG)
cursor=db.cursor()
