from flask import Blueprint,request,jsonify
from werkzeug.security import generate_password_hash,check_password_hash
from app import db

auth=Blueprint("auth",__name__)

@auth.route("/signup",methods=["POST"])
def signup():
    data=request.json
    email=data["email"]
    password= generate_password_hash(data["password"])
    
    cursor=db.cursor()
    cursor.execute("INSERT into users (email,password_hash) VALUES(%s,%s)",(email,password))
    db.commit()
    
    return jsonify({"message": "User registered successfully!"})

@auth.route("/login",methods=["POST"])
def login():
    data=request.json
    email=data["email"]
    password=data["password"]
    